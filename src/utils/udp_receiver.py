#!/usr/bin/env -S uv run --script
## Recieves UDP data and adds it to a queue
## after some very basic filtering

import multiprocessing as mp
import socket
import struct
import sys
from typing import Optional

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


# 1 MB socket buffer; tune upward if kernel drops packets
SO_RCVBUF_SIZE = 1_048_576


def udp_receiver(
    bind_addr: str,
    bind_port: int,
    queue: mp.Queue,
    max_qsize: int = 100_000,
    chunk_size: int = 65_507,  ## The largest UDP payload over IPv4
    stop_event: mp.synchronize.Event | None = None,
) -> None:

    # any other process can call stop_event.set() to break the loop and exit cleanly
    if stop_event is None:
        stop_event = mp.Event()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SO_RCVBUF_SIZE)
    sock.bind((bind_addr, bind_port))

    logging.info("UDP receiver listening on %s:%d", bind_addr, bind_port)

    try:
        while not stop_event.is_set():
            try:
                data, _ = sock.recvfrom(chunk_size)
                if queue.qsize() < max_qsize:
                    queue.put_nowait(data)
            except OSError:
                # Ignore transient errors; keep spinning
                continue
    finally:
        sock.close()
        logging.info("UDP receiver shutdown complete")


if __name__ == "__main__":
    pass
