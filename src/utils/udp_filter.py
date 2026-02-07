#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

import multiprocessing
import signal
import sys
import time

from loguru import logger
from rich.logging import RichHandler

from models import classes, constants
from utils import udp_receiver

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
        }
    ]
)


def start_udp_queue(output: multiprocessing.Queue):
    multiprocessing.set_start_method("spawn", force=True)

    terminate = multiprocessing.Event()

    # Allow me to interrupt it
    def sigint_handler(signum, frame):
        terminate.set()

    signal.signal(signal.SIGINT, sigint_handler)

    producer = multiprocessing.Process(
        target=udp_receiver.udp_receiver, args=("0.0.0.0", 20127, output), daemon=True
    )
    logger.info("Starting UDP queue")
    producer.start()


def packet_to_dict(packet) -> dict:
    """Recursively convert ctypes to dictionaries."""
    # check if it has fields
    if hasattr(packet, "_fields_"):
        # non recursive, so simply wrap the getattr in this function again
        # return {field: getattr(packet, field) for field, _ctypes in packet._fields_}
        return {
            field: packet_to_dict(getattr(packet, field))
            for field, _ctypes in packet._fields_
        }
    # handle things like LapData * 22
    if hasattr(packet, "_type_") and hasattr(packet, "_length_"):
        return [packet_to_dict(item) for item in packet]

    # handle arrays that are actually ctypes
    if hasattr(packet, "_fields_") and hasattr(packet, "_pack_"):
        return {
            field: packet_to_dict(getattr(packet, field))
            for field, _ in packet._fields_
        }

    # handle things that are already decoded
    return packet


def decode_packets(packet):
    logger.trace(packet)

    header_data = classes.Header.from_buffer_copy(packet)
    packet_id = header_data.packet_id
    logger.debug(f"Received header packet_id of: {packet_id}")

    if packet_id not in constants.PACKET_CLASS_DICT:
        logger.debug(f"Cant handle packet_id of: {packet_id}")
        return {}

    packet_class = constants.PACKET_CLASS_DICT[packet_id]
    packet_class = packet_class.from_buffer_copy(packet)
    result = packet_to_dict(packet_class)
    #
    # Need to handle stupid event packet seperately
    if packet_id == 3:
        event_code = packet_class.event_code_string.decode("ascii")
        logger.debug(f"Handling event_code: {event_code}")
        if event_code in constants.EVENT_DICT:
            event_class = constants.EVENT_DICT[event_code]
            if type(event_class) == str:
                result["event_data"] = event_class
            else:
                event_data = event_class.from_buffer_copy(packet)
                result["event_data"] = packet_to_dict(event_data)

    logger.debug(result)
    return {packet_id: result}


def decode_worker(
    ingest: multiprocessing.Queue,
    output: multiprocessing.Queue,
    stop_event: multiprocessing.synchronize.Event | None = None,
) -> None:

    # Continue until stopped
    if stop_event is None:
        stop_event = multiprocessing.Event()

    logger.info("Decoding of stack started")
    logger.critical(f"Decode Queue size: {ingest.qsize()}")
    try:
        while not stop_event.is_set():
            try:
                raw = ingest.get(timeout=0.2)
                decoded_data = decode_packets(raw)
                if decoded_data is not None:
                    output.put_nowait(decoded_data)
            except KeyboardInterrupt:
                stop_event.set()
            except multiprocessing.queues.Empty:
                logger.info("Attempted to ingest queue, but it was empty")
                logger.info("Sleeping for 5 seconds before retrying")
                try:
                    time.sleep(5)
                    continue
                except KeyboardInterrupt:
                    stop_event.set()

    finally:
        # drain inbound so the sender can join
        while not ingest.empty():
            try:
                ingest.get_nowait()
            except Exception:
                break

        logger.info("Decoding of stack stopped")


if __name__ == "__main__":
    ## Test output
    multiprocessing.set_start_method("spawn", force=True)
    raw_queue = multiprocessing.Queue()
    decoded_queue = multiprocessing.Queue()
    terminate = multiprocessing.Event()

    num_workers = int(multiprocessing.cpu_count() / 2)
    decode_posse = []

    for _ in range(num_workers):
        decode_worker_process = multiprocessing.Process(
            target=decode_worker,
            args=(raw_queue, decoded_queue, terminate),
            daemon=True,
            name=f"comrade_worker_{_ + 1}",
        )
        decode_posse.append(decode_worker_process)
        decode_worker_process.start()
        logger.debug(f"Started worker: {decode_worker_process.name}")

    start_udp_queue(raw_queue)

    # Wait for workers to finish
    for comrade in decode_posse:
        comrade.join()
        logger.debug(f"{comrade.name} has completed their worker")
