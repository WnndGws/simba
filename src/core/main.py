#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import asyncio
from multiprocessing import Process, shared_memory

from rich import print

from utils import udp_collector, udp_processor, udp_receiver


def start_udp_receiver_process(
    port: int = 20127,
    ip: str = "0.0.0.0",
    shared_memory_name: str = "udp_queue",
    shared_memory_size: int = 100 * 1024 * 1024,
):
    """Start the existing blocking UDP receiver in a separate process so it can
    keep writing to shared memory.
    """
    receiver_proc = Process(
        target=udp_receiver.udp_receiver,
        kwargs={
            "port": port,
            "ip": ip,
            "shared_memory_name": shared_memory_name,
            "shared_memory_size": shared_memory_size,
        },
        daemon=True,
    )
    receiver_proc.start()
    return receiver_proc


async def start_udp_processor():
    q: asyncio.Queue = asyncio.Queue(maxsize=200)
    start_udp_receiver_process()
    task = asyncio.create_task(udp_processor.async_process_named_shared_memory(q))
    try:
        # simple test consumer: print a tick every snapshot
        while True:
            snap = await q.get()
            print("snapshot tick", list(snap["player_cars"].keys()))
    finally:
        task.cancel()
        await task


if __name__ == "__main__":
    asyncio.run(start_udp_processor())
