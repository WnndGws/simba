#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import multiprocessing
import time

import rich
from loguru import logger
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.logging import RichHandler
from rich.table import Table

from models import classes, constants
from utils import udp_filter


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


def generate_session_table(data, fields=None) -> Table:
    table = Table()
    table.add_column()
    table.add_column("Info")

    if fields is None:
        fields = [field_name for field_name, _ in classes.SessionData._fields_]

    for field_name in fields:
        field_value = getattr(data, field_name)
        if field_value is not None:
            try:
                k, v = constants.display_data(field_name, field_value)
                table.add_row(k, v)
            # if the filed isnt in the dict
            except TypeError:
                pass

    return table


def main():
    raw_queue = multiprocessing.Queue()

    state = udp_filter.get_shared_state()
    udp_filter.start_udp_queue(raw_queue)

    console = Console()
    layout = make_layout()

    table_01_contents = [
        "weather",
        "track_temp_c",
        "air_temp_c",
        "total_race_laps",
        "session_type",
        "track_id",
        "formula",
        "session_time_remaining_seconds",
        "session_duration_seconds",
        "drs_status",
    ]

    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            if not raw_queue.empty():
                data = raw_queue.get()
                udp_filter.decode_packets(data)
            else:
                time.sleep(0.1)
            layout["body"].update(
                generate_session_table(state.session_data, table_01_contents)
            )


if __name__ == "__main__":
    main()
