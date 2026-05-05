#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from typing import Any

import pytest

from models import udp_protocol
from tests.single_examples import (
    classification_packet_example,
    damage_packet_example,
    event_packet_example,
    exmotion_packet_example,
    lapdata_packet_example,
    motion_packet_example,
    participants_packet_example,
    position_history_packet_example,
    session_history_packet_example,
    session_packet_example,
    setups_packet_example,
    status_packet_example,
    telemetry_packet_example,
    tyre_sets_packet_example,
)


# Helper assertion functions
def assert_instance(obj: Any, tpe: type):
    assert isinstance(obj, tpe), f"Expected instance of {tpe}, got {type(obj)}"


def assert_value(obj: Any, val: Any):
    assert obj == val, f"Expected instance of {obj} == {val}, got {obj} == {val}"


def assert_notvalue(obj: Any, val: Any):
    assert obj != val, f"Expected instance of {obj} != {val}, got {obj} != {val}"


def assert_list_length(lst: list, expected: int, msg: str = ""):
    assert isinstance(lst, list), "Expected a list"
    assert len(lst) == expected, f"{msg} expected length {expected}, got {len(lst)}"


#############
### TESTS ###
#############
def test_motion():
    pkt = motion_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.MotionPacket.decode(pkt)

    assert_value(header.packet_id, 0)
    assert_list_length(packet.cars, 22)
    assert_value(packet.cars[0].roll_radians, 0.000474567583296448)


def test_session():
    pkt = session_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.SessionPacket.decode(pkt)

    assert_value(header.packet_id, 1)
    assert_value(packet.weather, "light cloud")
    assert_value(packet.session_type, "Race 2")
    assert_list_length(packet.list_of_marshal_zones, 21)
    assert_list_length(packet.weather_forecasts, 64)
    assert_value(
        packet.list_of_marshal_zones[
            packet.number_of_marshal_zones
        ].zone_start_at_lap_percentage,
        0.0,
    )
    assert_notvalue(
        packet.list_of_marshal_zones[
            packet.number_of_marshal_zones - 1
        ].zone_start_at_lap_percentage,
        0.0,
    )
    assert_notvalue(packet.list_of_marshal_zones[0].zone_start_at_lap_percentage, 0.0)
    assert_value(packet.sector_2_start_distance_m, 2826)


def test_lapdata():
    pkt = lapdata_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.LapdataPacket.decode(pkt)

    assert_value(header.packet_id, 2)
    assert_list_length(packet.cars, 22)
    assert_value(packet.cars[header.player_car_index].grid_position, 20)


def test_participants():
    pkt = participants_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.ParticipantsPacket.decode(pkt)

    assert_value(header.packet_id, 4)
    assert_list_length(packet.cars, 22)
    assert_value(packet.number_of_active_cars, 20)
    assert_value(packet.cars[header.player_car_index].is_ai_controlled_flag, 0)
    assert_value(packet.cars[header.player_car_index].team_id, "Ferrari")
    assert_value(packet.cars[header.player_car_index].name, "HAMILTON")
    assert_value(packet.cars[header.player_car_index + 1].is_ai_controlled_flag, 1)
    assert_value(packet.cars[header.player_car_index + 1].team_id, "Red Bull Racing")
    assert_value(packet.cars[header.player_car_index + 1].name, "VERSTAPPEN")
    assert_value(packet.cars[packet.number_of_active_cars].is_ai_controlled_flag, 0)
    assert_value(packet.cars[packet.number_of_active_cars].team_id, "N/A")
    assert_value(packet.cars[packet.number_of_active_cars].name, "")


def test_setups():
    pkt = setups_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.SetupPacket.decode(pkt)

    assert_value(header.packet_id, 5)
    assert_list_length(packet.setups, 22)
    assert_value(packet.setups[header.player_car_index].on_throttle, 30)
    assert_value(packet.setups[header.player_car_index + 1].on_throttle, 90)


def test_telemetry():
    pkt = telemetry_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.TelemetryPacket.decode(pkt)

    assert_value(header.packet_id, 6)
    assert_list_length(packet.statuses, 22)
    assert_value(packet.statuses[header.player_car_index].gear, 5)
    assert_value(packet.statuses[header.player_car_index].brake, 0.0)


def test_carstatuses():
    pkt = status_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.StatusPacket.decode(pkt)

    assert_value(header.packet_id, 7)
    assert_list_length(packet.statuses, 22)
    assert_value(packet.statuses[header.player_car_index].drs_allowed, "not allowed")
    assert_value(packet.statuses[header.player_car_index].visual_tyre_compound, "soft")
    assert_value(packet.statuses[header.player_car_index].actual_tyre_compound, "C4")


def test_classification():
    pkt = classification_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.ClassificationPacket.decode(pkt)

    assert_value(header.packet_id, 8)
    assert_list_length(packet.classification, 22)
    assert_value(packet.classification[header.player_car_index].grid_position, 20)
    assert_value(
        packet.classification[header.player_car_index].tyre_stint_1_visual_tyre, "soft"
    )
    assert_value(
        packet.classification[header.player_car_index].tyre_stint_1_actual_tyre, "C4"
    )


def test_damage():
    pkt = damage_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.DamagePacket.decode(pkt)

    assert_value(header.packet_id, 10)
    assert_list_length(packet.statuses, 22)
    assert_value(packet.statuses[header.player_car_index].drs_fault, "OK")
    assert_value(packet.statuses[header.player_car_index].tyre_fr_damage_percentage, 3)


def test_sessionhistory():
    pkt = session_history_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.SessionHistoryPacket.decode(pkt)

    assert_value(header.packet_id, 11)
    assert_list_length(packet.lap_history_data, 100)
    assert_list_length(packet.tyre_history_data, 8)
    assert_value(packet.best_lap_number, 6)
    assert_value(packet.best_s1_lap_number, 6)


def test_tyresets():
    pkt = tyre_sets_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.TyreSetsPacket.decode(pkt)

    assert_value(header.packet_id, 12)
    assert_list_length(packet.tyre_set_data, 20)
    assert_value(packet.car_idx, 7)
    assert_value(packet.fitted_idx, 8)


def test_exmotion():
    pkt = exmotion_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.ExMotionPacket.decode(pkt)

    assert_value(header.packet_id, 13)
    assert_value(packet.suspension_rl_position, 44.06889724731445)


def test_laphistory():
    pkt = position_history_packet_example
    header = udp_protocol.Header.decode(pkt)
    packet = udp_protocol.LapPositionPacket.decode(pkt)

    assert_value(header.packet_id, 15)
    assert_value(packet.laps_in_data, 3)
    assert_list_length(packet.position_for_vehicle_idx, 50)
    assert_list_length(list(packet.position_for_vehicle_idx[0]), 22)
    assert_value(packet.position_for_vehicle_idx[0][header.player_car_index], 20)
    assert_value(packet.position_for_vehicle_idx[1][header.player_car_index], 11)
