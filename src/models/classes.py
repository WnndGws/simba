#!/usr/bin/env python
## UDP data structures as laid out in EA documentation
## Generally use XxxxData for individual data
## Generally use XxxxPacket for collections of XxxxData

## All data is littleEndian
## le/ge values are just the c-types converted to bit length

from typing import Annotated

from pydantic import BaseModel, Field


class Header(BaseModel):
    packet_format: Annotated[int, Field(strict=True, ge=0, le=65535)]
    game_year: Annotated[int, Field(strict=True, ge=0, le=255)]
    game_major_version: Annotated[int, Field(strict=True, ge=0, le=255)]
    game_minor_version: Annotated[int, Field(strict=True, ge=0, le=255)]
    packet_version: Annotated[int, Field(strict=True, ge=0, le=255)]
    packet_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    session_uuid: Annotated[int, Field(strict=True, ge=0, le=18446744073709551615)]
    session_time: Annotated[float, Field(strict=True)]
    frame_id: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    overall_frame: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    player_car_index: Annotated[int, Field(strict=True, ge=0, le=255)]
    player2_car_index: Annotated[int, Field(strict=True, ge=0, le=255)]


class Motion(BaseModel):
    header: Header
    world_position_x: Annotated[float, Field(strict=True)]
    world_position_y: Annotated[float, Field(strict=True)]
    world_position_z: Annotated[float, Field(strict=True)]
    world_velocity_x: Annotated[float, Field(strict=True)]
    world_velocity_y: Annotated[float, Field(strict=True)]
    world_velocity_z: Annotated[float, Field(strict=True)]
    world_forward_direction_x: Annotated[int, Field(strict=True, ge=-32768, le=32767)]
    world_forward_direction_y: Annotated[int, Field(strict=True, ge=-32768, le=32767)]
    world_forward_direction_z: Annotated[int, Field(strict=True, ge=-32768, le=32767)]
    world_right_direction_x: Annotated[int, Field(strict=True, ge=-32768, le=32767)]
    world_right_direction_y: Annotated[int, Field(strict=True, ge=-32768, le=32767)]
    world_right_direction_z: Annotated[int, Field(strict=True, ge=-32768, le=32767)]
    g_force_lateral: Annotated[float, Field(strict=True)]
    g_force_longitudinal: Annotated[float, Field(strict=True)]
    g_force_vertical: Annotated[float, Field(strict=True)]
    yaw_radians: Annotated[float, Field(strict=True)]
    pitch_radians: Annotated[float, Field(strict=True)]
    roll_radians: Annotated[float, Field(strict=True)]


class MarshalZone(BaseModel):
    zone_start_at_lap_percentage: Annotated[float, Field(strict=True)]
    zone_flag_type: Annotated[int, Field(strict=True, ge=-128, le=127)]


class WeatherForcast(BaseModel):
    session_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    time_offset: Annotated[int, Field(strict=True, ge=0, le=255)]
    weather: Annotated[int, Field(strict=True, ge=0, le=255)]
    track_temp_c: Annotated[int, Field(strict=True, ge=-128, le=127)]
    track_temp_change_c: Annotated[int, Field(strict=True, ge=-128, le=127)]
    air_temp_c: Annotated[int, Field(strict=True, ge=-128, le=127)]
    air_temp_change_c: Annotated[int, Field(strict=True, ge=-128, le=127)]
    rain_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]


