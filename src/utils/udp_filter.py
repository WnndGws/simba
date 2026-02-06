#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

import multiprocessing
import signal
import sys

import udp_receiver
from loguru import logger
from rich.logging import RichHandler

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
            "level": "INFO",
        }
    ]
)


def receive_stack():
    multiprocessing.set_start_method("spawn", force=True)
    packet_queue = multiprocessing.Queue()
    terminate = multiprocessing.Event()

    # Allow me to interrupt it
    def sigint_handler(signum, frame):
        terminate.set()

    signal.signal(signal.SIGINT, sigint_handler)

    producer = multiprocessing.Process(
        target=udp_receiver.udp_receiver, args=("0.0.0.0", 20127), daemon=True
    )
    producer.start()
    try:
        while True:
            payload = packet_queue.get(timeout=0.5)
            # TODO: process payload
            logger.debug(f"Received payload {len(payload)} bytes long")
    except KeyboardInterrupt:
        terminate.set()
    finally:
        receiver.join()


def decode_packets(packet):
    pass


if __name__ == "__main__":
    pass
