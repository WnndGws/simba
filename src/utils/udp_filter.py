#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

import multiprocessing
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


def decode_packets(packet):
    pass


if __name__ == "__main__":
    pass