class SessionData(BaseModel):
    header: Header
    weather: Annotated[int, Field(strict=True, ge=0, le=255)]
    track_temp_c: Annotated[int, Field(strict=True, ge=-128, le=127)]
    air_temp_c: Annotated[int, Field(strict=True, ge=-128, le=127)]
    total_race_laps: Annotated[int, Field(strict=True, ge=0, le=255)]
    track_length_m: Annotated[int, Field(strict=True, ge=0, le=65535)]
    session_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    track_id: Annotated[int, Field(strict=True, ge=-128, le=127)]
    formula: Annotated[int, Field(strict=True, ge=0, le=255)]
    session_time_remaining_seconds: Annotated[int, Field(strict=True, ge=0, le=65535)]
    session_duration_seconds: Annotated[int, Field(strict=True, ge=0, le=65535)]
    pit_speed_limit_kph: Annotated[int, Field(strict=True, ge=0, le=255)]
    game_paused: Annotated[int, Field(strict=True, ge=0, le=255)]
    is_spectating: Annotated[int, Field(strict=True, ge=0, le=255)]
    spectator_car_index: Annotated[int, Field(strict=True, ge=0, le=255)]
    sli_pro_native_support: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_marshal_zones: Annotated[int, Field(strict=True, ge=0, le=255)]
    list_of_marshal_zones: list[MarshalZone] = Field(min_items=21, max_items=21)
    safety_car_status: Annotated[int, Field(strict=True, ge=0, le=255)]
    network_game: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_weather_forcast_samples: Annotated[int, Field(strict=True, ge=0, le=255)]
    weather_forcasts: list[WeatherForcast] = Field(min_items=64, max_items=64)
    weather_forecast_accuracy: Annotated[int, Field(strict=True, ge=0, le=255)]
    ai_difficulty_level: Annotated[int, Field(strict=True, ge=0, le=255)]
    season_link_id: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    weekend_link_id: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    session_link_id: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    pit_stop_ideal_lap: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_stop_latest_lap: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_stop_rejoin_position: Annotated[int, Field(strict=True, ge=0, le=255)]
    steering_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    braking_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    gearbox_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_release_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    ers_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    drs_assist: Annotated[int, Field(strict=True, ge=0, le=255)]
    dynamic_racing_line: Annotated[int, Field(strict=True, ge=0, le=255)]
    dynamic_racing_line_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    game_mode: Annotated[int, Field(strict=True, ge=0, le=255)]
    ruleset: Annotated[int, Field(strict=True, ge=0, le=255)]
    time_of_day: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    session_length: Annotated[int, Field(strict=True, ge=0, le=255)]
    speed_units_player1: Annotated[int, Field(strict=True, ge=0, le=255)]
    temp_units_player1: Annotated[int, Field(strict=True, ge=0, le=255)]
    speed_units_player2: Annotated[int, Field(strict=True, ge=0, le=255)]
    temp_units_player2: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_safetycar_incidents: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_virtualsafetycar_incidents: Annotated[
        int, Field(strict=True, ge=0, le=255)
    ]
    number_of_red_flags: Annotated[int, Field(strict=True, ge=0, le=255)]
    equal_car_performance: Annotated[int, Field(strict=True, ge=0, le=255)]
    recovery_mode: Annotated[int, Field(strict=True, ge=0, le=255)]
    flashback_limit: Annotated[int, Field(strict=True, ge=0, le=255)]
    surface_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    low_fuel_mode: Annotated[int, Field(strict=True, ge=0, le=255)]
    race_starts: Annotated[int, Field(strict=True, ge=0, le=255)]
    tyre_temps: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_lane_tyre_sim: Annotated[int, Field(strict=True, ge=0, le=255)]
    car_damage: Annotated[int, Field(strict=True, ge=0, le=255)]
    car_damage_rate: Annotated[int, Field(strict=True, ge=0, le=255)]
    collisions: Annotated[int, Field(strict=True, ge=0, le=255)]
    collisions_first_lap_only: Annotated[int, Field(strict=True, ge=0, le=255)]
    multiplayer_unsafe_pit_release: Annotated[int, Field(strict=True, ge=0, le=255)]
    multiplayer_kick_for_griefing: Annotated[int, Field(strict=True, ge=0, le=255)]
    corner_cutting_stringency: Annotated[int, Field(strict=True, ge=0, le=255)]
    parc_ferme: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_stop_experience: Annotated[int, Field(strict=True, ge=0, le=255)]
    safety_car: Annotated[int, Field(strict=True, ge=0, le=255)]
    safety_car_experience: Annotated[int, Field(strict=True, ge=0, le=255)]
    formation_lap: Annotated[int, Field(strict=True, ge=0, le=255)]
    formation_lap_experience: Annotated[int, Field(strict=True, ge=0, le=255)]
    red_flags: Annotated[int, Field(strict=True, ge=0, le=255)]
    affects_licence_level_solo: Annotated[int, Field(strict=True, ge=0, le=255)]
    affects_licence_level_multiplayer: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_sessions_in_weekend: Annotated[int, Field(strict=True, ge=0, le=255)]
    weekend_structure: list[int] = Field(min_items=12, max_items=12)
    sector_2_start_distance_m: Annotated[float, Field(strict=True)]
    sector_3_start_distance_m: Annotated[float, Field(strict=True)]


