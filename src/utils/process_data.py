#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import functools

from config import shared_variables as shared
from utils import prettyfy


def process_initial_data(header, values, shared, task_queue):
    shared.header = header

    if header.packet_id == 1:
        shared.prev_session = shared.session
        shared.session = values
        shared.session_type_cache = values.session_type
        shared.session_cache = 0


def process_race_data(header, values, shared, task_queue):
    shared.header = header

    if header.packet_id == 1:
        shared.prev_session = shared.session
        shared.session = values
        shared.session_type_cache = values.session_type
        task_queue.put_nowait(functools.partial(prettyfy.calc_track_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_pit_string))
    if header.packet_id == 2 and shared.participants_cache != 0:
        if shared.prev_lapdata is None:
            shared.prev_lapdata = values
            shared.lapdata = values
        else:
            shared.prev_lapdata = shared.lapdata
            shared.lapdata = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_track_position))
        task_queue.put_nowait(functools.partial(prettyfy.calc_lap_time_strings))
        task_queue.put_nowait(functools.partial(prettyfy.calc_laps_completed_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_behind_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_infront_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_position_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_gap_to_p2))
    if header.packet_id == 3:
        shared.event = values
        task_queue.put_nowait(functools.partial(prettyfy.set_event_events))
    if header.packet_id == 4 and shared.participants_cache == 0:
        shared.participants = values.cars
        shared.participants_cache += 1
    if header.packet_id == 5:
        shared.prev_setup = shared.telemetry
        shared.setup = values
    if header.packet_id == 6:
        shared.prev_telemetry = shared.telemetry
        shared.telemetry = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_temps_strings))
    if header.packet_id == 7:
        shared.prev_status = shared.status
        shared.status = values
    if header.packet_id == 8:
        shared.prev_classification = shared.classification
        shared.classification = values
    if header.packet_id == 9 and shared.lobby_cache == 0:
        shared.lobby = values
        shared.lobby_cache += 1
    if header.packet_id == 10:
        shared.prev_damage = shared.damage
        shared.damage = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_damage_strings))
    if header.packet_id == 11:
        if values.relevant_car_id == header.player_car_index:
            shared.player_histories += 1
        task_queue.put_nowait(functools.partial(prettyfy.update_shared_history, values))
    if header.packet_id == 12:
        shared.tyres[values.car_idx] = {
            "tyre_sets_data": values.tyre_set_data,
            "fitted_idx": values.fitted_idx,
        }
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_sets))
    if header.packet_id == 13:
        shared.prev_exmotion = shared.exmotion
        shared.exmotion = values
    if header.packet_id == 14:
        shared.prev_timetrial = shared.timetrial
        shared.timetrial = values
    if header.packet_id == 15:
        shared.position_history = values


def process_practice_data(header, values, shared, task_queue):
    shared.header = header

    if header.packet_id == 1:
        shared.prev_session = shared.session
        shared.session = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_track_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_pit_string))
    if header.packet_id == 2 and shared.participants_cache != 0:
        if shared.prev_lapdata is None:
            shared.prev_lapdata = values
            shared.lapdata = values
        else:
            shared.prev_lapdata = shared.lapdata
            shared.lapdata = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_track_position))
        task_queue.put_nowait(functools.partial(prettyfy.calc_lap_time_strings))
        task_queue.put_nowait(functools.partial(prettyfy.calc_laps_completed_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_behind_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_infront_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_position_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_gap_to_p2))
    if header.packet_id == 3:
        shared.event = values
        task_queue.put_nowait(functools.partial(prettyfy.set_event_events))
    if header.packet_id == 4 and shared.participants_cache == 0:
        shared.participants = values.cars
        shared.participants_cache += 1
    if header.packet_id == 5:
        shared.prev_setup = shared.telemetry
        shared.setup = values
    if header.packet_id == 6:
        shared.prev_telemetry = shared.telemetry
        shared.telemetry = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_temps_strings))
    if header.packet_id == 7:
        shared.prev_status = shared.status
        shared.status = values
    if header.packet_id == 8:
        shared.prev_classification = shared.classification
        shared.classification = values
    if header.packet_id == 9 and shared.lobby_cache == 0:
        shared.lobby = values
        shared.lobby_cache += 1
    if header.packet_id == 10:
        shared.prev_damage = shared.damage
        shared.damage = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_damage_strings))
    if header.packet_id == 11:
        if values.relevant_car_id == header.player_car_index:
            shared.player_histories += 1
        task_queue.put_nowait(functools.partial(prettyfy.update_shared_history, values))
    if header.packet_id == 12:
        shared.tyres[values.car_idx] = {
            "tyre_sets_data": values.tyre_set_data,
            "fitted_idx": values.fitted_idx,
        }
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_sets))
    if header.packet_id == 13:
        shared.prev_exmotion = shared.exmotion
        shared.exmotion = values
    if header.packet_id == 14:
        shared.prev_timetrial = shared.timetrial
        shared.timetrial = values
    if header.packet_id == 15:
        shared.position_history = values


def process_quali_data(header, values, shared, task_queue):
    shared.header = header

    if header.packet_id == 1:
        shared.prev_session = shared.session
        shared.session = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_track_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_pit_string))
    if header.packet_id == 2 and shared.participants_cache != 0:
        if shared.prev_lapdata is None:
            shared.prev_lapdata = values
            shared.lapdata = values
        else:
            shared.prev_lapdata = shared.lapdata
            shared.lapdata = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_track_position))
        task_queue.put_nowait(functools.partial(prettyfy.calc_lap_time_strings))
        task_queue.put_nowait(functools.partial(prettyfy.calc_laps_completed_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_behind_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_infront_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_position_string))
        task_queue.put_nowait(functools.partial(prettyfy.calc_gap_to_p2))
    if header.packet_id == 3:
        shared.event = values
        task_queue.put_nowait(functools.partial(prettyfy.set_event_events))
    if header.packet_id == 4 and shared.participants_cache == 0:
        shared.participants = values.cars
        shared.participants_cache += 1
    if header.packet_id == 5:
        shared.prev_setup = shared.telemetry
        shared.setup = values
    if header.packet_id == 6:
        shared.prev_telemetry = shared.telemetry
        shared.telemetry = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_temps_strings))
    if header.packet_id == 7:
        shared.prev_status = shared.status
        shared.status = values
    if header.packet_id == 8:
        shared.prev_classification = shared.classification
        shared.classification = values
    if header.packet_id == 9 and shared.lobby_cache == 0:
        shared.lobby = values
        shared.lobby_cache += 1
    if header.packet_id == 10:
        shared.prev_damage = shared.damage
        shared.damage = values
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_damage_strings))
    if header.packet_id == 11:
        if values.relevant_car_id == header.player_car_index:
            shared.player_histories += 1
        task_queue.put_nowait(functools.partial(prettyfy.update_shared_history, values))
    if header.packet_id == 12:
        shared.tyres[values.car_idx] = {
            "tyre_sets_data": values.tyre_set_data,
            "fitted_idx": values.fitted_idx,
        }
        task_queue.put_nowait(functools.partial(prettyfy.calc_tyre_sets))
    if header.packet_id == 13:
        shared.prev_exmotion = shared.exmotion
        shared.exmotion = values
    if header.packet_id == 14:
        shared.prev_timetrial = shared.timetrial
        shared.timetrial = values
    if header.packet_id == 15:
        shared.position_history = values
