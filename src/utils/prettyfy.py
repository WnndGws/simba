#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from operator import attrgetter

from loguru import logger

from models import decode_dictionaries as dc


def humanise(milliseconds: int):
    sign = "-" if milliseconds < 0 else "+"
    total_seconds = abs(milliseconds) / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    if minutes > 0:
        text = f"{sign}{minutes:02.0f} : {seconds:06.3f}"
    else:
        text = f"{sign}{seconds:.3f}"

    return f"{text}"


def calculate_drs_status(player, infront_idx, behind_idx, shared):
    """Calculates the DRS status of the player in relation to the cars ahead and behind."""
    if shared.status == None:
        return "", "", ""
    if shared.telemetry == None:
        return "", "", ""

    track_id = shared.session.track_id
    drs_detection_points = dc.drs_detection_zones_dict[track_id]

    drs_detection_distance = next(
        distance - player.lap_distance_travelled_m
        if distance > player.lap_distance_travelled_m
        else 0
        for distance in drs_detection_points
    )

    if drs_detection_distance > 0:
        drs_player = int(drs_detection_distance)
    else:
        drs_player = ""

    if infront_idx != 255:
        drs_front = dc.drs_allowed_dict[shared.telemetry.statuses[infront_idx].drs]
    else:
        drs_front = ""

    if behind_idx != 255:
        drs_behind = dc.drs_allowed_dict[shared.telemetry.statuses[behind_idx].drs]
    else:
        drs_behind = ""

    return drs_player, drs_front, drs_behind


def prettyfy_motion(shared):
    # Header 0
    pass


def prettyfy_session(shared):
    # Header 1
    header = shared.header
    prev_session = shared.prev_session
    session = shared.session

    weather_string = f"{dc.weather_dict[session.weather]}"
    total_laps_string = f"of {session.total_race_laps}"
    track_string = f"{dc.tract_dict[session.track_id]} ({weather_string})"

    pit_speed = session.pit_speed_limit_kph
    pit_lap = session.pit_stop_ideal_lap
    pit_latest_lap = session.pit_stop_latest_lap
    pit_rejoin_position = session.pit_stop_rejoin_position

    pit_string = f"{pit_speed}kmph\nPit  between lap {pit_lap} to {pit_latest_lap}\nRejoin: {pit_rejoin_position}"

    return total_laps_string, track_string, pit_string


