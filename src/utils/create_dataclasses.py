#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from dataclasses import dataclass, field

import rich
from loguru import logger

from models import classes, constants


@dataclass
class LapHistory:
    lap_time_ms: int | None = None
    sector1_time_ms_component: int | None = None
    sector1_time_minutes_component: int | None = None
    sector2_time_ms_component: int | None = None
    sector2_time_minutes_component: int | None = None
    sector3_time_ms_component: int | None = None
    sector3_time_minutes_component: int | None = None
    lap_valid_bit_flags: int | None = None


@dataclass
class TyreHistory:
    tyre_replaced_lap: int | None = None
    tyre_actual_compound: int | None = None
    tyre_visual_compound: int | None = None


@dataclass
class AvailableTyres:
    actual_tyre_compound: int | None = None
    visual_tyre_compound: int | None = None
    wear: int | None = None
    available: int | None = None
    recommended_session: int | None = None
    life_span: int | None = None
    usable_life: int | None = None
    lap_delta_time: int | None = None
    fitted: int | None = None


@dataclass
class Livery:
    livery_red: int | None = None
    livery_green: int | None = None
    livery_blue: int | None = None


@dataclass
class PenaltyInfo:
    penalty_type: int | None = None
    infringement_type: int | None = None
    car_id_of_criminal: int | None = None
    car_id_of_victim: int | None = None
    time_gained: int | None = None
    lap_number_of_offence: int | None = None
    places_gained: int | None = None