class LapData(BaseModel):
    last_lap_time_ms: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    current_lap_time_ms: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    sector1_time_ms_component: Annotated[int, Field(strict=True, ge=0, le=65535)]
    sector1_time_minutes_component: Annotated[int, Field(strict=True, ge=0, le=255)]
    sector2_time_ms_component: Annotated[int, Field(strict=True, ge=0, le=65535)]
    sector2_time_minutes_component: Annotated[int, Field(strict=True, ge=0, le=255)]
    delta_to_car_in_front_ms_component: Annotated[
        int, Field(strict=True, ge=0, le=65535)
    ]
    delta_to_car_in_front_minutes_component: Annotated[
        int, Field(strict=True, ge=0, le=255)
    ]
    delta_to_leader_ms_component: Annotated[int, Field(strict=True, ge=0, le=65535)]
    delta_to_leader_minutes_component: Annotated[int, Field(strict=True, ge=0, le=255)]
    lap_distance_travelled_m: Annotated[float, Field(strict=True)]
    session_distance_travelled_m: Annotated[float, Field(strict=True)]
    safety_car_delta: Annotated[float, Field(strict=True)]
    car_position: Annotated[int, Field(strict=True, ge=0, le=255)]
    current_lap_number: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_status: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_pit_stops: Annotated[int, Field(strict=True, ge=0, le=255)]
    sector: Annotated[int, Field(strict=True, ge=0, le=255)]
    current_lap_invalid: Annotated[int, Field(strict=True, ge=0, le=255)]
    penalties: Annotated[int, Field(strict=True, ge=0, le=255)]
    total_warnings: Annotated[int, Field(strict=True, ge=0, le=255)]
    corner_cutting_warnings: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_unserved_drive_through_pens: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_unserved_stop_go_pens: Annotated[int, Field(strict=True, ge=0, le=255)]
    grid_position: Annotated[int, Field(strict=True, ge=0, le=255)]
    driver_status: Annotated[int, Field(strict=True, ge=0, le=255)]
    result_status: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_lane_timer_active: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_lane_time_ms: Annotated[int, Field(strict=True, ge=0, le=65535)]
    pit_lane_stop_time_ms: Annotated[int, Field(strict=True, ge=0, le=65535)]
    pit_stop_must_serve_pen: Annotated[int, Field(strict=True, ge=0, le=255)]
    fastest_speed_trap_speed_kph: Annotated[float, Field(strict=True)]
    fastest_speed_trap_lap: Annotated[int, Field(strict=True, ge=0, le=255)]


class LapDataPacket(BaseModel):
    header: Header
    cars: list[LapData] = Field(min_items=22, max_items=22)
    timetrial_pb: Annotated[int, Field(strict=True, ge=0, le=255)]
    timetrial_rival_car_index: Annotated[int, Field(strict=True, ge=0, le=255)]


class LapHistoryData(BaseModel):
    lap_time_ms: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    sector1_time_ms_component: Annotated[int, Field(strict=True, ge=0, le=65535)]
    sector1_time_minutes_component: Annotated[int, Field(strict=True, ge=0, le=255)]
    sector2_time_ms_component: Annotated[int, Field(strict=True, ge=0, le=65535)]
    sector2_time_minutes_component: Annotated[int, Field(strict=True, ge=0, le=255)]
    sector3_time_ms_component: Annotated[int, Field(strict=True, ge=0, le=65535)]
    sector3_time_minutes_component: Annotated[int, Field(strict=True, ge=0, le=255)]
    lap_valid_bit_flags: Annotated[int, Field(strict=True, ge=0, le=255)]


class TyreHistoryData(BaseModel):
    tyre_replaced_lap: Annotated[int, Field(strict=True, ge=0, le=255)]
    tyre_actual_compound: Annotated[int, Field(strict=True, ge=0, le=255)]
    tyre_visual_compound: Annotated[int, Field(strict=True, ge=0, le=255)]


class LapHistoryPacket(BaseModel):
    header: Header
    relevant_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_laps_in_data: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_tyre_stints: Annotated[int, Field(strict=True, ge=0, le=255)]
    best_lap_number: Annotated[int, Field(strict=True, ge=0, le=255)]
    best_s1_lap_number: Annotated[int, Field(strict=True, ge=0, le=255)]
    best_s2_lap_number: Annotated[int, Field(strict=True, ge=0, le=255)]
    best_s3_lap_number: Annotated[int, Field(strict=True, ge=0, le=255)]
    lap_history_data: list[LapHistoryData] = Field(min_items=100, max_items=100)
    tyre_history_data: list[TyreHistoryData] = Field(min_items=8, max_items=8)


