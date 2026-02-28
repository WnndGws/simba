#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import rich
from rich.layout import Layout
from rich.panel import Panel


def create_race_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header_upper"),
        Layout(name="header_lower"),
        Layout(name="body"),
        Layout(name="footer"),
    )

    layout["header_upper"].ratio = 1
    layout["header_lower"].ratio = 2
    layout["body"].ratio = 8
    layout["footer"].ratio = 3

    layout["header_upper"].split_row(
        Layout(name="position"), Layout(name="track"), Layout(name="lap")
    )
    layout["header_lower"].split_row(
        Layout(name="position"), Layout(name="track"), Layout(name="lap")
    )

    layout["body"].split_row(Layout(name="left"), Layout(name="right"))
    layout["body"]["left"].split_column(
        Layout(name="driver_ahead"), Layout(name="driver_behind")
    )
    layout["body"]["right"].split_column(
        Layout(name="current_lap"),
        Layout(name="my_best_lap"),
        Layout(name="session_best"),
    )

    layout["footer"].split_row(
        Layout(name="pit_info"),
        Layout(name="available_tyres"),
        Layout(name="tyre_temp"),
        Layout(name="tyre_deg"),
    )

    layout["footer"]["available_tyres"].split_row(Layout(name="r1"), Layout(name="r2"))
    layout["footer"]["available_tyres"]["r1"].split_column(
        Layout(name="soft"), Layout(name="hard")
    )
    layout["footer"]["available_tyres"]["r2"].split_column(
        Layout(name="medium"), Layout(name="inter")
    )

    layout["footer"]["tyre_temp"].split_row(Layout(name="front"), Layout(name="rear"))
    layout["footer"]["tyre_temp"]["front"].split_column(
        Layout(name="left"), Layout(name="right")
    )
    layout["footer"]["tyre_temp"]["rear"].split_column(
        Layout(name="left"), Layout(name="right")
    )

    layout["footer"]["tyre_deg"].split_row(Layout(name="front"), Layout(name="rear"))
    layout["footer"]["tyre_deg"]["front"].split_column(
        Layout(name="left"), Layout(name="right")
    )
    layout["footer"]["tyre_deg"]["rear"].split_column(
        Layout(name="left"), Layout(name="right")
    )

    layout["header_upper"]["position"].ratio = 1
    layout["header_upper"]["track"].ratio = 2
    layout["header_upper"]["lap"].ratio = 1

    layout["header_lower"]["lap"].split_row(
        Layout(name="completed_laps"), Layout(name="total_laps")
    )

    layout["header_lower"]["position"].ratio = 1
    layout["header_lower"]["track"].ratio = 2
    layout["header_lower"]["lap"].ratio = 1

    layout["header_upper"]["position"].update(
        Panel(
            rich.text.Text("POSITION", justify="center"),
            box=rich.box.HEAVY_EDGE,
            style=rich.style.Style(bold=True),
        )
    )
    layout["header_upper"]["track"].update(
        Panel(
            rich.text.Text("", justify="center"),
            box=rich.box.HEAVY_EDGE,
            style=rich.style.Style(bold=True),
        )
    )
    layout["header_upper"]["lap"].update(
        Panel(
            rich.text.Text("LAP", justify="center"),
            box=rich.box.HEAVY_EDGE,
            style=rich.style.Style(bold=True),
        )
    )

    return layout
