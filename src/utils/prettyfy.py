#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from operator import attrgetter

from loguru import logger

from config import shared_variables as sv
from models import decode_dictionaries as dc


def surround_by_div(string: str) -> str:
    return f"<div>{string}</div>"


def surround_by_circle(string: str) -> str:
    return f'<svg width="125" height="125" viewBox="0 0 100 100"><circle cx="50" cy="47.5" r="40" fill="none" stroke="black" stroke-width="6" /><circle cx="50" cy="47.5" r="30" fill="green" stroke="red" stroke-width="4" /><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" font-size="20">{string}</text></svg>'


def humanise(milliseconds: int) -> str:
    # Turn millisecond strings into nicer strings.
    sign = "-" if milliseconds < 0 else "+"
    total_seconds = abs(milliseconds) / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    if minutes > 0:
        text = f"{sign}{minutes:02.0f} : {seconds:06.3f}"
    else:
        text = f"{sign}{seconds:.3f}"

    return f"{text}"


def compact_humanise(milliseconds: int) -> str:
    # Turn millisecond strings into nicer strings.
    sign = "-" if milliseconds < 0 else "+"
    total_seconds = abs(milliseconds) / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    if minutes > 0:
        text = f"{sign}{minutes:02.0f}:{seconds:04.1f}"
    else:
        text = f"{sign}{seconds:.1f}"

    return f"{text}"


def calculate_drs_status(player, oppo_idx, sv):
    """Calculates the DRS status of the player in relation
    to the cars ahead and behind.
    """
    if sv.status == None:
        return None
    if sv.telemetry == None:
        return None

    track_id = sv.session.track_id

    try:
        drs_detection_points = dc.drs_detection_zones_dict[track_id]
        drs_detection_distance = next(
            distance - player.lap_distance_travelled_m
            if distance > player.lap_distance_travelled_m
            else 0
            for distance in drs_detection_points
        )
    except StopIteration():
        drs_detection_distance = ""

    drs_player = int(drs_detection_distance) if drs_detection_distance > 0 else ""
    drs_oppo = (
        dc.drs_allowed_dict[sv.telemetry.statuses[oppo_idx].drs]
        if oppo_idx != 255
        else ""
    )

    return [drs_player, drs_oppo]


### -------------------------------------------------------------------------------- ###
def calc_track_string():
    if sv.session_cache < 1:
        session = sv.session
        weather_string = f"{dc.weather_dict[session.weather]}"
        track_string = f"{dc.tract_dict[session.track_id]} ({weather_string})"

        sv.session_cache += 1

        return ("track_string", track_string)
    return None


### -------------------------------------------------------------------------------- ###
def calc_pit_string():
    if sv.session_cache < 2:
        session = sv.session
        pit_speed = session.pit_speed_limit_kph
        pit_lap = session.pit_stop_ideal_lap
        pit_latest_lap = session.pit_stop_latest_lap
        pit_rejoin_position = session.pit_stop_rejoin_position
        pit_string = f"<div>{pit_speed}kmph</div><div>Pit  between lap {pit_lap} to {pit_latest_lap}</div><div>Rejoin: {pit_rejoin_position}</div>"

        sv.session_cache += 2

        return ("pit_string", pit_string)
    return None


### -------------------------------------------------------------------------------- ###
def calc_track_position():
    player_idx = sv.header.player_car_index
    lapdata = sv.lapdata
    player = lapdata.cars[player_idx]
    track_position = f"{player.lap_distance_travelled_m:6.0f}m"
    return ("track_position", track_position)