@dataclass
class CarData:
    # LapHistory fields
    number_of_laps_in_data: int | None = None
    number_of_tyre_stints: int | None = None
    best_lap_number: int | None = None
    best_s1_lap_number: int | None = None
    best_s2_lap_number: int | None = None
    best_s3_lap_number: int | None = None

    # Motion fields
    world_position_x: float | None = None
    world_position_y: float | None = None
    world_position_z: float | None = None
    world_velocity_x: float | None = None
    world_velocity_y: float | None = None
    world_velocity_z: float | None = None
    g_force_lateral: float | None = None
    g_force_longitudinal: float | None = None
    g_force_vertical: float | None = None
    yaw_radians: float | None = None
    pitch_radians: float | None = None
    roll_radians: float | None = None

    # LapData fields
    last_lap_time_ms: int | None = None
    current_lap_time_ms: int | None = None
    sector1_time_ms_component: int | None = None
    sector1_time_minutes_component: int | None = None
    sector2_time_ms_component: int | None = None
    sector2_time_minutes_component: int | None = None
    delta_to_car_in_front_ms_component: int | None = None
    delta_to_car_in_front_minutes_component: int | None = None
    delta_to_leader_ms_component: int | None = None
    delta_to_leader_minutes_component: int | None = None
    lap_distance_travelled_m: float | None = None
    session_distance_travelled_m: float | None = None
    safety_car_delta: float | None = None
    car_position: int | None = None
    current_lap_number: int | None = None
    pit_status: int | None = None
    number_of_pit_stops: int | None = None
    sector: int | None = None
    current_lap_invalid: int | None = None
    penalties: int | None = None
    total_warnings: int | None = None
    corner_cutting_warnings: int | None = None
    number_unserved_drive_through_pens: int | None = None
    number_unserved_stop_go_pens: int | None = None
    grid_position: int | None = None
    driver_status: int | None = None
    result_status: int | None = None
    pit_lane_timer_active: int | None = None
    pit_lane_time_ms: int | None = None
    pit_lane_stop_time_ms: int | None = None
    pit_stop_must_serve_pen: int | None = None
    fastest_speed_trap_speed_kph: float | None = None
    fastest_speed_trap_lap: int | None = None

    # CarStatus fields
    traction_control: int | None = None
    anti_lock_brakes: int | None = None
    fuel_mix: int | None = None
    front_brake_bias: int | None = None
    pit_limiter_status: int | None = None
    current_fuel_in_tank_kg: float | None = None
    fuel_capacity: float | None = None
    fuel_remaining_laps: float | None = None
    max_rpm: int | None = None
    idle_rpm: int | None = None
    max_gears: int | None = None
    drs_allowed: int | None = None
    drs_activated_in_distance: int | None = None
    actual_tyre_compound: int | None = None
    visual_tyre_compound: int | None = None
    tyre_age_laps: int | None = None
    vehicle_flags_shown: int | None = None
    engine_power_ice: float | None = None
    engine_power_mguk: float | None = None
    ers_store_energy: float | None = None
    ers_deploy_mode: int | None = None
    ers_harvested_mguk: float | None = None
    ers_harvested_mgu_h: float | None = None
    ers_deployed_this_lap: float | None = None

    # CarDamage fields
    tyre_wear_percentage: list[int] | None = None
    tyre_damage_percentage: list[int] | None = None
    brakes_damage_percentage: list[int] | None = None
    tyre_blisters_percentage: list[int] | None = None
    front_wing_damage_percentage: int | None = None
    rear_wing_damage_percentage: int | None = None
    floor_damage_percentage: int | None = None
    diffuser_damage_percentage: int | None = None
    sidepod_damage_percentage: int | None = None
    drs_fault: int | None = None
    ers_fault: int | None = None
    gearbox_damage_percentage: int | None = None
    engine_damage_percentage: int | None = None
    engine_mguh_wear_percentage: int | None = None
    engine_es_wear_percentage: int | None = None
    engine_ce_wear_percentage: int | None = None
    engine_ice_wear_percentage: int | None = None
    engine_mguk_wear_percentage: int | None = None
    engine_tc_wear_percentage: int | None = None
    engine_blown: int | None = None
    engine_seized: int | None = None

    # ParticipantData fields
    is_ai_controlled_flag: int | None = None
    driver_id: int | None = None
    network_id: int | None = None
    team_id: int | None = None
    my_team_flag: int | None = None
    race_number: int | None = None
    nationality: int | None = None
    name: str | None = None
    platform: int | None = None

    # EventDetails fields
    fastest_lap_flag: int | None = None
    fastest_lap_time: int | None = None
    retired_flag: int | None = None
    retired_reason: str | None = None
    teammate_in_pits_flag: int | None = None

    # SpeedtrapData fields
    speed_trap_speed: float | None = None
    is_fastest_speedtrap_flag: int | None = None

    # CollisionData fields
    collisions_with: int | None = None

    # CarSetup fields
    front_wing: int | None = None
    rear_wing: int | None = None
    on_throttle: int | None = None
    off_throttle: int | None = None
    front_camber: float | None = None
    rear_camber: float | None = None
    front_toe: float | None = None
    rear_toe: float | None = None
    front_suspension: int | None = None
    rear_suspension: int | None = None
    front_anti_roll_bar: int | None = None
    rear_anti_roll_bar: int | None = None
    front_suspension_height: int | None = None
    rear_suspension_height: int | None = None
    brake_pressure: int | None = None
    brake_bias: int | None = None
    engine_braking: int | None = None
    rear_left_tyre_pressure: float | None = None
    rear_right_tyre_pressure: float | None = None
    front_left_tyre_pressure: float | None = None
    front_right_tyre_pressure: float | None = None
    ballast: int | None = None
    fuel_load: float | None = None

    # CarTelemetry fields
    speed: int | None = None
    throttle: float | None = None
    steer: float | None = None
    brake: float | None = None
    clutch: int | None = None
    gear: int | None = None
    engine_rpm: int | None = None
    drs: int | None = None
    rev_lights_percent: int | None = None
    rev_lights_bit_value: int | None = None
    brakes_temperature: list[int] | None = None
    tyres_surface_temperature: list[int] | None = None
    tyres_inner_temperature: list[int] | None = None
    engine_temperature: int | None = None
    tyres_pressure: list[float] | None = None
    surface_type: list[int] | None = None
    current_tyre_index: int | None = None

    # Nested data structures
    lap_history: list[LapHistory] = field(
        default_factory=lambda: [LapHistory() for _ in range(100)]
    )
    tyre_history: list[TyreHistory] = field(
        default_factory=lambda: [TyreHistory() for _ in range(8)]
    )
    available_tyres: list[AvailableTyres] = field(
        default_factory=lambda: [AvailableTyres() for _ in range(20)]
    )
    livery: list[Livery] = field(default_factory=lambda: [Livery() for _ in range(5)])
    penalties: list[PenaltyInfo] = field(
        default_factory=lambda: [PenaltyInfo() for _ in range(10)]
    )


