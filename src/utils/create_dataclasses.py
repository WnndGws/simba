#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import multiprocessing
import sys
import time

from loguru import logger
from rich.logging import RichHandler

from models import classes, constants
from utils import create_dataclasses, udp_filter

# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    sys.stderr,
)
logger.configure(
    handlers=[
        {
            "sink": RichHandler(
                rich_tracebacks=True, show_path=True, tracebacks_show_locals=True
            ),
            "level": "CRITICAL",
        },
    ]
)


session_info = classes.SessionInfo()
wg_data = classes.PlayerInfo()
sg_data = classes.PlayerInfo()


def udp_to_class_info(
    ingest: multiprocessing.Queue,
    output: multiprocessing.Queue,
    session,
    player1,
    player2,
    stop_event: multiprocessing.synchronize.Event | None = None,
):
    # Continue until stopped
    if stop_event is None:
        stop_event = multiprocessing.Event()

    while not stop_event.is_set():
        try:
            raw = ingest.get(timeout=0.2)
            try:
                packet_type = next(iter(raw))
            except StopIteration:
                return
            logger.critical(f"Presenting Queue size: {ingest.qsize()}")
            raw = raw[packet_type]
            match packet_type:
                case 0:
                    pass
                case 1:
                    session_info.track = constants.TRACK_DICT[raw["track_id"]]
                    session_info.session_type = constants.SESSION_TYPE_DICT[
                        raw["session_type"]
                    ]
                    session_info.track_temp = raw["track_temp_c"]
                    session_info.air_temp = raw["air_temp_c"]
                    session_info.weather = constants.WEATHER_TYPE_DICT[raw["weather"]]
                    session_info.track_length_m = raw["track_length_m"]
                    session_info.total_race_laps = raw["total_race_laps"]
                    session_info.session_duration_s = raw["session_duration_seconds"]
                    session_info.session_time_remaining_s = raw[
                        "session_time_remaining_seconds"
                    ]
                    session_info.difficulty = raw["ai_difficulty_level"]
                    session_info.parc_ferme = constants.PARC_FERME_DICT[
                        raw["parc_ferme"]
                    ]
                    logger.critical(session_info)
                    output.put_nowait(session_info)
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case 7:
                    pass
                case 8:
                    pass
                case 9:
                    pass
                case 10:
                    pass
                case 11:
                    pass
                case 12:
                    pass
        except KeyboardInterrupt:
            stop_event.set()
        except multiprocessing.queues.Empty:
            logger.critical("Queue Empty")
            time.sleep(1)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    raw_queue = multiprocessing.Queue()
    decoded_queue = multiprocessing.Queue()
    session_queue = multiprocessing.Queue()
    lap_queue = multiprocessing.Queue()
    terminate = multiprocessing.Event()

    session_info = classes.SessionInfo()
    p1_info = classes.PlayerInfo()
    p2_info = classes.PlayerInfo()

    logger.critical(session_info)

    num_workers = int(multiprocessing.cpu_count() / 4)
    decode_posse = []
    presenting_posse = []

    for _ in range(num_workers):
        decode_worker_process = multiprocessing.Process(
            target=udp_filter.decode_worker,
            args=(raw_queue, decoded_queue, terminate),
            daemon=True,
            name=f"comrade_decoder_{_ + 1}",
        )
        decode_posse.append(decode_worker_process)
        decode_worker_process.start()

    for _ in range(num_workers):
        presenting_worker_process = multiprocessing.Process(
            target=udp_to_class_info,
            args=(decoded_queue, session_queue, session_info, p1_info, p2_info),
            daemon=True,
            name=f"comrade_presenter_{_ + 1}",
        )
        presenting_posse.append(presenting_worker_process)
        presenting_worker_process.start()

    udp_filter.start_udp_queue(raw_queue)

    # Wait for workers to finish
    for comrade in decode_posse:
        comrade.join()