### -------------------------------------------------------------------------------- ###
def calc_lap_time_strings():
    header = sv.header
    lapdata = sv.lapdata

    player_idx = header.player_car_index
    player_history = sv.history[player_idx]

    player = lapdata.cars[player_idx]
    current_lap_time = player.current_lap_time_ms
    current_s1_time = (
        player.sector1_time_ms_component
        if player.sector1_time_ms_component > 0
        else 9999999999
    )
    current_s2_time = (
        player.sector2_time_ms_component
        if player.sector2_time_ms_component > 0
        else 9999999999
    )

    if player.current_lap_number > 1:
        # zero index so -1, then want previous lap so -1 again
        previous_lap_time = player_history["lap_history_data"][
            player_history["number_of_laps_in_data"] - 2
        ].lap_time_ms
        previous_s1_time = player_history["lap_history_data"][
            player_history["number_of_laps_in_data"] - 2
        ].sector1_time_ms_component
        previous_s2_time = player_history["lap_history_data"][
            player_history["number_of_laps_in_data"] - 2
        ].sector2_time_ms_component
        previous_s3_time = player_history["lap_history_data"][
            player_history["number_of_laps_in_data"] - 2
        ].sector3_time_ms_component

        # Where the magic sauce happens
        if player.sector >= 0:
            s1_delta = min(current_lap_time, current_s1_time) - (
                (
                    min(
                        player.lap_distance_travelled_m,
                        sv.session.sector_2_start_distance_m,
                    )
                )
                / (sv.session.sector_2_start_distance_m)
                * previous_s1_time
            )
        if player.sector >= 1:
            s2_delta = min(current_lap_time - current_s1_time, current_s2_time) - (
                (
                    min(
                        player.lap_distance_travelled_m,
                        sv.session.sector_3_start_distance_m,
                    )
                    - sv.session.sector_2_start_distance_m
                )
                / (
                    sv.session.sector_3_start_distance_m
                    - sv.session.sector_2_start_distance_m
                )
                * previous_s2_time
            )
        else:
            s2_delta = 0
        if player.sector >= 2:
            s3_delta = (current_lap_time - current_s1_time - current_s2_time) - (
                (player.lap_distance_travelled_m - sv.session.sector_3_start_distance_m)
                / (sv.session.track_length_m - sv.session.sector_3_start_distance_m)
                * previous_s3_time
            )
        else:
            s3_delta = 0

        _s1 = surround_by_div(humanise(current_lap_time))
        _s2 = humanise(min(current_lap_time, current_s1_time))
        _s3 = humanise(s1_delta)
        _s4 = humanise(
            min(current_lap_time - current_s1_time, current_s2_time)
            if player.sector > 0
            else 0
        )
        _s5 = humanise(s2_delta)
        _s6 = humanise(
            current_lap_time - current_s1_time - current_s2_time
            if player.sector > 1
            else 0
        )
        _s7 = humanise(s3_delta)
        title = surround_by_div("CURRENT LAP")
        _s8 = surround_by_div(f"{_s1}{_s2} ({_s3}) | {_s4} ({_s5}) | {_s6} ({_s7})")
        current_lap_time_string = f"{title}{_s8}"
    else:
        title = surround_by_div("CURRENT LAP")
        _s1 = surround_by_div(f"{humanise(player.current_lap_time_ms)}")
        current_lap_time_string = f"{title}{_s1}"

    if player.current_lap_number > 1:
        # zero indexed
        best_lap_time = player_history["lap_history_data"][
            player_history["best_lap_number"] - 1
        ].lap_time_ms
        best_lap_s1_time = player_history["lap_history_data"][
            player_history["best_lap_number"] - 1
        ].sector1_time_ms_component
        best_lap_s2_time = player_history["lap_history_data"][
            player_history["best_lap_number"] - 1
        ].sector2_time_ms_component
        best_lap_s3_time = player_history["lap_history_data"][
            player_history["best_lap_number"] - 1
        ].sector3_time_ms_component

        _s1 = surround_by_div(humanise(best_lap_time))
        _s2 = humanise(best_lap_s1_time)
        _s3 = humanise(best_lap_s2_time)
        _s4 = humanise(best_lap_s3_time)
        _s5 = surround_by_div(f"{_s1}{_s2} | {_s3} | {_s4}")
        _title = surround_by_div("PLAYER BEST")
        best_lap_string = f"{_title}{_s5}"
    else:
        _title = surround_by_div("PLAYER BEST")
        _s1 = surround_by_div(humanise(player.current_lap_time_ms))
        best_lap_string = f"{_title}{_s1}"

    return [
        ("current_lap_time_string", current_lap_time_string),
        ("player_best_lap_time_string", best_lap_string),
    ]


### -------------------------------------------------------------------------------- ###
def calc_laps_completed_string():
    header = sv.header
    lapdata = sv.lapdata
    session = sv.session
    player = lapdata.cars[header.player_car_index]
    title = surround_by_div("LAPS")
    _s1 = surround_by_div(f"{player.current_lap_number} of {session.total_race_laps}")
    laps_completed_string = f"{title}{_s1}"
    return ("laps_completed_string", laps_completed_string)


