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
                output_queue.put_nowait(decode_udp(data, length))
                read_idx = (read_idx + 1) % (shared_memory_size // slot_size)
            else:
                time.sleep(0.01)  # Backoff when empty
        except KeyboardInterrupt:
            shm.unlink()
            shm.close()
            break


def decode_udp(packet: bytes, length: int):
    udp_protocol.Header.decode(packet)
    match length:
        case 1349:
            udp_protocol.MotionPacket.decode(packet)
        case 753:
            udp_protocol.SessionPacket.decode(packet)
        case 1285:
            udp_protocol.LapdataPacket.decode(packet)
        case 45:
            udp_protocol.EventPacket.decode(packet)
        case 1284:
            udp_protocol.ParticipantsPacket.decode(packet)
        case 1133:
            udp_protocol.SetupPacket.decode(packet)
        case 1352:
            udp_protocol.TelemetryPacket.decode(packet)
        case 1239:
            udp_protocol.StatusPacket.decode(packet)
        case 1042:
            udp_protocol.ClassificationPacket.decode(packet)
        case 954:
            udp_protocol.LobbyPacket.decode(packet)
        case 1041:
            udp_protocol.DamagePacket.decode(packet)
        case 1460:
            udp_protocol.SessionHistoryPacket.decode(packet)
        case 231:
            udp_protocol.TyreSetsPacket.decode(packet)
        case 273:
            udp_protocol.ExMotionPacket.decode(packet)
        case 101:
            # TimeTrial
            pass
        case 1131:
            udp_protocol.LapPositionPacket.decode(packet)
        case _:
            pass


if __name__ == "__main__":
    receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver.start()

    queue = Queue()
    process_named_shared_memory(output_queue=queue)
