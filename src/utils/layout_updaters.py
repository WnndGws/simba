#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import rich
from rich.panel import Panel

from config import shared_variables
from models import decode_dictionaries
from utils import prettyfy


def update_using_motion(layout, shared):
    # Header 0
    pass


def update_using_session(layout, shared):
    # Header 1

    total_laps_string, track_string, pit_string = prettyfy.prettyfy_session(shared)

    layout["header_upper"]["track"].update(
        Panel(
            rich.text.Text(
                track_string,
                justify="center",
            )
        )
    )

    layout["header_lower"]["lap"]["total_laps"].update(
        Panel(
            rich.text.Text(
                total_laps_string,
                justify="left",
            )
        )
    )
    layout["footer"]["pit_info"].update(
        Panel(
            rich.text.Text(
                pit_string,
                justify="left",
            )
        )
    )


def update_using_lapdata(layout, shared):
    # Header 2
    (
        position_string,
        infront_string,
        behind_string,
        laps_string,
        current_lap_time_string,
        best_lap_string,
        fastest_lap_string,
        track_position,
    ) = prettyfy.prettyfy_lapdata(shared)

    layout["header_lower"]["position"].update(
        Panel(
            rich.text.Text(
                position_string,
                justify="center",
            )
        )
    )

    layout["header_lower"]["lap"]["completed_laps"].update(
        Panel(
            rich.text.Text(
                laps_string,
                justify="right",
            )
        )
    )

    layout["header_lower"]["track"].update(
        Panel(
            rich.text.Text(
                track_position,
                justify="center",
            )
        )
    )

    # comment out to get drs positions
    """
    layout["body"]["driver_ahead"].update(
        Panel(
            rich.text.Text(
                infront_string,
                justify="center",
            )
        )
    )

    layout["body"]["driver_behind"].update(
        Panel(
            rich.text.Text(
                behind_string,
                justify="center",
            )
        )
    )
    """

    layout["body"]["right"]["current_lap"].update(
        Panel(
            rich.text.Text(
                current_lap_time_string,
                justify="center",
            )
        )
    )

    layout["body"]["right"]["my_best_lap"].update(
        Panel(
            rich.text.Text(
                best_lap_string,
                justify="center",
            )
        )
    )

    layout["body"]["right"]["session_best"].update(
        Panel(
            rich.text.Text(
                fastest_lap_string,
                justify="center",
            )
        )
    )


def update_using_event(layout, shared):
    # Header 3
    text = prettyfy.prettyfy_event(shared)


def update_using_participants(layout, shared):
    # Header 4
    pass


def update_using_setup(item_values, shared):
    # Header 5
    pass


def update_using_telemetry(layout, shared):
    # Header 6

    rl, rr, fl, fr = prettyfy.prettyfy_telemetry(shared)

    layout["footer"]["tyre_temp"]["front"]["left"].update(
        Panel(
            rich.text.Text(
                fl,
                justify="center",
            )
        )
    )

    layout["footer"]["tyre_temp"]["front"]["right"].update(
        Panel(
            rich.text.Text(
                fr,
                justify="center",
            )
        )
    )

    layout["footer"]["tyre_temp"]["rear"]["left"].update(
        Panel(
            rich.text.Text(
                rl,
                justify="center",
            )
        )
    )

    layout["footer"]["tyre_temp"]["rear"]["right"].update(
        Panel(
            rich.text.Text(
                rr,
                justify="center",
            )
        )
    )


def update_using_status(layout, shared):
    # Header 7
    pass


def update_using_classification(layout, shared):
    # Header 8
    pass


def update_using_lobby(layout, shared):
    # Header 9
    pass


def update_using_damage(layout, shared):
    # Header 10
    rl, rr, fl, fr = prettyfy.prettyfy_damage(shared)

    layout["footer"]["tyre_deg"]["front"]["left"].update(
        Panel(
            rich.text.Text(
                fl,
                justify="center",
            )
        )
    )

    layout["footer"]["tyre_deg"]["front"]["right"].update(
        Panel(
            rich.text.Text(
                fr,
                justify="center",
            )
        )
    )

    layout["footer"]["tyre_deg"]["rear"]["left"].update(
        Panel(
            rich.text.Text(
                rl,
                justify="center",
            )
        )
    )

    layout["footer"]["tyre_deg"]["rear"]["right"].update(
        Panel(
            rich.text.Text(
                rr,
                justify="center",
            )
        )
    )


def update_using_history(layout, shared):
    # Header 11
    pass


def update_using_available_tyres(layout, shared):
    # Header 12

    softs, mediums, hards, inters = prettyfy.prettyfy_tyres(shared)

    layout["footer"]["available_tyres"]["r1"]["soft"].update(
        Panel(
            rich.text.Text(
                softs,
                justify="center",
            )
        )
    )

    layout["footer"]["available_tyres"]["r1"]["hard"].update(
        Panel(
            rich.text.Text(
                hards,
                justify="center",
            )
        )
    )

    layout["footer"]["available_tyres"]["r2"]["medium"].update(
        Panel(
            rich.text.Text(
                mediums,
                justify="center",
            )
        )
    )

    layout["footer"]["available_tyres"]["r2"]["inter"].update(
        Panel(
            rich.text.Text(
                inters,
                justify="center",
            )
        )
    )


def update_using_extended_motion(layout, shared):
    # Header 13
    pass


def update_using_time_trial(layout, shared):
    # Header 14
    pass


def update_using_position_history(layout, shared):
    # Header 15
    pass