### -------------------------------------------------------------------------------- ###
def calc_behind_string():
    header = sv.header
    lapdata = sv.lapdata
    participants = sv.participants
    prev_lapdata = sv.prev_lapdata

    if sv.status is None:
        return None

    player = lapdata.cars[header.player_car_index]
    try:
        behind_idx, behind_player = next(
            (idx, car)
            for (idx, car) in enumerate(lapdata.cars)
            if car.car_position == player.car_position + 1
        )
        # Want to check against player position this lap since thats what matters now
        behind_idx_previous, behind_player_previous = next(
            (idx, car)
            for (idx, car) in enumerate(prev_lapdata.cars)
            if car.car_position == player.car_position + 1
        )
    except StopIteration:
        # In first place
        behind_idx = 255
        behind_player = "Currently in Last Place"

    # html div tags to make life easier later
    if behind_idx != 255:
        try:
            drs_player, drs_behind = calculate_drs_status(player, behind_idx, sv)
        except TypeError:
            # when no data loaded yet
            drs_player = ""
            drs_behind = ""
        _s1 = surround_by_div(dc.driver_dict[participants[behind_idx].driver_id])
        _s2 = surround_by_div(
            humanise(behind_player.delta_to_car_in_front_ms_component)
        )
        _s3 = surround_by_div(drs_behind)
        _s4 = surround_by_div(
            dc.visual_tyre_compound_dict[
                sv.status.statuses[behind_idx].visual_tyre_compound
            ]
        )
        _s5 = surround_by_div(drs_player)
    else:
        _s1 = behind_player
        _s2 = ""
        _s3 = ""
        _s4 = ""
        _s5 = ""

    _title = surround_by_div("PLAYER BEHIND")
    _s6 = surround_by_div(f"{_s1}{_s2}{_s3}{_s4}{_s5}")
    behind_string = f"{_title}{_s6}"
    return ("behind_string", behind_string)


### -------------------------------------------------------------------------------- ###
def calc_infront_string():
    header = sv.header
    lapdata = sv.lapdata
    participants = sv.participants
    prev_lapdata = sv.prev_lapdata

    if sv.status is None:
        return None

    player = lapdata.cars[header.player_car_index]
    try:
        infront_idx, infront_player = next(
            (idx, car)
            for (idx, car) in enumerate(lapdata.cars)
            if car.car_position == player.car_position - 1
        )
        # Want to check against player position this lap since thats what matters now
        infront_idx_previous, infront_player_previous = next(
            (idx, car)
            for (idx, car) in enumerate(prev_lapdata.cars)
            if car.car_position == player.car_position - 1
        )
    except StopIteration:
        # In first place
        infront_idx = 255
        infront_player = "Currently in P1"

    # html div tags to make life easier later
    if infront_idx != 255:
        try:
            drs_player, drs_infront = calculate_drs_status(player, infront_idx, sv)
        except TypeError:
            # when no data loaded yet
            drs_player = ""
            drs_infront = ""

        _s1 = surround_by_div(dc.driver_dict[participants[infront_idx].driver_id])
        _s2 = surround_by_div(humanise(player.delta_to_car_in_front_ms_component))
        _s3 = surround_by_div(drs_infront)
        _s4 = surround_by_div(
            dc.visual_tyre_compound_dict[
                sv.status.statuses[infront_idx].visual_tyre_compound
            ]
        )
        _s5 = surround_by_div(drs_player)
    else:
        _s1 = infront_player
        _s2 = ""
        _s3 = ""
        _s4 = ""
        _s5 = ""

    _title = surround_by_div("PLAYER AHEAD")
    _s6 = surround_by_div(f"{_s1}{_s2}{_s3}{_s4}{_s5}")
    infront_string = f"{_title}{_s6}"
    return ("infront_string", infront_string)