class CarStatusData(BaseModel):
    traction_control: Annotated[int, Field(strict=True, ge=0, le=255)]
    anti_lock_brakes: Annotated[int, Field(strict=True, ge=0, le=255)]
    fuel_mix: Annotated[int, Field(strict=True, ge=0, le=255)]
    front_brake_bias: Annotated[int, Field(strict=True, ge=0, le=255)]
    pit_limiter_status: Annotated[int, Field(strict=True, ge=0, le=255)]
    current_fuel_in_tank_kg: Annotated[float, Field(strict=True)]
    fuel_capacity: Annotated[float, Field(strict=True)]
    fuel_remaining_laps: Annotated[float, Field(strict=True)]
    max_rpm: Annotated[int, Field(strict=True, ge=0, le=65535)]
    idle_rpm: Annotated[int, Field(strict=True, ge=0, le=65535)]
    max_gears: Annotated[int, Field(strict=True, ge=0, le=255)]
    drs_allowed: Annotated[int, Field(strict=True, ge=0, le=255)]
    drs_activated_in_distance: Annotated[int, Field(strict=True, ge=0, le=65535)]
    actual_tyre_compound: Annotated[int, Field(strict=True, ge=0, le=255)]
    visual_tyre_compound: Annotated[int, Field(strict=True, ge=0, le=255)]
    tyre_age_laps: Annotated[int, Field(strict=True, ge=0, le=255)]
    vehicle_flags_shown: Annotated[int, Field(strict=True, ge=-128, le=127)]
    engine_power_ice: Annotated[float, Field(strict=True)]
    engine_power_mguk: Annotated[float, Field(strict=True)]
    ers_store_energy: Annotated[float, Field(strict=True)]
    ers_deploy_mode: Annotated[int, Field(strict=True, ge=0, le=255)]
    ers_harvested_mguk: Annotated[float, Field(strict=True)]
    ers_harvested_mgu_h: Annotated[float, Field(strict=True)]
    ers_deployed_this_lap: Annotated[float, Field(strict=True)]
    network_paused: Annotated[int, Field(strict=True, ge=0, le=255)]


class CarStatusPacket(BaseModel):
    header: Header
    cars: list[CarStatusData] = Field(min_items=22, max_items=22)


class CarDamageData(BaseModel):
    tyre_wear_percentage: Annotated[float, Field(strict=True)]
    tyre_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    brakes_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    tyre_blisters_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    front_wing_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    rear_wing_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    floor_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    diffuser_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    sidepod_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    drs_fault: Annotated[int, Field(strict=True, ge=0, le=255)]
    ers_fault: Annotated[int, Field(strict=True, ge=0, le=255)]
    gearbox_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_damage_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_mguh_wear_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_es_wear_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_ce_wear_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_ice_wear_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_mguk_wear_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_tc_wear_percentage: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_blown: Annotated[int, Field(strict=True, ge=0, le=255)]
    engine_seized: Annotated[int, Field(strict=True, ge=0, le=255)]


class CarDamagePacket(BaseModel):
    header: Header
    cars: list[CarDamageData] = Field(min_items=22, max_items=22)


class LiveryColours(BaseModel):
    red: Annotated[int, Field(strict=True, ge=0, le=255)]
    green: Annotated[int, Field(strict=True, ge=0, le=255)]
    blue: Annotated[int, Field(strict=True, ge=0, le=255)]


class ParticipantData(BaseModel):
    is_ai_controlled_flag: Annotated[int, Field(strict=True, ge=0, le=255)]
    driver_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    network_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    team_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    my_team_flag: Annotated[int, Field(strict=True, ge=0, le=255)]
    race_number: Annotated[int, Field(strict=True, ge=0, le=255)]
    nationality: Annotated[int, Field(strict=True, ge=0, le=255)]
    name: bytes
    network_telemetry_flag: Annotated[int, Field(strict=True, ge=0, le=255)]
    show_online_names: Annotated[int, Field(strict=True, ge=0, le=255)]
    f1_world_tech_level: Annotated[int, Field(strict=True, ge=0, le=65535)]
    platform: Annotated[int, Field(strict=True, ge=0, le=255)]
    number_of_colours: Annotated[int, Field(strict=True, ge=0, le=255)]
    livery_colours: list[LiveryColours] = Field(min_items=4, max_items=4)


