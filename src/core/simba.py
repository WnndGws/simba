#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import multiprocessing
import sys
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


def generate_player_table(data, fields=None) -> Table:
    two_players = False

    table = Table()
    table.add_column()
    table.add_column("WG")
    player1 = data[0]
    player1_minus_one = data[1]
    player1_plus_one = data[2]
    player2 = data[3]
    player2_minus_one = data[4]
    player2_plus_one = data[5]

    if player2.car_position != None:
        two_players = True

    try:
        # Convert all to ms
        player1.delta_to_car_behind_ms = (
            player1.delta_to_leader_ms_component
            - player1_plus_one.delta_to_leader_ms_component
        ) * -1
    # when they are still None
    except TypeError:
        player1.delta_to_car_behind_ms = None

    # Second Player
    if two_players:
        table.add_column("SG")
        try:
            # Convert all to ms
            player2.delta_to_car_behind_ms = (
                player2.delta_to_leader_ms_component
                - player2_plus_one.delta_to_leader_ms_component
            ) * -1
        except TypeError:
            player2.delta_to_car_behind_ms = None

    if fields is None:
        rich.print("Please state fields for the car table")
        sys.exit()

    for field_name in fields:
        field_value1 = getattr(player1, field_name)
        if two_players:
            field_value2 = getattr(player2, field_name)
        if field_value1 is not None:
            try:
                k1, v1 = constants.display_data(field_name, field_value1)
                if two_players:
                    k2, v2 = constants.display_data(field_name, field_value2)
                    table.add_row(k1, v1, v2)
                else:
                    table.add_row(k1, v1, None)
            # if the filed isnt in the dict
            except TypeError:
                rich.print(f"Create 'display_data' entry for {field_name} and rerun...")
                sys.exit()

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

    table_02_contents = [
        "car_position",
        "grid_position",
        "delta_to_car_in_front_ms_component",
        "delta_to_car_behind_ms",
        "delta_to_leader_ms_component",
    ]

    combined_contents = table_01_contents + table_02_contents

    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            if not raw_queue.empty():
                data = raw_queue.get()
                udp_filter.decode_packets(data, combined_contents)
            else:
                time.sleep(0.1)
            layout["box1"].update(
                generate_session_table(state.session_data, table_01_contents)
            )
            layout["body"].update(
                generate_player_table(state.surrounding_cars_data, table_02_contents)
            )


if __name__ == "__main__":
    main()
