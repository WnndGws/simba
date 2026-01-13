#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools

from ctypes import (
    LittleEndianStructure,
    Structure,
    c_char,
    c_float,
    c_int8,
    c_int16,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
)
from dataclasses import dataclass


class Header(LittleEndianStructure):
    # Need to specify packing
    # https://wumb0.in/a-better-way-to-work-with-raw-data-types-in-python.html
    _pack_ = 1
    _fields_ = [
        ("packet_format", c_uint16),
        ("game_year", c_uint8),
        ("game_major_version", c_uint8),
        ("game_minor_version", c_uint8),
        ("packet_version", c_uint8),
        ("packet_id", c_uint8),
        ("session_uuid", c_uint64),
        ("session_time", c_float),
        ("frame_id", c_uint32),
        ("overall_frame", c_uint32),
        ("player_car_index", c_uint8),
        ("player2_car_index", c_uint8),
    ]


class Motion(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", Header),
        ("world_position_x", c_float),
        ("world_position_y", c_float),
        ("world_position_z", c_float),
        ("world_velocity_x", c_float),
        ("world_velocity_y", c_float),
        ("world_velocity_z", c_float),
        ("world_forward_direction_x", c_int16),
        ("world_forward_direction_y", c_int16),
        ("world_forward_direction_z", c_int16),
        ("world_right_direction_x", c_int16),
        ("world_right_direction_y", c_int16),
        ("world_right_direction_z", c_int16),
        ("g_force_lateral", c_float),
        ("g_force_longitudinal", c_float),
        ("g_force_vertical", c_float),
        ("yaw_radians", c_float),
        ("pitch_radians", c_float),
        ("roll_radians", c_float),
    ]


class MartialZone(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("zone_start_at_lap_percentage", c_float), ("zone_flag_type", c_int8)]


class WeatherForcast(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("session_type", c_uint8),
        ("time_offset", c_uint8),
        ("weather", c_uint8),
        ("track_temp_c", c_int8),
        ("track_temp_change_c", c_int8),
        ("air_temp_c", c_int8),
        ("air_temp_change_c", c_int8),
        ("rain_percentage", c_uint8),
    ]


class SessionData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", Header),
        ("weather", c_uint8),
        ("track_temp_c", c_int8),
        ("air_temp_c", c_int8),
        ("total_race_laps", c_uint8),
        ("track_length_m", c_uint16),
        ("session_type", c_uint8),
        ("track_id", c_int8),
        ("formula", c_uint8),
        ("session_time_remaining_seconds", c_uint16),
        ("session_duration_seconds", c_uint16),
        ("pit_speed_limit_kph", c_uint8),
        ("game_paused", c_uint8),
        ("is_spectating", c_uint8),
        ("spectator_car_index", c_uint8),
        ("sli_pro_native_support", c_uint8),
        ("number_of_martial_zones", c_uint8),
        ("list_of_martial_zones", MartialZone * 21),
        ("safety_car_status", c_uint8),
        ("network_game", c_uint8),
        ("number_of_weather_forcast_samples", c_uint8),
        ("weather_forcasts", WeatherForcast * 64),
        ("weather_forecast_accuracy", c_uint8),
        ("ai_difficulty_level", c_uint8),
        ("season_link_id", c_uint32),
        ("weekend_link_id", c_uint32),
        ("session_link_id", c_uint32),
        ("pit_stop_ideal_lap", c_uint8),
        ("pit_stop_latest_lap", c_uint8),
        ("pit_stop_rejoin_position", c_uint8),
        ("steering_assist", c_uint8),
        ("braking_assist", c_uint8),
        ("gearbox_assist", c_uint8),
        ("pit_assist", c_uint8),
        ("pit_release_assist", c_uint8),
        ("ers_assist", c_uint8),
        ("drs_assist", c_uint8),
        ("dynamic_racing_line", c_uint8),
        ("dynamic_racing_line_type", c_uint8),
        ("game_mode", c_uint8),
        ("ruleset", c_uint8),
        ("time_of_day", c_uint32),
        ("session_length", c_uint8),
        ("speed_units_player1", c_uint8),
        ("temp_units_player1", c_uint8),
        ("speed_units_player2", c_uint8),
        ("temp_units_player2", c_uint8),
        ("number_of_safetycar_incidents", c_uint8),
        ("number_of_virtualsafetycar_incidents", c_uint8),
        ("number_of_red_flags", c_uint8),
        ("equal_car_performance", c_uint8),
        ("recovery_mode", c_uint8),
        ("flashback_limit", c_uint8),
        ("surface_type", c_uint8),
        ("low_fuel_mode", c_uint8),
        ("race_starts", c_uint8),
        ("tyre_temps", c_uint8),
        ("pit_lane_tyre_sim", c_uint8),
        ("car_damage", c_uint8),
        ("car_damage_rate", c_uint8),
        ("collisions", c_uint8),
        ("collisions_first_lap_only", c_uint8),
        ("multiplayer_unsafe_pit_release", c_uint8),
        ("multiplayer_kick_for_griefing", c_uint8),
        ("corner_cutting_stringency", c_uint8),
        ("parc_ferme", c_uint8),
        ("pit_stop_experience", c_uint8),
        ("safety_car", c_uint8),
        ("safety_car_experience", c_uint8),
        ("formation_lap", c_uint8),
        ("formation_lap_experience", c_uint8),
        ("red_flags", c_uint8),
        ("affects_licence_level_solo", c_uint8),
        ("affects_licence_level_multiplayer", c_uint8),
        ("number_of_sessions_in_weekend", c_uint8),
        ("weekend_structure", c_uint8 * 12),
        ("sector_2_start_distance_m", c_float),
        ("sector_3_start_distance_m", c_float),
    ]


