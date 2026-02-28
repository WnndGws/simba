#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import ast
import random
from pathlib import Path

import pytest

from config import shared_variables as shared
from models import decode_dictionaries, rich_layout
from utils import layout_updaters, prepare_data_for_layouts, udp_processor, udp_receiver


# Assuming the file is a pickle file containing a list of (length, byte-data) tuples
def load_test_data(filepath: str, sample_size: int = 500) -> list:
    all_data = []
    with Path.open(filepath, "r") as f:
        for line in f:
            line.strip()
            if line:
                all_data.append(ast.literal_eval(line))

    return random.sample(all_data, sample_size)


# Parametrize the test with 500 random samples
@pytest.mark.sq
@pytest.mark.parametrize("length,packet", load_test_data("sprint_quali.log"))
def test_prettify_sprint_quali(length: int, packet: bytes):
    header, data = udp_processor.decode_udp(packet, length)

    assert header.packet_id in range(16)
    prepare_data_for_layouts.prettify_header(header, shared)
    assert shared.Static.player_idx == 3

    if header.packet_id == 1:
        prepare_data_for_layouts.prettify_session(data, shared)

        assert shared.Static.session_cache_count == 1
        assert shared.Static.track_id == 2
        assert shared.Static.track_length_m == 5441
        assert shared.Static.track_string == "Shanghai"
        assert shared.Static.total_lap_string == "/1"
        assert shared.Static.session_type in [10, 11]
        assert shared.Static.sector_distances == [0, 1417, 2984, 5441]

    if header.packet_id == 2:
        pretty = prepare_data_for_layouts.prettify_lapdata(data, shared)

        # unknown grid position
        assert pretty[1] == 0

        # lap number
        assert pretty[2] in [1, 2]
        # sector
        assert pretty[3] in decode_dictionaries.sector_dict


@pytest.mark.rq
@pytest.mark.parametrize("length,packet", load_test_data("quali.log"))
def test_prettify_quali(length: int, packet: bytes):
    header, data = udp_processor.decode_udp(packet, length)

    assert header.packet_id in range(16)
    prepare_data_for_layouts.prettify_header(header, shared)
    assert shared.Static.player_idx == 3


@pytest.mark.rr
@pytest.mark.parametrize("length,packet", load_test_data("race.log"))
def test_prettify_race(length: int, packet: bytes):
    header, data = udp_processor.decode_udp(packet, length)

    assert header.packet_id in range(16)
    prepare_data_for_layouts.prettify_header(header, shared)
    assert shared.Static.player_idx == 3

    if header.packet_id == 1:
        prepare_data_for_layouts.prettify_session(data, shared)

        assert shared.Static.session_cache_count == 1
        assert shared.Static.track_id == 2
        assert shared.Static.track_length_m == 5441
        assert shared.Static.track_string == "Shanghai"
        assert shared.Static.total_lap_string == "/14"
        assert shared.Static.session_type == 16
        assert shared.Static.sector_distances == [0, 1417, 2984, 5441]

    if header.packet_id == 2:
        pretty = prepare_data_for_layouts.prettify_lapdata(data, shared)

        # grid position
        assert pretty[1] == 20
        # lap number
        assert pretty[2] in [1, 2, 3]
        # sector
        assert pretty[3] in decode_dictionaries.sector_dict
