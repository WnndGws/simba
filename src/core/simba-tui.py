#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

import ast
import random
import time
from dataclasses import fields
from multiprocessing import Process, Queue
from pathlib import Path

from loguru import logger  ## imports main one set up in udp_receiver
from rich.live import Live

from config import shared_variables as shared
from models import decode_dictionaries, rich_layout
from utils import layout_updaters, udp_processor, udp_receiver


def process_data(header, values, layout, shared):
    shared.header = header

    if header.packet_id == 1:
        shared.prev_session = shared.session
        shared.session = values
        layout_updaters.update_using_session(layout, shared)
        time.sleep(0.05)
    if header.packet_id == 2 and shared.participants_cache != 0:
        if shared.prev_lapdata is None:
            shared.prev_lapdata = values
            shared.lapdata = values
        else:
            shared.prev_lapdata = shared.lapdata
            shared.lapdata = values
        layout_updaters.update_using_lapdata(layout, shared)
        time.sleep(0.05)
    if header.packet_id == 3:
        shared.event = values
        layout_updaters.update_using_event(layout, shared)
    if header.packet_id == 4 and shared.participants_cache == 0:
        shared.participants = values.cars
        shared.participants_cache += 1
    if header.packet_id == 5:
        shared.prev_setup = shared.telemetry
        shared.setup = values
    if header.packet_id == 6:
        shared.prev_telemetry = shared.telemetry
        shared.telemetry = values
        layout_updaters.update_using_telemetry(layout, shared)
    if header.packet_id == 7:
        shared.prev_status = shared.status
        shared.status = values
    if header.packet_id == 8:
        shared.prev_classification = shared.classification
        shared.classification = values
    if header.packet_id == 9 and shared.lobby_cache == 0:
        shared.lobby = values
        shared.lobby_cache += 1
    if header.packet_id == 10:
        shared.prev_damage = shared.damage
        shared.damage = values
        layout_updaters.update_using_damage(layout, shared)
    if header.packet_id == 11:
        if values.relevant_car_id == header.player_car_index:
            shared.player_histories += 1
        shared.history[values.relevant_car_id] = {
            "number_of_laps_in_data": values.number_of_laps_in_data,
            "number_of_tyre_stints": values.number_of_tyre_stints,
            "best_lap_number": values.best_lap_number,
            "best_s1_lap_number": values.best_s1_lap_number,
            "best_s2_lap_number": values.best_s2_lap_number,
            "best_s3_lap_number": values.best_s3_lap_number,
            "lap_history_data": values.lap_history_data,
            "tyre_history_data": values.tyre_history_data,
        }
    if header.packet_id == 12:
        shared.tyres[values.car_idx] = {
            "tyre_sets_data": values.tyre_set_data,
            "fitted_idx": values.fitted_idx,
        }
        layout_updaters.update_using_available_tyres(layout, shared)
    if header.packet_id == 13:
        shared.prev_exmotion = shared.exmotion
        shared.exmotion = values
    if header.packet_id == 14:
        shared.prev_timetrial = shared.timetrial
        shared.timetrial = values
    if header.packet_id == 15:
        shared.position_history = values


def main():
    layout = rich_layout.create_race_layout()

    item_queue = Queue()

    receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver.start()

    producer = Process(
        target=udp_processor.process_named_shared_memory,
        args=(item_queue,),
        daemon=True,
    )
    producer.start()

    with Live(layout, refresh_per_second=10, screen=False):
        while True:
            if not item_queue.empty():
                header, values = item_queue.get()
                process_data(header, values, layout, shared)
            else:
                time.sleep(0.5)


def test_layout():
    layout = rich_layout.create_race_layout()

    def load_test_data(filepath: str) -> list:
        all_data = []
        with Path.open(filepath, "r") as f:
            for line in f:
                line.strip()
                if line:
                    all_data.append(ast.literal_eval(line))

        return all_data

    data = load_test_data("src/tests/race.log")

    with Live(layout, refresh_per_second=10, screen=True):
        for length, packet in data:
            header, values = udp_processor.decode_udp(packet, length)
            process_data(header, values, layout, shared)


if __name__ == "__main__":
    main()
    # test_layout()
