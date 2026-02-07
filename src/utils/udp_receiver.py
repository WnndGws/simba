#!/usr/bin/env -S uv run --script
## Recieves UDP data and adds it to a queue
## after some very basic filtering

import multiprocessing
import socket
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


def udp_receiver(
    bind_addr: str,
    bind_port: int,
    output: multiprocessing.Queue,
    max_qsize: int = 100_000,
    chunk_size: int = 65_507,  ## The largest UDP payload over IPv4
    stop_event: multiprocessing.synchronize.Event | None = None,
) -> None:

    # any other process can call stop_event.set() to break the loop and exit cleanly
    if stop_event is None:
        stop_event = multiprocessing.Event()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 * chunk_size)
    sock.settimeout(0.2)  # non-blocking check for stop_event
    sock.bind((bind_addr, bind_port))

    logger.info("UDP receiver listening on %s:%d", bind_addr, bind_port)

    try:
        while not stop_event.is_set():
            try:
                data, _ = sock.recvfrom(chunk_size)
                logger.trace(data)
                if output.qsize() < max_qsize:
                    output.put_nowait(data)
            except TimeoutError:
                continue
            except KeyboardInterrupt:
                logger.info("Recieved KeyboardInterrupt. Stopping")
                stop_event.set()
    finally:
        sock.close()
        logger.info("UDP receiver shutdown complete")


if __name__ == "__main__":
    pass
