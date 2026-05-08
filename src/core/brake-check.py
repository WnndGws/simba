#!/usr/bin/env python

from multiprocessing import Process, Queue, shared_memory

from loguru import logger
from rich.logging import RichHandler

from utils import udp_processor, udp_receiver, udp_simulator

#
# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    RichHandler(rich_tracebacks=True, show_path=True, tracebacks_show_locals=True),
    level="INFO",
)
logger.add("udp.log", level="CRITICAL", format="{message}")

if __name__ == "__main__":
    # receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver = Process(target=udp_simulator.udp_receiver, daemon=True)
    receiver.start()

    queue = Queue()
    udp_processor.process_named_shared_memory(
        output_queue=queue, decode_list=["lapdata"]
    )