@dataclass
class AdminData:
    packet_format: int | None = None
    game_year: int | None = None
    game_major_version: int | None = None
    game_minor_version: int | None = None
    packet_version: int | None = None
    packet_id: int | None = None
    session_uuid: int | None = None
    session_time: float | None = None
    frame_id: int | None = None
    overall_frame: int | None = None
    player_car_index: int | None = None
    player2_car_index: int | None = None
    game_paused: int | None = None
    is_spectating: int | None = None
    spectator_car_index: int | None = None
    sli_pro_native_support: int | None = None
    network_game: int | None = None
    season_link_id: int | None = None
    weekend_link_id: int | None = None
    session_link_id: int | None = None


@dataclass
class SessionData:
    world_forward_direction_x: float | None = None
    world_forward_direction_y: float | None = None
    world_forward_direction_z: float | None = None
    world_right_direction_x: float | None = None
    world_right_direction_y: float | None = None
    world_right_direction_z: float | None = None
    weather: int | None = None
    track_temp_c: int | None = None
    air_temp_c: int | None = None
    total_race_laps: int | None = None
    track_length_m: int | None = None
    session_type: int | None = None
    track_id: int | None = None
    formula: int | None = None
    session_time_remaining_seconds: int | None = None
    session_duration_seconds: int | None = None
    pit_speed_limit_kph: int | None = None
    game_paused: int | None = None
    safety_car_status: int | None = None
    ai_difficulty_level: int | None = None
    pit_stop_ideal_lap: int | None = None
    pit_stop_latest_lap: int | None = None
    pit_stop_rejoin_position: int | None = None
    steering_assist: int | None = None
    braking_assist: int | None = None
    gearbox_assist: int | None = None
    pit_assist: int | None = None
    pit_release_assist: int | None = None
    ers_assist: int | None = None
    drs_assist: int | None = None
    dynamic_racing_line: int | None = None
    dynamic_racing_line_type: int | None = None
    game_mode: int | None = None
    ruleset: int | None = None
    time_of_day: int | None = None
    session_length: int | None = None
    speed_units_player1: int | None = None
    temp_units_player1: int | None = None
    speed_units_player2: int | None = None
    temp_units_player2: int | None = None
    number_of_safetycar_incidents: int | None = None
    number_of_virtualsafetycar_incidents: int | None = None
    number_of_red_flags: int | None = None
    equal_car_performance: int | None = None
    recovery_mode: int | None = None
    flashback_limit: int | None = None
    surface_type: int | None = None
    low_fuel_mode: int | None = None
    race_starts: int | None = None
    tyre_temps: int | None = None
    pit_lane_tyre_sim: int | None = None
    car_damage: int | None = None
    car_damage_rate: int | None = None
    collisions: int | None = None
    collisions_first_lap_only: int | None = None
    multiplayer_unsafe_pit_release: int | None = None
    multiplayer_kick_for_griefing: int | None = None
    corner_cutting_stringency: int | None = None
    parc_ferme: int | None = None
    pit_stop_experience: int | None = None
    safety_car: int | None = None
    safety_car_experience: int | None = None
    formation_lap: int | None = None
    formation_lap_experience: int | None = None
    red_flags: int | None = None
    sector_2_start_distance_m: int | None = None
    sector_3_start_distance_m: int | None = None
    safety_car_data: int | None = None
    drs_status: str | None = "Enabled"
    session_top_speedtrap: float | None = None
    session_top_speedtrap_driver: float | None = None

    # Marshal zones - using dict for dynamic field names
    marshal_zones: dict = field(default_factory=dict)

    def __post_init__(self):
        # Initialize marshal zones
        for i in range(1, 22):
            self.marshal_zones[f"marshal_zone_{i:02d}_start_at_lap_percentage"] = None
            self.marshal_zones[f"marshal_zone_{i:02d}_flag_type"] = None


def init_admin_data() -> AdminData:
    return AdminData()


def init_cars_data() -> dict:
    return {i: CarData() for i in range(22)}


def init_surrounding_cars_data() -> dict:
    # will use following indexes
    # 0: player1
    # 1: in front of player1
    # 2: behind player1
    # 3: player2
    # 4: in front of player2
    # 5: behind player2
    return {i: CarData() for i in range(6)}


def init_session_data() -> SessionData:
    return SessionData()