### -------------------------------------------------------------------------------- ###
def calc_position_string():
    header = sv.header
    lapdata = sv.lapdata

    player = lapdata.cars[header.player_car_index]
    _s1 = player.car_position
    _s2 = int(player.car_position) - int(player.grid_position)
    # Can set custom html if want
    _prefix = (
        "<i class='bi bi-caret-up-fill' style='color: green'>"
        if _s2 < 0
        else "<i class='bi bi-caret-down-fill' style='color: red'>"
        if _s2 > 0
        else "<i class='bi bi-caret-down-fill' style='color: yellow'>"
    )
    _s2 = str(_s2).replace("-", "") if _s2 < 0 else str(_s2)
    _s3 = surround_by_div(f"{_s1} ({_prefix}{_s2}</i> )")

    pit_stop_count_of_cars_ahead = [
        car.number_of_pit_stops
        for car in lapdata.cars
        if car.car_position > player.car_position
    ].count(0)

    effective_position = (
        (player.car_position - pit_stop_count_of_cars_ahead)
        if player.number_of_pit_stops > 0
        else player.car_position
    )
    _s4 = surround_by_div(f"Effective: {effective_position}")

    title = surround_by_div("POSITION")
    position_string = f"{title}{_s3}{_s4}"

    return ("position_string", position_string)


### -------------------------------------------------------------------------------- ###
def calc_tyre_damage_strings():
    header = sv.header
    damage = sv.damage.statuses[header.player_car_index]

    _s1 = damage.tyre_rl_wear_percentage
    _s2 = damage.tyre_rr_wear_percentage
    _s3 = damage.tyre_fl_wear_percentage
    _s4 = damage.tyre_fr_wear_percentage

    rear_left_wear_string = surround_by_circle(f"{_s1:5.1f}%")
    rear_right_wear_string = f"{_s2:5.1f}%"
    front_left_wear_string = f"{_s3:5.1f}%"
    front_right_wear_string = f"{_s4:5.1f}%"

    return [
        ("front_left_wear_string", front_left_wear_string),
        ("front_right_wear_string", front_right_wear_string),
        ("rear_left_wear_string", rear_left_wear_string),
        ("rear_right_wear_string", rear_right_wear_string),
    ]


### -------------------------------------------------------------------------------- ###
def calc_tyre_temps_strings():
    header = sv.header
    telemetry = sv.telemetry.statuses[header.player_car_index]
    setup = sv.setup.setups[header.player_car_index]

    _s1 = surround_by_div(telemetry.tyres_rl_surface_temperature)
    _s2 = surround_by_div(telemetry.tyres_rl_inner_temperature)
    _s3 = surround_by_div(f"{setup.rear_left_tyre_pressure:4.1f}")
    _s4 = surround_by_div(f"{telemetry.tyres_rl_pressure:4.1f}")
    rear_left_temp_string = f"surface: {_s1}core: {_s2}pressure: {_s4} ({_s3})"
    del _s1, _s2, _s3, _s4

    _s1 = surround_by_div(telemetry.tyres_rr_surface_temperature)
    _s2 = surround_by_div(telemetry.tyres_rr_inner_temperature)
    _s3 = surround_by_div(f"{setup.rear_right_tyre_pressure:4.1f}")
    _s4 = surround_by_div(f"{telemetry.tyres_rr_pressure:4.1f}")
    rear_right_temp_string = f"surface: {_s1}core: {_s2}pressure: {_s4} ({_s3})"
    del _s1, _s2, _s3, _s4

    _s1 = surround_by_div(telemetry.tyres_fl_surface_temperature)
    _s2 = surround_by_div(telemetry.tyres_fl_inner_temperature)
    _s3 = surround_by_div(f"{setup.front_left_tyre_pressure:4.1f}")
    _s4 = surround_by_div(f"{telemetry.tyres_fl_pressure:4.1f}")
    front_left_temp_string = f"surface: {_s1}core: {_s2}pressure: {_s4} ({_s3})"
    del _s1, _s2, _s3, _s4

    _s1 = surround_by_div(telemetry.tyres_fr_surface_temperature)
    _s2 = surround_by_div(telemetry.tyres_fr_inner_temperature)
    _s3 = surround_by_div(f"{setup.front_right_tyre_pressure:4.1f}")
    _s4 = surround_by_div(f"{telemetry.tyres_fr_pressure:4.1f}")
    front_right_temp_string = f"surface: {_s1}core: {_s2}pressure: {_s4} ({_s3})"

    return [
        ("front_left_temp_string", front_left_temp_string),
        ("front_right_temp_string", front_right_temp_string),
        ("rear_left_temp_string", rear_left_temp_string),
        ("rear_right_temp_string", rear_right_temp_string),
    ]


