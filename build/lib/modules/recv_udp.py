#!/usr/bin/env python

"""#!/usr/bin/env -S uv run --script.

Run this script using uv
init uv with `uv init && uv venv && source .venv/bin/activate`
Check `skeletons/tools/py` for a list of currently preferred tools
"""

import socket
import struct
import sys
import time

from loguru import logger
from rich.logging import RichHandler

from constants import classes, constants, dataframes

# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    sys.stderr,
)
logger.configure(
    handlers=[
        {"sink": "file.log", "level": "TRACE"},
        {
            "sink": RichHandler(
                rich_tracebacks=True, show_path=True, tracebacks_show_locals=True
            ),
            "level": "DEBUG",
        },
    ]
)

session_info = dataframes.session_info_dataframe
lap_info = dataframes.race_timing_dataframe
damage_info = dataframes.car_info_dataframe

# int8: b
# uint8: B
# int16: h
# uint16: H
# int32: l
# uint32: L
# int64: q
# uint64: Q
# float: f
# string: s

# Set some variables
check_iterations = 0


def sort_packets(data):
    logger.trace(data)
    header_data = classes.Header.from_buffer_copy(data)
    logger.trace({k: getattr(header_data, k) for k, ctype in header_data._fields_})
    packet_id = header_data.packet_id
    logger.trace(f"Received header packet_id of: {packet_id}")
    match packet_id:
        case 1:
            relevant = classes.SessionData.from_buffer_copy(data)
            relevant_data = {k: getattr(relevant, k) for k, ctype in relevant._fields_}
            logger.debug(relevant_data)
            return relevant_data
        case 2:
            relevant = classes.LapDataPacket.from_buffer_copy(data)
            relevant_data = {k: getattr(relevant, k) for k, ctype in relevant._fields_}
            logger.debug(relevant_data)
            return relevant_data
        case 4:
            relevant = classes.ParticipantsPacket.from_buffer_copy(data)
            relevant_data = {k: getattr(relevant, k) for k, ctype in relevant._fields_}
            logger.debug(relevant_data)
            return relevant_data
        case 7:
            relevant = classes.CarStatusPacket.from_buffer_copy(data)
            relevant_data = {k: getattr(relevant, k) for k, ctype in relevant._fields_}
            logger.debug(relevant_data)
            return relevant_data
        case 10:
            relevant = classes.CarDamagePacket.from_buffer_copy(data)
            relevant_data = {k: getattr(relevant, k) for k, ctype in relevant._fields_}
            logger.debug(relevant_data)
            return relevant_data


def find_player_data(header_data, optional_opponent: str, longer_data_packet_example):
    logger.trace(header_data)
    player_one_data = header_data["player_car_index"]
    if optional_opponent is not None:
        valid_values = constants.DRIVER_ID_DICT.values()
        if optional_opponent in valid_values:
            is_opponent_in_this_race = False
            while (not is_opponent_in_this_race) and (
                check_iterations < len(longer_data_packet_example)
            ):
                pass


def recv_udp_data(ip: str, port: int):
    """Receive the data from specified ip and url."""
    sock = socket.socket(
        socket.AF_INET,  # Internet
        socket.SOCK_DGRAM,
    )  # UDP
    sock.settimeout(10)
    sock.bind((ip, port))

    logger.trace(f"Attempting UDP connection at {ip}:{port}....")
    while True:
        try:
            data, addr = sock.recvfrom(65507)  # buffer size is 65507 bytes
            if data is not None:
                logger.trace(data)
                sort_packets(data)
        except TimeoutError:
            logger.debug(f"No UDP connection at {ip}:{port}....")
            logger.debug("Retrying in 10s...")
            time.sleep(10)


if __name__ == "__main__":
    # TODO make a cli to choose url and port
    recv_udp_data("0.0.0.0", 20127)
