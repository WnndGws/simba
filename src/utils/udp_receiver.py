#!/usr/bin/env -S uv run --script
## Receives UDP data and adds it to a queue
## after some very basic filtering

import multiprocessing
import signal
import socket
import sys
import time

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
            "level": "WARNING",
        }
    ]
)

# Global variables for signal handler access
stop_event = multiprocessing.Event()
receiver_thread = None


def udp_receiver(
    bind_addr: str,
    bind_port: int,
    output: multiprocessing.Queue,
    chunk_size: int = 65_507,  ## The largest UDP payload over IPv4
    stop_event: multiprocessing.Event | None = None,
) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 * chunk_size)
    sock.settimeout(0.2)  # Non-blocking check for stop_event
    sock.bind((bind_addr, bind_port))

    logger.info(f"UDP receiver listening on {bind_addr}:{bind_port}")

    while not stop_event.is_set():
        try:
            data, _ = sock.recvfrom(chunk_size)
            # logger.trace(data)
            output.put_nowait(data)
        except TimeoutError:
            pass  # Normal behavior, just try again
        except OSError as e:
            logger.error(f"Socket error: {e}")
            break

    logger.info("UDP receiver stopped")
    sock.close()


def main():
    # Mainly use as a way to test the file.
    # Use the main as the starting point for the module that ingests this file

    multiprocessing.set_start_method("spawn")
    stop_event = multiprocessing.Event()
    # Create thread-safe queue for output
    output_queue = multiprocessing.Queue()

    # Start UDP receiver thread
    receiver_thread = multiprocessing.Process(
        target=udp_receiver, args=("0.0.0.0", 20127, output_queue, 65507, stop_event)
    )
    receiver_thread.daemon = True
    receiver_thread.start()

    try:
        while True:
            # Main thread can process items from output_queue
            if not output_queue.empty():
                data = output_queue.get()
                logger.trace(data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, stopping UDP receiver...")
        if stop_event and receiver_thread:
            stop_event.set()
            receiver_thread.join(timeout=2.0)


if __name__ == "__main__":
    main()
