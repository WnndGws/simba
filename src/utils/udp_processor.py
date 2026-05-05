#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import asyncio
import copy
import struct
import time
from multiprocessing import Process, Queue, shared_memory

from loguru import logger

from models import udp_protocol
from utils import udp_receiver

PACKET_MAP = {
    1349: ("motion", udp_protocol.MotionPacket.decode),
    753: ("session", udp_protocol.SessionPacket.decode),
    1285: ("lapdata", udp_protocol.LapdataPacket.decode),
    45: ("event", udp_protocol.EventPacket.decode),
    1284: ("participants", udp_protocol.ParticipantsPacket.decode),
    1133: ("setup", udp_protocol.SetupPacket.decode),
    1352: ("telemetry", udp_protocol.TelemetryPacket.decode),
    1239: ("status", udp_protocol.StatusPacket.decode),
    1042: ("classification", udp_protocol.ClassificationPacket.decode),
    954: ("lobby", udp_protocol.LobbyPacket.decode),
    1041: ("damage", udp_protocol.DamagePacket.decode),
    1460: ("session_history", udp_protocol.SessionHistoryPacket.decode),
    231: ("tyresets", udp_protocol.TyreSetsPacket.decode),
    273: ("exmotion", udp_protocol.ExMotionPacket.decode),
    101: ("timetrial", None),  # placeholder
    1131: ("lapposition", udp_protocol.LapPositionPacket.decode),
}


def process_named_shared_memory(
    output_queue: Queue,
    shared_memory_name: str = "udp_queue",
    shared_memory_size: int = 100 * 1024 * 1024,
    decode_list: list[str] = [],
):
    shm = shared_memory.SharedMemory(name=shared_memory_name)
    slot_size = 65535 + 9
    read_idx = 0

    while True:
        try:
            offset = read_idx * slot_size
            ready = shm.buf[offset + 4 + 65535]

            if ready == 1:
                length = struct.unpack("I", shm.buf[offset : offset + 4])[0]
                data = bytes(shm.buf[offset + 4 : offset + 4 + length])

                # Clear flag and process
                shm.buf[offset + 4 + 65535] = 0
                output_queue.put_nowait(decode_udp(data, length, decode_list))
                read_idx = (read_idx + 1) % (shared_memory_size // slot_size)
            else:
                time.sleep(0.01)  # Backoff when empty
        except KeyboardInterrupt:
            shm.unlink()
            shm.close()
            break


def decode_udp(packet: bytes, length: int, decode_list: list[str]):
    if len(decode_list) == 0:
        decode_list = [
            "motion",
            "session",
            "lapdata",
            "event",
            "participants",
            "setup",
            "telemetry",
            "status",
            "classification",
            "lobby",
            "damage",
            "session_history",
            "tyresets",
            "exmotion",
            "lapposition",
        ]
    else:
        decode_list = set(decode_list)

    name, func = PACKET_MAP.get(length)
    if name is not None and name in decode_list:
        udp_protocol.Header.decode(packet)
        func(packet)


if __name__ == "__main__":
    receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver.start()

    queue = Queue()
    process_named_shared_memory(output_queue=queue)
