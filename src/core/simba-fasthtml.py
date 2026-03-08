#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import asyncio
import multiprocessing as mp
import os
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Flag
from multiprocessing import shared_memory as mp_shared_memory
from pathlib import Path

from fasthtml.common import Div, serve, signal_shutdown
from loguru import logger
from sse_starlette import EventSourceResponse

from config import shared_variables as shared
from models import htmx_modules
from utils import process_data, udp_processor, udp_receiver

### ----------------------------- ###
### --- CONSTANTS and GLOBALS --- ###
### ----------------------------- ###
basedir = Path(__file__).parent.parent.resolve()

app, rt = htmx_modules.build_constants()

# Globals for queues and worker processes
shutdown_event = signal_shutdown()
task_queue = asyncio.Queue()
results_queue = asyncio.Queue()
item_queue = mp.Queue()

receiver_proc = None
producer_proc = None


### --------------- ###
### --- HELPERS --- ###
### --------------- ###
def _cleanup_leftover_shared_memory(name="udp_queue"):
    try:
        existing = mp_shared_memory.SharedMemory(name=name)
    except FileNotFoundError:
        return
    except Exception:
        return

    try:
        existing.close()
        existing.unlink()
    except Exception as e:
        logger.warning("Failed to unlink leftover shared memory %s: %s", name, e)


def start_queues():
    global receiver_proc, producer_proc

    # Attempt to remove leftover shared memory from previous runs
    _cleanup_leftover_shared_memory("udp_queue")

    # Start UDP receiver as a daemon
    receiver_proc = mp.Process(target=udp_receiver.udp_receiver, daemon=True)
    receiver_proc.start()

    # Wait for the receiver to create the named shared memory region so the processor can open it
    for _ in range(200):
        try:
            shm = mp_shared_memory.SharedMemory(name="udp_queue")
            shm.close()
            break
        except FileNotFoundError:
            time.sleep(0.01)
    else:
        logger.warning(
            "Shared memory 'udp_queue' did not appear after starting receiver"
        )

    # Start the shared-memory reader process
    producer_proc = mp.Process(
        target=udp_processor.process_named_shared_memory,
        args=(item_queue,),
        daemon=True,
    )
    producer_proc.start()
    logger.info(
        "Started receiver PID=%s producer PID=%s",
        getattr(receiver_proc, "pid", None),
        getattr(producer_proc, "pid", None),
    )


def stop_queues():
    global receiver_proc, producer_proc

    # Signal consumer to stop
    try:
        item_queue.put_nowait((None, None))
    except Exception:
        pass

    # Terminate child processes
    for p in (producer_proc, receiver_proc):
        if p is None:
            continue
        try:
            if p.is_alive():
                p.terminate()
                p.join(timeout=2)
        except Exception as e:
            logger.warning("Error terminating process %s: %s", p, e)

    # Attempt to cleanup shared memory
    _cleanup_leftover_shared_memory("udp_queue")


try:
    app.add_event_handler("startup", start_queues)
    app.add_event_handler("shutdown", stop_queues)
except Exception:
    logger.debug(
        "Could not register event handlers. Check start_queues() is invoked in the process that runs the server"
    )


class SessionCombos(Flag):
    PRACTICE = 1  # 0b001
    QUALIFYING = 2  # 0b010
    RACE = 4  # 0b100


def return_module_for_session_types(module: str, enum_code: int) -> str:
    combos = SessionCombos(enum_code)
    session_type = shared.session_type_cache

    sessions_wanted = [255]
    if SessionCombos.PRACTICE in combos:
        sessions_wanted.append([1, 2, 3, 4, 18])
    if SessionCombos.QUALIFYING in combos:
        sessions_wanted.append(range(5, 14))
    if SessionCombos.RACE in combos:
        sessions_wanted.append(range(15, 17))

    if session_type in sessions_wanted:
        return Div(
            Div(
                Div(module),
                hx_ext="sse",
                sse_connect="/stream",
            ),
            style="background-color: #000;",
        )

    return None


### ------------------------- ###
### --- FastHTML and HTMX --- ###
### ------------------------- ###
async def get_stream():
    # No need to overkill
    cpu = os.cpu_count() or 2
    max_workers = int(min(4, max(2, cpu // 2)))
    worker_executor = ThreadPoolExecutor(max_workers=max_workers)
    loop = asyncio.get_running_loop()

    async def process_incoming_udp():
        while True:
            header_values = await loop.run_in_executor(None, item_queue.get)
            header, values = header_values

            # request shutdown
            if header is None and values is None:
                for _ in range(max_workers):
                    await task_queue.put(None)
                await results_queue.put(None)
                break

            if shared.session_cache == 255:
                process_data.process_initial_data(header, values, shared, task_queue)
            else:
                process_data.process_data(header, values, shared, task_queue)
            await asyncio.sleep(0)

    async def worker_loop(worker_id: int):
        while True:
            callable_obj = await task_queue.get()
            if callable_obj is None:
                break
            try:
                result = await loop.run_in_executor(worker_executor, callable_obj)
                if result is None:
                    continue
                if isinstance(result, list):
                    for k, v in result:
                        await results_queue.put({"event": k, "data": v})
                else:
                    k, v = result
                    await results_queue.put({"event": k, "data": v})
            except Exception:
                logger.exception("Worker failed to process callable")

    producer_task = asyncio.create_task(process_incoming_udp())
    worker_tasks = [asyncio.create_task(worker_loop(i)) for i in range(max_workers)]

    try:
        while True:
            payload = await results_queue.get()
            if payload is None:
                break
            yield payload
    finally:
        if "producer_task" in locals() and not producer_task.done():
            try:
                producer_task.cancel()
            except Exception:
                pass

        try:
            await asyncio.gather(*worker_tasks, return_exceptions=True)
        except Exception:
            pass

        try:
            worker_executor.shutdown(wait=True)
        except Exception:
            pass


### ----------------- ###
### --- ENDPOINTS --- ###
### ----------------- ###
@rt
async def stream():
    return EventSourceResponse(get_stream())


@rt
def laps():
    return return_module_for_session_types(htmx_modules.laps_module(), 3)


@rt
def car_behind():
    return return_module_for_session_types(htmx_modules.car_behind_module(), 3)


@rt
def car_ahead():
    return return_module_for_session_types(htmx_modules.car_ahead_module(), 3)


@rt
def position():
    return return_module_for_session_types(htmx_modules.position_module(), 3)


@rt
def fastest_lap():
    return return_module_for_session_types(htmx_modules.fastest_lap_module(), 3)


serve()
