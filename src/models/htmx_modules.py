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


### ----------------- ###
### --- TEMPLATES --- ###
### ----------------- ###
def full_card(replace: str) -> Html:
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
            cls="card w-100 h-100 d-flex justify-content-center align-items-center border-warning border-5 rounded-5 bg-transparent",
            style="position: fixed; top: 0; left: 0;",
        ),
    )


### --------------- ###
### --- MODULES --- ###
### --------------- ###
def laps_module() -> Html:
    return full_card("laps_completed_string")


def position_module() -> Html:
    return full_card("position_string")


def car_behind_module() -> Html:
    return full_card("behind_string")


def car_ahead_module() -> Html:
    return full_card("infront_string")


def fastest_lap_module() -> Html:
    return full_card("fastest_lap_string")