def prettyfy_lapdata(shared):
    # Header 2
    header = shared.header
    prev_lapdata = shared.prev_lapdata
    lapdata = shared.lapdata
    participants = shared.participants

    player = lapdata.cars[header.player_car_index]
    player_previous = prev_lapdata.cars[header.player_car_index]

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
        # In last place
        behind_idx = 255
        behind_player = "Currently in Last Place"

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

    if player.current_lap_number > 1:
        drs_player, drs_front, drs_behind = calculate_drs_status(
            player, infront_idx, behind_idx, shared
        )
    else:
        drs_player, drs_front, drs_behind = "", "", ""

    _s1 = player.car_position
    _s2 = int(player.car_position) - int(player.grid_position)
    position_string = f"{_s1} ({_s2})"
    del _s1, _s2

    try:
        infront_tyre = dc.visual_tyre_compound_dict[
            shared.status.statuses[infront_idx].visual_tyre_compound
        ]
    except (AttributeError, IndexError):
        infront_tyre = ""

    try:
        behind_tyre = dc.visual_tyre_compound_dict[
            shared.status.statuses[behind_idx].visual_tyre_compound
        ]
    except (AttributeError, IndexError):
        behind_tyre = ""

    try:
        _s1 = dc.driver_dict[participants[infront_idx].driver_id]
        _s2 = humanise(player.delta_to_car_in_front_ms_component)
        infront_string = f"{_s1}\n{_s2}\n{drs_front}\n{infront_tyre}\n\n{drs_player}"
        del _s1, _s2
    except (UnboundLocalError, IndexError):
        infront_string = infront_player

    try:
        _s1 = dc.driver_dict[participants[behind_idx].driver_id]
        _s2 = humanise(behind_player.delta_to_car_in_front_ms_component)
        behind_string = f"{_s1}\n{_s2}\n{drs_behind}\n{behind_tyre}"
        del _s1, _s2
    except (UnboundLocalError, IndexError):
        behind_string = behind_player

    laps_completed_string = str(player.current_lap_number)

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
        previous_lap_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["number_of_laps_in_data"] - 2
        ].lap_time_ms
        previous_s1_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["number_of_laps_in_data"] - 2
        ].sector1_time_ms_component
        previous_s2_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["number_of_laps_in_data"] - 2
        ].sector2_time_ms_component
        previous_s3_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["number_of_laps_in_data"] - 2
        ].sector3_time_ms_component

        if player.sector >= 0:
            s1_delta = min(current_lap_time, current_s1_time) - (
                (
                    min(
                        player.lap_distance_travelled_m,
                        shared.session.sector_2_start_distance_m,
                    )
                )
                / (shared.session.sector_2_start_distance_m)
                * previous_s1_time
            )
        if player.sector >= 1:
            s2_delta = min(current_lap_time - current_s1_time, current_s2_time) - (
                (
                    min(
                        player.lap_distance_travelled_m,
                        shared.session.sector_3_start_distance_m,
                    )
                    - shared.session.sector_2_start_distance_m
                )
                / (
                    shared.session.sector_3_start_distance_m
                    - shared.session.sector_2_start_distance_m
                )
                * previous_s2_time
            )
        else:
            s2_delta = 0
        if player.sector >= 2:
            s3_delta = (current_lap_time - current_s1_time - current_s2_time) - (
                (
                    player.lap_distance_travelled_m
                    - shared.session.sector_3_start_distance_m
                )
                / (
                    shared.session.track_length_m
                    - shared.session.sector_3_start_distance_m
                )
                * previous_s3_time
            )
        else:
            s3_delta = 0

        _s1 = humanise(current_lap_time)
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
        current_lap_time_string = (
            f"{_s1}\n{_s2} ({_s3}) | {_s4} ({_s5}) | {_s6} ({_s7})"
        )
        del _s1, _s2, _s3, _s4, _s5, _s6, _s7
    else:
        current_lap_time_string = f"{humanise(player.current_lap_time_ms)}"

    if player.current_lap_number > 1:
        # zero indexed
        best_lap_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["best_lap_number"] - 1
        ].lap_time_ms
        best_lap_s1_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["best_lap_number"] - 1
        ].sector1_time_ms_component
        best_lap_s2_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["best_lap_number"] - 1
        ].sector2_time_ms_component
        best_lap_s3_time = shared.history[header.player_car_index]["lap_history_data"][
            shared.history[header.player_car_index]["best_lap_number"] - 1
        ].sector3_time_ms_component

        _s1 = humanise(best_lap_time)
        _s2 = humanise(best_lap_s1_time)
        _s3 = humanise(best_lap_s2_time)
        _s4 = humanise(best_lap_s3_time)
        best_lap_string = f"{_s1}\n{_s2} | {_s3} | {_s4}"
        del _s1, _s2, _s3, _s4
    else:
        best_lap_string = humanise(player.current_lap_time_ms)

    if shared.event_fastest_lap != None:
        fastest_lap_string = f"{shared.event_fastest_lap['driver']}\n{humanise(shared.event_fastest_lap['time'])}\nLap {shared.event_fastest_lap['lap']}"
    else:
        fastest_lap_string = ""

    track_position = f"{player.lap_distance_travelled_m:6.0f}m"

    return (
        position_string,
        infront_string,
        behind_string,
        laps_completed_string,
        current_lap_time_string,
        best_lap_string,
        fastest_lap_string,
        track_position,
    )


def prettyfy_event(shared):
    # Header 3
    header = shared.header
    event = shared.event

    match event.event_code:
        case "SSTA":
            pass
        case "SEND":
            pass
        case "FTLP":
            shared.event_fastest_lap = {
                "driver": dc.driver_dict[
                    shared.participants[event.fastest_lap_car_id].driver_id
                ],
                "time": (event.fastest_lap_seconds * 1000),
                "lap": shared.lapdata.cars[header.player_car_index].current_lap_number,
            }
        case "RTMT":
            pass
        case "DRSE":
            pass
        case "DRSD":
            pass
        case "TMPT":
            pass
        case "CHQF":
            pass
        case "RCWN":
            pass
        case "PENA":
            pass
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
            pass
        case "COLL":
            pass


def prettyfy_participants():
    # Header 4
    pass


def prettyfy_setup():
    # Header 5
    pass


