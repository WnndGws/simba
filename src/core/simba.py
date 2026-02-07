#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import dataclasses
import multiprocessing
import sys
import time

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.logging import RichHandler
from rich.table import Table

from models import classes, constants
from utils import create_dataclasses, udp_filter


def make_layout():
    """Define the layout."""
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    layout["side"].split(Layout(name="box1"), Layout(name="box2"))
    return layout


def generate_session_table(
    session_queue,
    stop_event: multiprocessing.synchronize.Event | None = None,
) -> Table:
    table = Table()
    table.add_column()
    table.add_column("Info")

    # Continue until stopped
    if stop_event is None:
        stop_event = multiprocessing.Event()

    while not stop_event.is_set():
        try:
            data = session_queue.get(timeout=0.2)
            for field in data.fields():
                value = str(getattr(data, field.name))
                table.add_row(field.name, value)
        except:
            pass

    return table


def main():
    multiprocessing.set_start_method("spawn", force=True)
    raw_queue = multiprocessing.Queue()
    decoded_queue = multiprocessing.Queue()
    session_queue = multiprocessing.Queue()
    lap_queue = multiprocessing.Queue()
    terminate = multiprocessing.Event()

    session_info = classes.SessionInfo()
    p1_info = classes.PlayerInfo()
    p2_info = classes.PlayerInfo()

    num_workers = int(multiprocessing.cpu_count() / 2)
    decode_posse = []

    for _ in range(num_workers):
        decode_worker_process = multiprocessing.Process(
            target=udp_filter.decode_worker,
            args=(raw_queue, decoded_queue, terminate),
            daemon=True,
            name=f"comrade_worker_{_ + 1}",
        )
        decode_posse.append(decode_worker_process)
        decode_worker_process.start()

    udp_filter.start_udp_queue(raw_queue)

    multiprocessing.Process(
        target=create_dataclasses.udp_to_class_info,
        args=(decoded_queue, session_queue, session_info, p1_info, p2_info),
        daemon=True,
    )

    console = Console()
    layout = make_layout()

    while True:
        layout["box1"].update(generate_session_table(session_queue))
        console.print(layout)
        time.sleep(1)

    # Wait for workers to finish
    for comrade in decode_posse:
        comrade.join()


if __name__ == "__main__":
    main()