class LapData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("last_lap_time_ms", c_uint32),
        ("current_lap_time_ms", c_uint32),
        ("sector1_time_ms_component", c_uint16),
        ("sector1_time_minutes_component", c_uint8),
        ("sector2_time_ms_component", c_uint16),
        ("sector2_time_minutes_component", c_uint8),
        ("delta_to_car_in_front_ms_component", c_uint16),
        ("delta_to_car_in_front_minutes_component", c_uint8),
        ("delta_to_leader_ms_component", c_uint16),
        ("delta_to_leader_minutes_component", c_uint8),
        ("lap_distance_travelled_m", c_float),
        ("session_distance_travelled_m", c_float),
        ("safety_car_delta", c_float),
        ("car_position", c_uint8),
        ("current_lap_number", c_uint8),
        ("pit_status", c_uint8),
        ("number_of_pit_stops", c_uint8),
        ("sector", c_uint8),
        ("current_lap_invalid", c_uint8),
        ("penalties", c_uint8),
        ("total_warnings", c_uint8),
        ("corner_cutting_warnings", c_uint8),
        ("number_unserved_drive_through_pens", c_uint8),
        ("number_unserved_stop_go_pens", c_uint8),
        ("grid_position", c_uint8),
        ("driver_status", c_uint8),
        ("result_status", c_uint8),
        ("pit_lane_timer_active", c_uint8),
        ("pit_lane_time_ms", c_uint16),
        ("pit_lane_stop_time_ms", c_uint16),
        ("pit_stop_must_serve_pen", c_uint8),
        ("fastest_speed_trap_speed_kph", c_float),
        ("fastest_speed_trap_lap", c_uint8),
    ]


class LapDataPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", Header),
        ("cars", LapData * 22),
        ("timetrial_pb", c_uint8),
        ("timetrial_rival_car_index", c_uint8),
    ]


class CarStatusData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("traction_control", c_uint8),
        ("anti_lock_brakes", c_uint8),
        ("fuel_mix", c_uint8),
        ("front_brake_bias", c_uint8),
        ("pit_limiter_status", c_uint8),
        ("current_fuel_in_tank_kg", c_float),
        ("fuel_capacity", c_float),
        ("fuel_remaining_laps", c_float),
        ("max_rpm", c_uint16),
        ("idle_rpm", c_uint16),
        ("max_gears", c_uint8),
        ("drs_allowed", c_uint8),
        ("drs_activated_in_distance", c_uint16),
        ("actual_tyre_compound", c_uint8),
        ("visual_tyre_compound", c_uint8),
        ("tyre_age_laps", c_uint8),
        ("vehicle_flags_shown", c_int8),
        ("engine_power_ice", c_float),
        ("engine_power_mguk", c_float),
        ("ers_store_energy", c_float),
        ("ers_deploy_mode", c_uint8),
        ("ers_harvested_mguk", c_float),
        ("ers_harvested_mgu_h", c_float),
        ("ers_deployed_this_lap", c_float),
        ("network_paused", c_uint8),
    ]


class CarStatusPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("header", Header), ("cars", CarStatusData * 22)]


class CarDamageData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("tyre_wear_percentage", c_float),
        ("tyre_damage_percentage", c_uint8),
        ("brakes_damage_percentage", c_uint8),
        ("tyre_blisters_percentage", c_uint8),
        ("front_wing_damage_percentage", c_uint8),
        ("rear_wing_damage_percentage", c_uint8),
        ("floor_damage_percentage", c_uint8),
        ("diffuser_damage_percentage", c_uint8),
        ("sidepod_damage_percentage", c_uint8),
        ("drs_fault", c_uint8),
        ("ers_fault", c_uint8),
        ("gearbox_damage_percentage", c_uint8),
        ("engine_damage_percentage", c_uint8),
        ("engine_mguh_wear_percentage", c_uint8),
        ("engine_es_wear_percentage", c_uint8),
        ("engine_ce_wear_percentage", c_uint8),
        ("engine_ice_wear_percentage", c_uint8),
        ("engine_mguk_wear_percentage", c_uint8),
        ("engine_tc_wear_percentage", c_uint8),
        ("engine_blown", c_uint8),
        ("engine_seized", c_uint8),
    ]


class CarDamagePacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("header", Header), ("cars", CarDamageData * 22)]


class LiveryColours(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("red", c_uint8),
        ("green", c_uint8),
        ("blue", c_uint8),
    ]


class ParticipantData(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("is_ai_controlled_flag", c_uint8),
        ("driver_id", c_uint8),
        ("network_id", c_uint8),
        ("team_id", c_uint8),
        ("my_team_flag", c_uint8),
        ("race_number", c_uint8),
        ("nationality", c_uint8),
        ("name", c_char * 32),
        ("network_telemetry_flag", c_uint8),
        ("show_online_names", c_uint8),
        ("f1_world_tech_level", c_uint16),
        ("platform", c_uint8),
        ("number_of_colours", c_uint8),
        ("livery_colours", LiveryColours * 4),
    ]


class ParticipantsPacket(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header", Header),
        ("number_of_active_cars", c_int8),
        ("participant_data", ParticipantData * 22),
    ]


@dataclass
class EventPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class CarSetupPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class CarTelemetryData:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class FinalClassificationPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class LobbyInfoPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class SessionHistoryPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class TyreSetsPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class ExtendedMotionPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class TimeTrialPacket:
    pass
    # TODO
    # non-relevant to what I want


@dataclass
class LapPositionPacket:
    pass
    # TODO
    # non-relevant to what I want
