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
from utils import udp_collector, udp_receiver


async def async_process_named_shared_memory(
    output_queue: asyncio.Queue,
    shared_memory_name: str = "udp_queue",
    shared_memory_size: int = 100 * 1024 * 1024,
    poll_delay: float = 0.01,
):
    # the same as synchronous until snapshot
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

                # Global dicts used in udp_collector updated and readable
                decode_udp(data, length)

                # publish snapshot (deep copy to avoid races)
                snapshot = {
                    "session": copy.deepcopy(udp_collector.collected_session),
                    "player_cars": copy.deepcopy(udp_collector.collected_player_cars),
                    "ai_cars": copy.deepcopy(udp_collector.collected_ai_cars),
                }

                # best-effort publish; if queue is full drop (non-blocking)
                try:
                    publish_queue.put_nowait(snapshot)
                except asyncio.QueueFull:
                    # backpressure policy: drop this snapshot
                    pass

                read_idx = (read_idx + 1) % max_slots
            else:
                await asyncio.sleep(poll_delay)
        except asyncio.CancelledError:
            # Called on shutdown
            pass
        finally:
            try:
                shm.close()
            except Exception:
                pass


def synchronously_process_named_shared_memory(
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
    udp_collector.handle_header(packet)
    match length:
        case 1349:
            udp_collector.handle_motion(packet)
        case 753:
            udp_collector.handle_session(packet)
        case 1285:
            udp_collector.handle_lapdata(packet)
        case 45:
            udp_collector.handle_event(packet)
        case 1284:
            udp_collector.handle_participants(packet)
        case 1133:
            udp_collector.handle_setups(packet)
        case 1352:
            udp_collector.handle_telemetry(packet)
        case 1239:
            udp_collector.handle_status(packet)
        case 1042:
            udp_collector.handle_classification(packet)
        case 954:
            udp_collector.handle_lobby(packet)
        case 1041:
            udp_collector.handle_damage(packet)
        case 1460:
            udp_collector.handle_sessionhistory(packet)
        case 231:
            udp_collector.handle_tyresets(packet)
        case 273:
            udp_collector.handle_exmotion(packet)
        case 101:
            pass
        case 1131:
            udp_collector.handle_positionhistory(packet)
        case _:
            pass


if __name__ == "__main__":
    receiver = Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver.start()

    queue = Queue()
    process_named_shared_memory(output_queue=queue)