### -------------------------------------------------------------------------------- ###
def calc_tyre_sets():
    header = sv.header
    try:
        tyres = sv.tyres[header.player_car_index]["tyre_sets_data"]
    except TypeError:
        return None

    softs = [
        tyre
        for tyre in tyres
        if tyre.visual_tyre_compound == 16 and tyre.available == 1 and tyre.fitted != 1
    ]
    mediums = [
        tyre
        for tyre in tyres
        if tyre.visual_tyre_compound == 17 and tyre.available == 1 and tyre.fitted != 1
    ]
    hards = [
        tyre
        for tyre in tyres
        if tyre.visual_tyre_compound == 18 and tyre.available == 1 and tyre.fitted != 1
    ]
    inters = [
        tyre
        for tyre in tyres
        if (tyre.visual_tyre_compound == 7 and tyre.available == 1 and tyre.fitted != 1)
    ]

    count_new_softs = len([tyre for tyre in softs if tyre.wear == 0])
    count_new_mediums = len([tyre for tyre in mediums if tyre.wear == 0])
    count_new_hards = len([tyre for tyre in hards if tyre.wear == 0])
    count_new_inters = len([tyre for tyre in inters if tyre.wear == 0])

    try:
        best_softs = min(softs, key=attrgetter("wear"))
        best_mediums = min(mediums, key=attrgetter("wear"))
        best_hards = min(hards, key=attrgetter("wear"))
        best_inters = min(inters, key=attrgetter("wear"))
    except ValueError:
        return ""

    _s1 = f"{count_new_softs} new" if count_new_softs > 0 else f"{len(softs)} used"
    _s2 = f"{compact_humanise(best_softs.lap_delta_time)}s"
    # Div by 2 since after 50% tyres are fairly useless
    _s3 = f"{best_softs.usable_life // 2}"
    softs_string = surround_by_div(f"Soft:{_s1}({_s3}@{_s2})")
    del _s1, _s2, _s3

    _s1 = (
        f"{count_new_mediums} new" if count_new_mediums > 0 else f"{len(mediums)} used"
    )
    _s2 = f"{compact_humanise(best_mediums.lap_delta_time)}s"
    _s3 = f"{best_mediums.usable_life // 2}"
    mediums_string = surround_by_div(f"Med:{_s1}({_s3}@{_s2})")
    del _s1, _s2, _s3

    _s1 = f"{count_new_hards} new" if count_new_hards > 0 else f"{len(hards)} used"
    _s2 = f"{compact_humanise(best_hards.lap_delta_time)}s"
    _s3 = f"{best_hards.usable_life // 2}"
    hards_string = surround_by_div(f"Hard:{_s1}({_s3}@{_s2})")
    del _s1, _s2, _s3

    _s1 = f"{count_new_inters} new" if count_new_inters > 0 else f"{len(inters)} used"
    _s2 = f"{compact_humanise(best_inters.lap_delta_time)}s"
    _s3 = f"{best_inters.usable_life // 2}"
    inters_string = surround_by_div(f"Int:{_s1}({_s3}@{_s2})")
    del _s1, _s2, _s3

    session = sv.session
    pit_speed = session.pit_speed_limit_kph
    pit_lap = session.pit_stop_ideal_lap
    pit_latest_lap = session.pit_stop_latest_lap
    pit_rejoin_position = session.pit_stop_rejoin_position
    _s1 = surround_by_div(pit_speed)
    _s2 = surround_by_div(f"Pit between lap {pit_lap} to {pit_latest_lap}")
    _s3 = surround_by_div(f"Rejoin position: {pit_rejoin_position}")
    pit_string = (
        f"{_s1}{_s2}{_s3}{softs_string}{mediums_string}{hards_string}{inters_string}"
    )

    return ("pit_string", pit_string)


### -------------------------------------------------------------------------------- ###
def update_shared_history(values, sv=sv) -> None:
    sv.history[values.relevant_car_id] = {
        "number_of_laps_in_data": values.number_of_laps_in_data,
        "number_of_tyre_stints": values.number_of_tyre_stints,
        "best_lap_number": values.best_lap_number,
        "best_s1_lap_number": values.best_s1_lap_number,
        "best_s2_lap_number": values.best_s2_lap_number,
        "best_s3_lap_number": values.best_s3_lap_number,
        "lap_history_data": values.lap_history_data,
        "tyre_history_data": values.tyre_history_data,
    }