class ParticipantsPacket(BaseModel):
    header: Header
    number_of_active_cars: Annotated[int, Field(strict=True, ge=-128, le=127)]
    participant_data: list[ParticipantData] = Field(min_items=22, max_items=22)


class FastestLapData(BaseModel):
    fastest_lap_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    fastest_lap_seconds: Annotated[float, Field(strict=True)]


class CarRetirementData(BaseModel):
    retired_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    retirement_reason: Annotated[int, Field(strict=True, ge=0, le=255)]


class DrsDisabledData(BaseModel):
    drs_disabled_reason: Annotated[int, Field(strict=True, ge=0, le=255)]


class TeammateInPitData(BaseModel):
    car_index_of_teammate: Annotated[int, Field(strict=True, ge=0, le=255)]


class RaceWinnerData(BaseModel):
    car_index_of_winner: Annotated[int, Field(strict=True, ge=0, le=255)]


class PenaltyData(BaseModel):
    penalty_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    infringement_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    car_id_of_criminal: Annotated[int, Field(strict=True, ge=0, le=255)]
    car_id_of_victim: Annotated[int, Field(strict=True, ge=0, le=255)]
    time_gained: Annotated[int, Field(strict=True, ge=0, le=255)]
    lap_number_of_offence: Annotated[int, Field(strict=True, ge=0, le=255)]
    places_gained: Annotated[int, Field(strict=True, ge=0, le=255)]


class SpeedTrapData(BaseModel):
    car_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    speed_kph: Annotated[float, Field(strict=True)]
    is_overall_fastest_in_session: Annotated[int, Field(strict=True, ge=0, le=255)]
    is_fastest_for_driver_session: Annotated[int, Field(strict=True, ge=0, le=255)]
    car_id_of_fastest_in_session: Annotated[int, Field(strict=True, ge=0, le=255)]
    fastest_speed_in_session_kph: Annotated[float, Field(strict=True)]


class StartLightsData(BaseModel):
    number_of_lights_lit: Annotated[int, Field(strict=True, ge=0, le=255)]


class DriveThroughPenaltyData(BaseModel):
    car_id_of_serving_car: Annotated[int, Field(strict=True, ge=0, le=255)]


class StopGoPenaltyServedData(BaseModel):
    car_id_of_serving_car: Annotated[int, Field(strict=True, ge=0, le=255)]


class FlashbackData(BaseModel):
    flashback_frame_id: Annotated[int, Field(strict=True, ge=0, le=4294967295)]
    flashback_to_time: Annotated[float, Field(strict=True)]


class ButtonPressedData(BaseModel):
    button_pressed: Annotated[int, Field(strict=True, ge=0, le=4294967295)]


class OvertakeData(BaseModel):
    overtaking_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    overtook_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]


class CollisionData(BaseModel):
    first_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]
    second_car_id: Annotated[int, Field(strict=True, ge=0, le=255)]


class SafetycarData(BaseModel):
    safety_car_type: Annotated[int, Field(strict=True, ge=0, le=255)]
    safety_car_status: Annotated[int, Field(strict=True, ge=0, le=255)]


class EventDetails(BaseModel):
    fastest_lap: FastestLapData | None = None
    retirement: CarRetirementData | None = None
    teammate_in_pits: TeammateInPitData | None = None
    race_winner: RaceWinnerData | None = None
    penalty_type: PenaltyData | None = None
    speedtrap: SpeedTrapData | None = None
    start_lights: StartLightsData | None = None
    drive_through_penalty_served: DriveThroughPenaltyData | None = None
    stop_go_penalty_served: StopGoPenaltyServedData | None = None
    flashback_info: FlashbackData | None = None
    button_pressed: ButtonPressedData | None = None


class EventPacket(BaseModel):
    header: Header
    event_code_string: bytes
    event_details: EventDetails


class CarSetupPacket(BaseModel):
    pass


class CarTelemetryData(BaseModel):
    pass


class FinalClassificationPacket(BaseModel):
    pass


class LobbyInfoPacket(BaseModel):
    pass


class SessionHistoryPacket(BaseModel):
    pass


class TyreSetsPacket(BaseModel):
    pass


class ExtendedMotionPacket(BaseModel):
    pass


class TimeTrialPacket(BaseModel):
    pass
