#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

import multiprocessing
import time

import rich
from loguru import logger

from models import classes, constants
from utils import create_dataclasses, udp_receiver

# Global variables for signal handler access
stop_event = multiprocessing.Event()
receiver_thread = None


class SharedStateManager:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.lock = multiprocessing.Lock()

        # Initialize shared data structures
        self.session_data = self.manager.Namespace()
        self.admin_data = self.manager.Namespace()
        self.cars_data = self.manager.dict()

        # Initialize with default values
        self._initialize_data()

    def _initialize_data(self):
        # Convert dataclass instances to manager-compatible structures
        session_instance = create_dataclasses.init_session_data()
        admin_instance = create_dataclasses.init_admin_data()
        cars_instance = create_dataclasses.init_cars_data()

        # For session_data and admin_data, copy attributes to Namespace
        for key, value in session_instance.__dict__.items():
            setattr(self.session_data, key, value)

        for key, value in admin_instance.__dict__.items():
            setattr(self.admin_data, key, value)

        # For cars_data, each car is a separate dataclass instance
        for car_id, car_instance in cars_instance.items():
            car_proxy = self.manager.Namespace()
            for key, value in car_instance.__dict__.items():
                setattr(car_proxy, key, value)
            self.cars_data[car_id] = car_proxy


# Global shared state manager
shared_state = None


def get_shared_state():
    global shared_state
    if shared_state is None:
        shared_state = SharedStateManager()
    return shared_state


def start_udp_queue(output: multiprocessing.Queue):
    global stop_event

    logger.debug("Starting UDP receiver")
    receiver_thread = multiprocessing.Process(
        target=udp_receiver.udp_receiver,
        args=("0.0.0.0", 20127, output, 65507, stop_event),
    )
    receiver_thread.daemon = True
    receiver_thread.start()


def decode_packets(packet):
    # logger.trace(packet)

    state = get_shared_state()

    header_data = classes.Header.from_buffer_copy(packet)
    packet_id = header_data.packet_id
    user_car = header_data.player_car_index
    logger.debug(f"Received header packet_id of: {packet_id}")

    if packet_id not in constants.PACKET_CLASS_DICT:
        logger.debug(f"Packet ID {packet_id} not in PACKET_CLASS_DICT")
        return

    packet_class = constants.PACKET_CLASS_DICT[packet_id]
    packet_class = packet_class.from_buffer_copy(packet)
    packet_data = {k: getattr(packet_class, k) for k, ctype in packet_class._fields_}
    logger.trace(packet_class)

    # Update the admin data with header information
    state.admin_data.packet_id = packet_id

    # Update shared state with locking for thread safety
    with state.lock:
        match packet_id:
            case 0:
                create_dataclasses.update_with_motion(
                    packet_data,
                    state.session_data,
                    state.cars_data,
                    header_data.player_car_index,
                )
            case 1:
                create_dataclasses.update_with_sessiondata(
                    packet_data, state.session_data
                )
            case 2:
                create_dataclasses.update_with_lapdata(
                    packet_data, state.cars_data, user_car
                )
            case 3:
                create_dataclasses.update_with_event_data(
                    packet_data, state.cars_data, state.session_data
                )
            case 4:
                create_dataclasses.update_with_participants_data(
                    packet_data, state.cars_data, state.session_data
                )
            case 5:
                create_dataclasses.update_with_car_setup_data(
                    packet_data, state.cars_data, header_data.player_car_index
                )
            case 6:
                create_dataclasses.update_with_car_telemetry_data(
                    packet_data, state.cars_data, header_data.player_car_index
                )
            case 7:
                create_dataclasses.update_with_car_status_data(
                    packet_data, state.cars_data, header_data.player_car_index
                )
            case 10:
                create_dataclasses.update_with_car_damage_data(
                    packet_data, state.cars_data, header_data.player_car_index
                )
            case 11:
                create_dataclasses.update_with_session_history_data(
                    packet_data, state.cars_data, header_data.player_car_index
                )
            case 12:
                create_dataclasses.update_with_tyre_sets_data(
                    packet_data, state.cars_data, header_data.player_car_index
                )


def main():
    raw_queue = multiprocessing.Queue()

    state = get_shared_state()

    start_udp_queue(raw_queue)

    while True:
        if not raw_queue.empty():
            data = raw_queue.get()
            # Pass all data structures to the decode function
            decode_packets(data)
        else:
            time.sleep(0.1)


if __name__ == "__main__":
    main()