def update_with_motion(
    packet, session_data: SessionData, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 0
    session_data.world_forward_direction_x = packet["world_forward_direction_x"]
    session_data.world_forward_direction_y = packet["world_forward_direction_y"]
    session_data.world_forward_direction_z = packet["world_forward_direction_z"]
    session_data.world_right_direction_x = packet["world_right_direction_x"]
    session_data.world_right_direction_y = packet["world_right_direction_y"]
    session_data.world_right_direction_z = packet["world_right_direction_z"]
    car_data[player_index].world_position_x = packet["world_position_x"]
    car_data[player_index].world_position_y = packet["world_position_y"]
    car_data[player_index].world_position_z = packet["world_position_z"]
    car_data[player_index].world_velocity_x = packet["world_velocity_x"]
    car_data[player_index].world_velocity_y = packet["world_velocity_y"]
    car_data[player_index].world_velocity_z = packet["world_velocity_z"]
    car_data[player_index].g_force_lateral = packet["g_force_lateral"]
    car_data[player_index].g_force_longitudinal = packet["g_force_longitudinal"]
    car_data[player_index].g_force_vertical = packet["g_force_vertical"]
    car_data[player_index].yaw_radians = packet["yaw_radians"]
    car_data[player_index].pitch_radians = packet["pitch_radians"]
    car_data[player_index].roll_radians = packet["roll_radians"]


def update_with_sessiondata(
    packet, session_data: SessionData, fields: list[str]
) -> None:
    ## Packet Header of 1
    for field in fields:
        if field in packet:
            if field == "marshal_zones":
                marshal_zones = packet["list_of_marshal_zones"]
                for i, zone in enumerate(marshal_zones):
                    if i < 21:  # Max 21 marshal zones
                        session_data.marshal_zones[
                            f"marshal_zone_{i + 1:02d}_start_at_lap_percentage"
                        ] = zone.zone_start_at_lap_percentage
                        session_data.marshal_zones[
                            f"marshal_zone_{i + 1:02d}_flag_type"
                        ] = zone.zone_flag_type
            else:
                setattr(session_data, field, packet[field])


def update_with_lapdata(packet, car_data, surrounding_cars, user_idx, requested_data):
    sent_car_data = packet["cars"]
    two_players = user_idx[1] != 255
    target_positions = set()

    # Single pass to update positions
    for index, item in enumerate(sent_car_data):
        decoded_item = classes.LapData.from_buffer_copy(item)
        car_position = decoded_item.car_position
        car_data[index].car_position = car_position

    # Calculate target positions
    p1_pos = car_data[user_idx[0]].car_position
    target_positions.update([p1_pos, p1_pos - 1, p1_pos + 1])

    if two_players:
        p2_pos = car_data[user_idx[1]].car_position
        target_positions.update([p2_pos, p2_pos - 1, p2_pos + 1])

    target_positions = {x for x in target_positions if x > 0}

    # Update target cars
    for index, item in enumerate(sent_car_data):
        current_position = car_data[index].car_position
        if current_position in target_positions:
            decoded_item = classes.LapData.from_buffer_copy(item)
            # Batch process requested data
            updates = []
            for k in requested_data:
                try:
                    updates.append((k, getattr(decoded_item, k)))
                except AttributeError:
                    pass  # Skip attributes not in class

            # Apply updates efficiently
            for key, value in updates:
                if current_position == p1_pos:
                    setattr(surrounding_cars[0], key, value)
                try:
                    if current_position == p1_pos - 1:
                        setattr(surrounding_cars[1], key, value)
                except UnboundLocalError:
                    surrounding_cars[1] = surrounding_cars[0]
                try:
                    if current_position == p1_pos + 1:
                        setattr(surrounding_cars[2], key, value)
                except UnboundLocalError:
                    surrounding_cars[2] = surrounding_cars[0]
                if two_players:
                    if current_position == p2_pos:
                        setattr(surrounding_cars[3], key, value)
                    try:
                        if current_position == p2_pos - 1:
                            setattr(surrounding_cars[4], key, value)
                    except UnboundLocalError:
                        surrounding_cars[4] = surrounding_cars[3]
                    try:
                        if current_position == p2_pos + 1:
                            setattr(surrounding_cars[5], key, value)
                    except UnboundLocalError:
                        surrounding_cars[5] = surrounding_cars[3]


def update_with_event_data(
    packet, car_data: dict[int, CarData], session_data: SessionData
) -> None:
    ## Packet Header of 3
    event_type = packet["event_code_string"].decode("ascii")
    try:
        event_class = constants.EVENT_DICT[event_type]
        if isinstance(event_class, str):
            # Handle string events
            match event_class:
                case "SESSION_START":
                    pass
                case "SESSION_END":
                    pass
                case "DRS_ENABLED":
                    session_data.drs_status = "Enabled"
                case "CHEQUERED_FLAG":
                    pass
                case "LIGHTS_OUT":
                    pass
        else:
            # Handle class-based events
            event_data_obj = event_class.from_buffer_copy(packet["event_details"])
            event_data = {
                k: getattr(event_data_obj, k) for k, _ in event_data_obj._fields_
            }
            logger.debug(f"Event data: {event_data}")
            match event_type:
                case "FTLP":
                    for item in car_data.values():
                        item.fastest_lap_flag = 0
                    car_data[event_data["fastest_lap_car_id"]].fastest_lap_flag = 1
                    car_data[event_data["fastest_lap_car_id"]].fastest_lap_time = int(
                        event_data["fastest_lap_seconds"] * 1000
                    )
                case "RTMT":
                    car_data[event_data["retired_car_id"]].retired_flag = 1
                    car_data[event_data["retired_car_id"]].retired_reason = event_data[
                        "retirement_reason"
                    ]
                case "DRSD":
                    session_data.drs_status = (
                        f"Disabled: {event_data['drs_disabled_reason']}"
                    )
                case "TMPT":
                    car_data[
                        event_data["car_index_of_teammate"]
                    ].teammate_in_pits_flag = 1
                case "RCWN":
                    pass  # Race winner
                case "PENA":
                    penalty_info = PenaltyInfo()
                    penalty_info.penalty_type = event_data["penalty_type"]
                    penalty_info.infringement_type = event_data["infringement_type"]
                    penalty_info.car_id_of_criminal = event_data["car_id_of_criminal"]
                    penalty_info.car_id_of_victim = event_data["car_id_of_victim"]
                    penalty_info.time_gained = event_data["time_gained"]
                    penalty_info.lap_number_of_offence = event_data[
                        "lap_number_of_offence"
                    ]
                    penalty_info.places_gained = event_data["places_gained"]
                    car_data[event_data["car_id_of_criminal"]].penalties.append(
                        penalty_info
                    )
                case "SPTP":
                    if event_data["is_fastest_for_driver_session"] == 1:
                        car_data[event_data["car_id"]].speed_trap_speed = event_data[
                            "speed_kph"
                        ]
                    session_data.session_top_speedtrap = event_data[
                        "fastest_speed_in_session_kph"
                    ]
                    session_data.session_top_speedtrap_driver = event_data[
                        "car_id_of_fastest_in_session"
                    ]
                case "STLG":
                    pass  # Start lights
                case "DTSV":
                    pass  # Drive through penalty served
                case "SGSV":
                    pass  # Stop go penalty served
                case "FLBK":
                    pass  # Flashback
                case "BUTN":
                    pass  # Button pressed
    except KeyError:
        logger.debug(f"Unknown event type: {event_type}")
        return
    except AttributeError:
        logger.debug(f"Attribute error for event: {event_type}")
        return


def update_with_participants_data(
    packet, car_data: dict[int, CarData], session_data: SessionData
) -> None:
    ## Packet Header of 4
    sent_participants_data = packet["participant_data"]
    for index, item in enumerate(sent_participants_data):
        decoded_item = classes.ParticipantData.from_buffer_copy(item)
        # Convert to dict and update car data
        item_data = {k: getattr(decoded_item, k) for k, _ in decoded_item._fields_}
        # Handle special case for name (c_char array)
        item_data["name"] = item_data["name"].decode("utf-8").rstrip("\x00")
        for key, value in item_data.items():
            setattr(car_data[index], key, value)


def update_with_car_setup_data(
    packet, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 5
    car_setups = packet["car_setups"]
    player_setup = car_setups[player_index]
    decoded_setup = classes.CarSetupData.from_buffer_copy(player_setup)
    setup_data = {k: getattr(decoded_setup, k) for k, _ in decoded_setup._fields_}
    for key, value in setup_data.items():
        setattr(car_data[player_index], key, value)


def update_with_car_telemetry_data(
    packet, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 6
    telemetry_data = packet["car_telemetry_data"]
    player_telemetry = telemetry_data[player_index]
    decoded_telemetry = classes.CarTelemetryData.from_buffer_copy(player_telemetry)
    telemetry_dict = {
        k: getattr(decoded_telemetry, k) for k, _ in decoded_telemetry._fields_
    }
    # Handle arrays
    telemetry_dict["brakes_temperature"] = list(telemetry_dict["brakes_temperature"])
    telemetry_dict["tyres_surface_temperature"] = list(
        telemetry_dict["tyres_surface_temperature"]
    )
    telemetry_dict["tyres_inner_temperature"] = list(
        telemetry_dict["tyres_inner_temperature"]
    )
    telemetry_dict["tyres_pressure"] = list(telemetry_dict["tyres_pressure"])
    telemetry_dict["surface_type"] = list(telemetry_dict["surface_type"])

    for key, value in telemetry_dict.items():
        setattr(car_data[player_index], key, value)


def update_with_car_status_data(
    packet, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 7
    car_status_data = packet["cars"]
    player_status = car_status_data[player_index]
    decoded_status = classes.CarStatusData.from_buffer_copy(player_status)
    status_data = {k: getattr(decoded_status, k) for k, _ in decoded_status._fields_}
    for key, value in status_data.items():
        setattr(car_data[player_index], key, value)


def update_with_car_damage_data(
    packet, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 10
    car_damage_data = packet["cars"]
    player_damage = car_damage_data[player_index]
    decoded_damage = classes.CarDamageData.from_buffer_copy(player_damage)
    damage_data = {k: getattr(decoded_damage, k) for k, _ in decoded_damage._fields_}
    # Handle arrays
    damage_data["tyre_wear_percentage"] = [damage_data["tyre_wear_percentage"]] * 4
    damage_data["tyre_damage_percentage"] = [damage_data["tyre_damage_percentage"]] * 4
    damage_data["brakes_damage_percentage"] = [
        damage_data["brakes_damage_percentage"]
    ] * 4
    damage_data["tyre_blisters_percentage"] = [
        damage_data["tyre_blisters_percentage"]
    ] * 4

    for key, value in damage_data.items():
        setattr(car_data[player_index], key, value)


def update_with_session_history_data(
    packet, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 11

    car_data[player_index].number_of_laps_in_data = packet["number_of_laps_in_data"]
    car_data[player_index].number_of_tyre_stints = packet["number_of_tyre_stints"]
    car_data[player_index].best_lap_number = packet["best_lap_number"]
    car_data[player_index].best_s1_lap_number = packet["best_s1_lap_number"]
    car_data[player_index].best_s2_lap_number = packet["best_s2_lap_number"]
    car_data[player_index].best_s3_lap_number = packet["best_s3_lap_number"]

    # Update lap history
    lap_history_data = packet["lap_history_data"]
    for i, lap_data in enumerate(lap_history_data):
        if i < len(car_data[player_index].lap_history):
            decoded_lap = classes.LapHistoryPacket.from_buffer_copy(lap_data)
            lap_dict = {k: getattr(decoded_lap, k) for k, _ in decoded_lap._fields_}
            for key, value in lap_dict.items():
                setattr(car_data[player_index].lap_history[i], key, value)

    # Update tyre history
    tyre_history_data = packet["tyre_history_data"]
    for i, tyre_data in enumerate(tyre_history_data):
        if i < len(car_data[player_index].tyre_history):
            decoded_tyre = classes.TyreHistoryData.from_buffer_copy(tyre_data)
            tyre_dict = {k: getattr(decoded_tyre, k) for k, _ in decoded_tyre._fields_}
            for key, value in tyre_dict.items():
                setattr(car_data[player_index].tyre_history[i], key, value)


def update_with_tyre_sets_data(
    packet, car_data: dict[int, CarData], player_index: int
) -> None:
    ## Packet Header of 12
    tyre_set_data = packet["tyre_set_data"]
    for i, tyre_data in enumerate(tyre_set_data):
        if i < len(car_data[player_index].available_tyres):
            decoded_tyre = classes.TyreSetData.from_buffer_copy(tyre_data)
            tyre_dict = {k: getattr(decoded_tyre, k) for k, _ in decoded_tyre._fields_}
            for key, value in tyre_dict.items():
                setattr(car_data[player_index].available_tyres[i], key, value)


def main():
    cars_data = init_cars_data()
    rich.print(cars_data)


if __name__ == "__main__":
    main()
