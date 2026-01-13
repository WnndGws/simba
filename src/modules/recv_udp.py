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
player_index = None
other_humans = []


def sort_packets(data):
    global player_index
    global other_humans

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
            relevant_data = {k: getattr(relevant, k) for k, ctype in relevant._fields_}[
                "participants_data"
            ]
            logger.debug(relevant_data)
            if player_index is None:
                player_index, other_humans = find_player_data(
                    header_data, relevant_data
                )
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


def find_player_data(header_data, participants_data):
    logger.trace(header_data)
    player_index = header_data["player_car_index"]
    other_humans = []
    for idx, participant in enumerate(participants_data):
        if participant["is_ai_controlled_flag"] == 0:
            other_humans.append[idx]

    logger.debug("Player Index: {player_index}")
    logger.debug("Other humans: {other_humans}")
    return player_index, other_humans


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
