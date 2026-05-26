#!/usr/bin/env python

from dataclasses import dataclass, field
from math import ceil, floor
from multiprocessing import Queue, get_context
from queue import Empty

from loguru import logger
from rich import print
from rich.logging import RichHandler
from tinydb import Query, TinyDB

from utils import udp_processor, udp_simulator

#
# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    RichHandler(rich_tracebacks=True, show_path=True, tracebacks_show_locals=True),
    level="WARNING",
)
# logger.add("udp.log", level="CRITICAL", format="{message}")


@dataclass()
class Stats:
    name: str = ""
    lap_number: int = 0
    brake: int = 0
    distance: float = 0.0
    distance25: int = 0
    drs_status: str = ""
    ers_status: str = ""
    brake_history: list = field(default_factory=list)

    def __post_init__(self):
        self.db = TinyDB("brake_history.json")
        self.brake_query = Query()

    def update_brake(self, new_brake_value: int):
        if self.brake != new_brake_value:
            if self.brake == 0 and new_brake_value == 1:
                self.table = self.db.table(f"lap_{self.lap_number}")
                self.table.insert(
                    {
                        "distance": self.distance,
                        "distance25": self.distance25,
                        "drs": self.drs_status,
                        "ers": self.ers_status,
                    },
                )
                logger.warning("Added db value")
            self.brake = new_brake_value


player_stats = Stats()


def check_braking(item_tuple: tuple):
    player_idx = item_tuple[0].player_car_index
    packet_idx = item_tuple[0].packet_id
    match packet_idx:
        case 6:
            _brake = ceil(item_tuple[1].statuses[player_idx].brake)
            _drs = item_tuple[1].statuses[player_idx].drs
            player_stats.update_brake(_brake)
            player_stats.drs_status = _drs
            logger.debug(player_stats)
        case 4:
            _name = item_tuple[1].cars[player_idx].name
            player_stats.name = _name
            logger.debug(player_stats)
        case 2:
            _distance = item_tuple[1].cars[player_idx].lap_distance_travelled_m
            _lap = item_tuple[1].cars[player_idx].current_lap_number
            player_stats.distance = _distance
            # Round down to nearest multiple of 25
            player_stats.distance25 = floor(_distance / 25) * 25
            player_stats.lap_number = _lap
            logger.debug(player_stats)
        case 7:
            _ers = item_tuple[1].statuses[player_idx].ers_deploy_mode
            player_stats.ers_status = _ers
            logger.debug(player_stats)


def consumer(in_q: Queue) -> None:
    while True:
        try:
            item = in_q.get(timeout=1.0)
            logger.debug(item)
            check_braking(item)
        except Empty:
            continue


if __name__ == "__main__":
    ctx = get_context("fork")
    receiver = ctx.Process(
        target=lambda: udp_simulator.udp_receiver(rate_hz=100),
        daemon=True,
    )
    receiver.start()

    q_1 = ctx.Queue()
    consumer = ctx.Process(target=consumer, args=(q_1,), daemon=True)
    consumer.start()

    udp_processor.process_named_shared_memory(
        output_queue=q_1,
        decode_list=["telemetry", "participants", "lapdata", "status"],
    )

    receiver.join()
    consumer.join()

    print(player_stats.db.all())
