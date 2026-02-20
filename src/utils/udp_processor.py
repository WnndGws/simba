#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import struct
import time
from multiprocessing import Process, shared_memory

from model import udp_protocol
from utils import udp_receiver


def process_named_shared_memory(
    shared_memory_name="udp_queue", shared_memory_size=100 * 1024 * 1024
):
    shm = shared_memory.SharedMemory(name=shared_memory_name)
    slot_size = 65535 + 9
    read_idx = 0

    while True:
        offset = read_idx * slot_size
        ready = shm.buf[offset + 4 + 65535]

        if ready == 1:
            length = struct.unpack("I", shm.buf[offset : offset + 4])[0]
            data = bytes(shm.buf[offset + 4 : offset + 4 + length])

            # Clear flag and process
            shm.buf[offset + 4 + 65535] = 0
            decode_udp(data, length)
            read_idx = (read_idx + 1) % (shared_memory_size // slot_size)
        else:
            time.sleep(0.01)  # Backoff when empty


def decode_udp(packet: bytes, length: int):
    header = udp_protocol.Header.decode(packet)
    match length:
        case 1349:
            values = udp_protocol.MotionPacket.decode(packet)
        case 753:
            values = udp_protocol.SessionPacket.decode(packet)
        case 1285:
            values = udp_protocol.LapdataPacket.decode(packet)
        case 45:
            values = udp_protocol.EventPacket.decode(packet)
        case 1284:
            values = udp_protocol.ParticipantsPacket.decode(packet)
        case 1133:
            values = udp_protocol.SetupPacket.decode(packet)
        case 1352:
            values = udp_protocol.TelemetryPacket.decode(packet)
        case 1239:
            values = udp_protocol.StatusPacket.decode(packet)
        case 1042:
            values = udp_protocol.ClassificationPacket.decode(packet)
        case 954:
            values = udp_protocol.LobbyPacket.decode(packet)
        case 1041:
            values = udp_protocol.DamagePacket.decode(packet)
        case 1460:
            values = udp_protocol.SessionHistoryPacket.decode(packet)
        case 231:
            values = udp_protocol.TyreSetsPacket.decode(packet)
        case 273:
            values = udp_protocol.TyreSetsPacket.decode(packet)
        case 101:
            values = udp_protocol.TimeTrialPacket.decode(packet)
        case 1131:
            values = udp_protocol.TimeTrialPacket.decode(packet)
        case _:
            values = None

    print(header)


if __name__ == "__main__":
    receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver.start()

    decoder = Process(target=process_named_shared_memory, daemon=True)
    decoder.start()
    decoder.join()