### -------------------------------------------------------------------------------- ###
def set_event_events():
    header = sv.header
    event = sv.event
    session = sv.session

    if session is not None:
        _s1 = dc.tract_dict[session.track_id]
        _s2 = dc.weather_dict[session.weather]
        _s3 = surround_by_div(f"{_s1} ({_s2})")
        _s4 = None

        match event.event_code:
            case "SSTA":
                pass
            case "SEND":
                pass
            case "FTLP":
                _s4 = surround_by_div(
                    f"Fastest Lap: {dc.driver_dict[sv.participants[event.fastest_lap_car_id].driver_id]}"
                )
                _s5 = surround_by_div(sv.event_fastest_lap["driver"])
                _s6 = surround_by_div(humanise(sv.event_fastest_lap["time"]))
                _s7 = surround_by_div(f"Lap {sv.event_fastest_lap['lap']}")
                _s8 = surround_by_div(f"{_s5}{_s6}{_s7}")
                _title = surround_by_div("SESSION BEST")
                fastest_lap_string = f"{_title}{_s8}"
                return ("fastest_lap_string", fastest_lap_string)
            case "RTMT":
                _driver = dc.driver_dict[
                    sv.participants[event.retired_car_id].driver_id
                ]
                _reason = dc.retirement_reason_dict[event.retirement_reason]
                _s4 = surround_by_div(f"{_driver} retired ({_reason})")
            case "DRSE":
                _s4 = surround_by_div("DRS Enabled")
            case "DRSD":
                _reason = dc.drs_reason_dict[event.reason]
                _s4 = surround_by_div(f"DRS Disabled ({_reason}")
            case "TMPT":
                pass
            case "CHQF":
                pass
            case "RCWN":
                pass
            case "PENA":
                _penalty_type = dc.penalty_dict[event.penalty_type]
                _infringement_type = dc.infringement_dict[event.infringement_type]
                _criminal = dc.driver_dict[
                    sv.participants[event.car_id_of_criminal].driver_id
                ]
                _s4 = surround_by_div(
                    f"{_criminal}: {_infringement_type} ({_penalty_type})"
                )
            case "SPTP":
                pass
            case "STLG":
                pass
            case "LGOT":
                pass
            case "DTSV":
                pass
            case "SGSV":
                pass
            case "FLBK":
                pass
            case "BUTN":
                pass
            case "RDFL":
                pass
            case "OVTK":
                pass
            case "SCAR":
                _car_type = dc.safety_car_type_dict[event.safety_car_type]
                _car_status = dc.safety_car_status_dict[event.safety_car_type]
                _s4 = surround_by_div(f"{_car_type}: {_car_status}")
            case "COLL":
                pass

        if _s4 is not None:
            track_string = f"{_s3}{_s4}"
            return ("track_string", track_string)
    return None


### -------------------------------------------------------------------------------- ###
def calc_gap_to_p2():
    header = sv.header
    lapdata = sv.lapdata
    participants = sv.participants

    if sv.status is None:
        return None

    player = lapdata.cars[header.player_car_index]
    player_gap_to_leader = player.delta_to_leader_ms_component

    player_controlled_cars = [
        idx for idx, _ in enumerate(participants) if _.is_ai_controlled_flag == 0
    ].remove(player)

    if header.player2_car_index != 255:
        player_2 = lapdata.cars[header.player2_car_index]
        player_2_gap_to_leader = player_2.delta_to_leader_ms_component
        delta_to_player_2 = humanise(player_2_gap_to_leader - player_gap_to_leader)
        _s2 = surround_by_div(f"P2: {delta_to_player_2}")
    elif len(player_controlled_cars) == 1:
        player_2 = next(player_controlled_cars)
        player_2_gap_to_leader = player_2.delta_to_leader_ms_component
        delta_to_player_2 = humanise(player_2_gap_to_leader - player_gap_to_leader)
        _s2 = surround_by_div(f"P2: {delta_to_player_2}")
    else:
        _s2 = ""

    _s1 = surround_by_div(f"Leader: {humanise(player_gap_to_leader)}")
    _title = "DELTAS"

    gap_string = f"{_title}{_s1}{_s2}"

    return ("gap_string", gap_string)
