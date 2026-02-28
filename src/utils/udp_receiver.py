#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
"""

"""Receives the flood of UDP packets and sends them to where they need to go
ie sends them to shared memory"""

import socket
import struct
import sys
from multiprocessing import shared_memory

from loguru import logger
from rich.logging import RichHandler

# Setup logger with RichHandler for better output
logger.remove()
logger.add(
    sys.stderr,
)
logger.configure(
    handlers=[
        {"sink": "udp.log", "level": "WARNING"},
        {
            "sink": RichHandler(
                rich_tracebacks=True, show_path=True, tracebacks_show_locals=True
            ),
            "level": "INFO",
        },
    ]
)


def udp_receiver(
    port: int = 20127,
    ip: str = "0.0.0.0",
    shared_memory_name: str = "udp_queue",
    shared_memory_size: int = 100 * 1024 * 1024,
):
    # Create named shared memory visible to other programs
    shm = shared_memory.SharedMemory(
        create=True, size=shared_memory_size, name=shared_memory_name
    )

    # Without offset, the code could not index into the correct position in the raw byte buffer to store packet metadata and payload separately.
    # Simple header: [offset:4][length:4][ready:1] per packet slot
    slot_size = 65535 + 9
    max_slots = shared_memory_size // slot_size
    write_idx = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16 * 1024 * 1024)
    sock.bind((ip, port))

    while True:
        data, addr = sock.recvfrom(65535)
        offset = write_idx * slot_size

        # Write atomically: length + data + ready flag
        shm.buf[offset : offset + 4] = struct.pack("I", len(data))
        shm.buf[offset + 4 : offset + 4 + len(data)] = data
        shm.buf[offset + 4 + 65535] = 1  # Ready flag

        write_idx = (write_idx + 1) % max_slots
