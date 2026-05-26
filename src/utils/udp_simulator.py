#!/usr/bin/env python

import ast
import struct
import time
from multiprocessing import shared_memory
from pathlib import Path

from loguru import logger


def udp_receiver(
    rate_hz: int = 20,
    file_path: str = "tests/race.log",
    shared_memory_name: str = "udp_queue",
    shared_memory_size: int = 100 * 1024 * 1024,
):
    # Create named shared memory visible to other programs
    try:
        shm = shared_memory.SharedMemory(
            create=True,
            size=shared_memory_size,
            name=shared_memory_name,
        )
    except FileExistsError:
        shm = shared_memory.SharedMemory(
            create=False,
            size=shared_memory_size,
            name=shared_memory_name,
        )
        shm.unlink()
        shm = shared_memory.SharedMemory(
            create=True,
            size=shared_memory_size,
            name=shared_memory_name,
        )

    # slot: [length:4][data:65535 bytes region][ready_flag:1]
    slot_size = 65535 + 9
    max_slots = shared_memory_size // slot_size
    write_idx = 0

    p = Path(file_path)
    if not p.exists():
        logger.error("File not found: {}", file_path)
        # Close shared memory handle and exit cleanly
        shm.close()
        return

    if rate_hz <= 0:
        logger.error("rate_hz must be > 0")
        shm.close()
        return

    period = 1.0 / rate_hz

    logger.info(
        "Streaming file '{}' at {} Hz into shared memory '{}' ({} bytes)",
        file_path,
        rate_hz,
        shared_memory_name,
        shared_memory_size,
    )

    try:
        while True:
            with p.open("r") as fh:
                next_time = time.perf_counter()
                for line_no, raw_line in enumerate(fh, start=1):
                    # Rate limiting: wait until next scheduled time
                    now = time.perf_counter()
                    sleep_for = next_time - now
                    if sleep_for > 0:
                        time.sleep(sleep_for)
                    else:
                        # If we're late, proceed immediately (do not accumulate drift)
                        next_time = now

                    data_bytes = ast.literal_eval(raw_line)
                    logger.trace(data_bytes)

                    # Truncate if larger than slot capacity (65535)
                    if len(data_bytes) > 65535:
                        logger.warning(
                            "Line {} longer than 65535 bytes; truncating",
                            line_no,
                        )
                        data_bytes = data_bytes[:65535]

                    offset = write_idx * slot_size

                    # Write atomically: length (4 bytes) + data + ready flag at fixed position
                    shm.buf[offset : offset + 4] = struct.pack("I", len(data_bytes))
                    shm.buf[offset + 4 : offset + 4 + len(data_bytes)] = data_bytes

                    # Zero out any leftover bytes in the data region to avoid leaking previous content.
                    data_region_end = offset + 4 + 65535
                    data_written_end = offset + 4 + len(data_bytes)
                    if data_written_end < data_region_end:
                        shm.buf[data_written_end:data_region_end] = b"\x00" * (
                            data_region_end - data_written_end
                        )

                    # Ready flag at fixed position (same as original): offset + 4 + 65535
                    shm.buf[offset + 4 + 65535] = 1

                    logger.debug(
                        "Wrote line {} ({} bytes) to slot {}",
                        line_no,
                        len(data_bytes),
                        write_idx,
                    )

                    write_idx = (write_idx + 1) % max_slots

                    # Schedule next emission time
                    next_time += period

            # Reached EOF
            logger.info("Reached EOF of '{}'; exiting", file_path)

    except KeyboardInterrupt:
        logger.info("Interrupted by user, exiting")
    finally:
        # Do not unlink shared memory so other processes can keep reading
        shm.close()
        logger.info("Closed shared memory")