def prettyfy_telemetry(shared):
    # Header 6
    header = shared.header
    telemetry = shared.telemetry.statuses[header.player_car_index]
    setup = shared.setup.setups[header.player_car_index]

    _s1 = telemetry.tyres_rl_surface_temperature
    _s2 = telemetry.tyres_rl_inner_temperature
    _s3 = setup.rear_left_tyre_pressure
    _s4 = telemetry.tyres_rl_pressure
    rear_left_temp_string = (
        f"surface: {_s1}\ncore: {_s2}\npressure: {_s4:4.1f} ({_s3:4.1f})"
    )
    del _s1, _s2, _s3, _s4

    _s1 = telemetry.tyres_rr_surface_temperature
    _s2 = telemetry.tyres_rr_inner_temperature
    _s3 = setup.rear_right_tyre_pressure
    _s4 = telemetry.tyres_rr_pressure
    rear_right_temp_string = (
        f"surface: {_s1}\ncore: {_s2}\npressure: {_s4:4.1f} ({_s3:4.1f})"
    )
    del _s1, _s2, _s3, _s4

    _s1 = telemetry.tyres_fl_surface_temperature
    _s2 = telemetry.tyres_fl_inner_temperature
    _s3 = setup.front_left_tyre_pressure
    _s4 = telemetry.tyres_fl_pressure
    front_left_temp_string = (
        f"surface: {_s1}\ncore: {_s2}\npressure: {_s4:4.1f} ({_s3:4.1f})"
    )
    del _s1, _s2, _s3, _s4

    _s1 = telemetry.tyres_fr_surface_temperature
    _s2 = telemetry.tyres_fr_inner_temperature
    _s3 = setup.front_right_tyre_pressure
    _s4 = telemetry.tyres_fr_pressure
    front_right_temp_string = (
        f"surface: {_s1}\ncore: {_s2}\npressure: {_s4:4.1f} ({_s3:4.1f})"
    )
    del _s1, _s2, _s3, _s4

    return (
        rear_left_temp_string,
        rear_right_temp_string,
        front_left_temp_string,
        front_right_temp_string,
    )


def prettyfy_status():
    # Header 7
    pass


def prettyfy_classification():
    # Header 8
    pass


def prettyfy_lobby():
    # Header 9
    pass


def prettyfy_damage(shared):
    # Header 10
    header = shared.header
    damage = shared.damage.statuses[header.player_car_index]

    _s1 = damage.tyre_rl_wear_percentage
    _s2 = damage.tyre_rr_wear_percentage
    _s3 = damage.tyre_fl_wear_percentage
    _s4 = damage.tyre_fr_wear_percentage

    rear_left_wear_string = f"{_s1:5.1f}%"
    rear_right_wear_string = f"{_s2:5.1f}%"
    front_left_wear_string = f"{_s3:5.1f}%"
    front_right_wear_string = f"{_s4:5.1f}%"

    return (
        rear_left_wear_string,
        rear_right_wear_string,
        front_left_wear_string,
        front_right_wear_string,
    )


def prettyfy_history():
    # Header 11
    pass


def prettyfy_tyres(shared):
    # Header 12
    header = shared.header
    try:
        tyres = shared.tyres[header.player_car_index]["tyre_sets_data"]
    except TypeError:
        softs, mediums, hards, inters = "", "", "", ""
        return softs, mediums, hards, inters

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
        return "", "", "", ""

    _s1 = count_new_inters
    _s2 = len(inters) - count_new_inters
    _s3 = humanise(best_inters.lap_delta_time)
    _s4 = best_inters.usable_life
    inters_string = f"Inters: {_s1} new, {_s2} used\n       {_s3} secs\n{_s4}"
    del _s1, _s2, _s3, _s4

    _s1 = count_new_softs
    _s2 = len(softs) - count_new_softs
    _s3 = humanise(best_softs.lap_delta_time)
    _s4 = best_softs.usable_life
    softs_string = f"Softs: {_s1} new, {_s2} used\n       {_s3} secs\n{_s4}"
    del _s1, _s2, _s3, _s4

    _s1 = count_new_mediums
    _s2 = len(mediums) - count_new_mediums
    _s3 = humanise(best_mediums.lap_delta_time)
    _s4 = best_mediums.usable_life
    mediums_string = f"Mediums: {_s1} new, {_s2} used\n       {_s3} secs\n{_s4}"
    del _s1, _s2, _s3, _s4

    _s1 = count_new_hards
    _s2 = len(hards) - count_new_hards
    _s3 = humanise(best_hards.lap_delta_time)
    _s4 = best_hards.usable_life
    hards_string = f"Hards: {_s1} new, {_s2} used\n       {_s3} secs\n{_s4}"
    del _s1, _s2, _s3, _s4

    return softs_string, mediums_string, hards_string, inters_string


def prettyfy_exmotion():
    # Header 13
    pass


def prettyfy_timetrial():
    # Header 14
    pass


def prettyfy_postitionhistory():
    # Header 15
    pass
