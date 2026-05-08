#!/usr/bin/env python

from multiprocessing import Process, Queue, shared_memory

from loguru import logger
from rich.logging import RichHandler

from utils import brake_point_finder, udp_processor, udp_receiver, udp_simulator

#
# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    RichHandler(rich_tracebacks=True, show_path=True, tracebacks_show_locals=True),
    level="INFO",
)
logger.add("udp.log", level="CRITICAL", format="{message}")

if __name__ == "__main__":
    q = brake_point_finder.create_queue()
    brake_point_finder.yield_queue(q)
