#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from fasthtml.common import (
    H1,
    H2,
    H3,
    H4,
    H5,
    Div,
    Html,
    Link,
    P,
    Script,
    Span,
    fast_app,
)


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###
def build_constants():
    htmx_sse = Script(src="https://unpkg.com/htmx-ext-sse@2.2.3/sse.js")
    bootstrap_script = Script(
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
    )
    bootstrap_stylesheet = Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
    )
    nerdfont_stylesheet = Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css",
    )
    app, rt = fast_app(
        live=False,
        hdrs=(htmx_sse, bootstrap_stylesheet, bootstrap_script, nerdfont_stylesheet),
    )

    return app, rt


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###
def top_bar_item(replace: str):
    return Html(
        Div(
            Div(
                P(
                    Span(
                        cls="card-text spinner-border text-warning", hx_swap_oob="true"
                    ),
                    Span(cls="card-text align-text-center"),
                    sse_swap=replace,
                    hx_target="this",
                ),
                cls="card-body fs-4 align-items-center justify-content-center text-center",
            ),
            cls="col card border-warning border-5 rounded-5",
            style="background-color: #000",
        ),
    )


def compose_top_bar():
    return Div(
        Div(
            top_bar_item("position_string"),
            top_bar_item("track_string"),
            top_bar_item("laps_completed_string"),
            cls="row g-0",
        ),
        cls="container-fluid overflow-hidden h-100",
        style="height: 15vh; background-color; #000",
    )


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###
def drivers_item(replace: str):
    return Html(
        Div(
            Div(
                P(
                    Span(
                        cls="card-text spinner-border text-warning", hx_swap_oob="true"
                    ),
                    Span(cls="card-text align-text-center"),
                    sse_swap=replace,
                    hx_target="this",
                ),
                cls="card-body g-0 fs-4 align-items-center justify-content-center text-center",
            ),
            cls="row card border-warning border-5 rounded-5 g-0",
            style="background-color: #000",
        ),
    )


def compose_middle_body():
    return Div(
        Div(
            # First column with 3 rows
            Div(
                Div(
                    drivers_item("infront_string"),
                    drivers_item("behind_string"),
                    cls="row g-0 h-100",
                ),
                cls="col-6 h-100 g-0",  # Left column: 6/12 width, contains 2 rows
            ),
            # Second column with 2 rows
            Div(
                Div(
                    drivers_item("current_lap_time_string"),
                    drivers_item("player_best_lap_time_string"),
                    drivers_item("session_fastest_lap_time_string"),
                    cls="row g-0 h-100",
                ),
                cls="col-6 h-100 g-0",  # Right column: 6/12 width, contains 3 rows
            ),
            cls="row h-100 g-0",  # Outer row
        ),
        cls="container-fluid overflow-hidden",
        style="height: 50vh;",
    )


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###


### -------------------------------------------------------------------------------- ###
### -------------------------------------------------------------------------------- ###
def single_tyre(replace: str):
    return Html(
        Div(
            Div(
                P(
                    Span(
                        cls="card-text spinner-border text-warning", hx_swap_oob="true"
                    ),
                    Span(cls="card-text m-0"),
                    sse_swap=replace,
                    hx_target="this",
                ),
                cls="card-body d-flex align-items-center justify-content-center flex-column g-0 fs-3 text-center",
            ),
            cls="col card bg-secondary rounded-circle border-5 border-warning g-0 h-100 overflow-hidden",
            style="aspect-ratio: 1/1;background-color: #000;",
        ),
    )


def bottom_item(replace: str):
    return Html(
        Div(
            Div(
                P(
                    Span(
                        cls="card-text spinner-border text-warning", hx_swap_oob="true"
                    ),
                    Span(cls="card-text align-text-center"),
                    sse_swap=replace,
                    hx_target="this",
                ),
                cls="card-body g-0 fs-4 align-items-center justify-content-center text-center",
            ),
            cls="col h-100 card border-warning border-5 rounded-5 g-0",
            style="background-color: #000",
        ),
    )


def compose_bottom_body():
    return Div(
        # outer container: two groups side-by-side
        Div(
            # left group (vehicle tyres) as a 2x2 grid
            Div(
                single_tyre("front_left_wear_string"),
                single_tyre("front_right_wear_string"),
                single_tyre("rear_left_wear_string"),
                single_tyre("rear_right_wear_string"),
                cls="d-grid card border-5 border-success",
                style=(
                    # set each column to 1/2 of the containers height
                    "grid-template-columns: repeat(2, 17.5vh); "
                    "grid-template-rows: repeat(2, 50%); "
                    # same thing here, width is determined by container height actually
                    "height: 100%; width: 17.5%; "
                    "align-items: center; justify-items: center; "
                    "background-color: #000;"
                ),
            ),
            Div(bottom_item("pit_string"), style="height: 100%; width: 17.5%; "),
            Div(bottom_item("gap_string"), style="height: 100%; width: 17.5%; "),
            # layout the two groups side-by-side and center them vertically
            cls="d-flex",
            style="height: 100%; align-items: center; justify-content: center; width: 100%;",
        ),
        cls="container-fluid overflow-hidden",
        style="height: 35vh;",
    )
