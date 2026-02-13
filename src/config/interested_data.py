#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

from models import constants
from utils import udp_filter

state = udp_filter.get_shared_state()
session_dict = state.session_data

data_map = {
    # session_dict.world_forward_direction_x: {
    # "name": "World Forward (x)",
    # "value": str(session_dict.world_forward_direction_x),
    # },
    # session_dict.world_forward_direction_y: {
    # "name": "World Forward (y)",
    # "value": str(session_dict.world_forward_direction_y),
    # },
    # session_dict.world_forward_direction_z: {
    # "name": "World Forward (z)",
    # "value": str(session_dict.world_forward_direction_z),
    # },
    # session_dict.world_right_direction_x: {
    # "name": "",
    # "value": str(session_dict.world_right_direction_x),
    # },
    # session_dict.world_right_direction_y: {
    # "name": "",
    # "value": str(session_dict.world_right_direction_y),
    # },
    # session_dict.world_right_direction_z: {
    # "name": "",
    # "value": str(session_dict.world_right_direction_z),
    # },
    session_dict.weather: {
        "name": "Weather",
        "value": constants.WEATHER_TYPE_DICT[session_dict.weather],
    },
    # session_dict.track_temp_c: {"name": "", "value": str(session_dict.track_temp_c)},
    # session_dict.air_temp_c: {"name": "", "value": str(session_dict.air_temp_c)},
    # session_dict.total_race_laps: {
    # "name": "",
    # "value": str(session_dict.total_race_laps),
    # },
    # session_dict.track_length_m: {
    # "name": "",
    # "value": str(session_dict.track_length_m),
    # },
    # session_dict.session_type: {"name": "", "value": str(session_dict.session_type)},
    # session_dict.track_id: {"name": "", "value": str(session_dict.track_id)},
    # session_dict.formula: {"name": "", "value": str(session_dict.formula)},
    # session_dict.session_time_remaining_seconds: {
    # "name": "",
    # "value": str(session_dict.session_time_remaining_seconds),
    # },
    # session_dict.session_duration_seconds: {
    # "name": "",
    # "value": str(session_dict.session_duration_seconds),
    # },
    # session_dict.pit_speed_limit_kph: {
    # "name": "",
    # "value": str(session_dict.pit_speed_limit_kph),
    # },
    # session_dict.game_paused: {"name": "", "value": str(session_dict.game_paused)},
    # session_dict.safety_car_status: {
    # "name": "",
    # "value": str(session_dict.safety_car_status),
    # },
    # session_dict.ai_difficulty_level: {
    # "name": "",
    # "value": str(session_dict.ai_difficulty_level),
    # },
    # session_dict.pit_stop_ideal_lap: {
    # "name": "",
    # "value": str(session_dict.pit_stop_ideal_lap),
    # },
    # session_dict.pit_stop_latest_lap: {
    # "name": "",
    # "value": str(session_dict.pit_stop_latest_lap),
    # },
    # session_dict.pit_stop_rejoin_position: {
    # "name": "",
    # "value": str(session_dict.pit_stop_rejoin_position),
    # },
    # session_dict.steering_assist: {
    # "name": "",
    # "value": str(session_dict.steering_assist),
    # },
    # session_dict.braking_assist: {
    # "name": "",
    # "value": str(session_dict.braking_assist),
    # },
    # session_dict.gearbox_assist: {
    # "name": "",
    # "value": str(session_dict.gearbox_assist),
    # },
    # session_dict.pit_assist: {"name": "", "value": str(session_dict.pit_assist)},
    # session_dict.pit_release_assist: {
    # "name": "",
    # "value": str(session_dict.pit_release_assist),
    # },
    # session_dict.ers_assist: {"name": "", "value": str(session_dict.ers_assist)},
    # session_dict.drs_assist: {"name": "", "value": str(session_dict.drs_assist)},
    # session_dict.dynamic_racing_line: {
    # "name": "",
    # "value": str(session_dict.dynamic_racing_line),
    # },
    # session_dict.dynamic_racing_line_type: {
    # "name": "",
    # "value": str(session_dict.dynamic_racing_line_type),
    # },
    # session_dict.game_mode: {"name": "", "value": str(session_dict.game_mode)},
    # session_dict.ruleset: {"name": "", "value": str(session_dict.ruleset)},
    # session_dict.time_of_day: {"name": "", "value": str(session_dict.time_of_day)},
    # session_dict.session_length: {
    # "name": "",
    # "value": str(session_dict.session_length),
    # },
    # session_dict.speed_units_player1: {
    # "name": "",
    # "value": str(session_dict.speed_units_player1),
    # },
    # session_dict.temp_units_player1: {
    # "name": "",
    # "value": str(session_dict.temp_units_player1),
    # },
    # session_dict.speed_units_player2: {
    # "name": "",
    # "value": str(session_dict.speed_units_player2),
    # },
    # session_dict.temp_units_player2: {
    # "name": "",
    # "value": str(session_dict.temp_units_player2),
    # },
    # session_dict.number_of_safetycar_incidents: {
    # "name": "",
    # "value": str(session_dict.number_of_safetycar_incidents),
    # },
    # session_dict.number_of_virtualsafetycar_incidents: {
    # "name": "",
    # "value": str(session_dict.number_of_virtualsafetycar_incidents),
    # },
    # session_dict.number_of_red_flags: {
    # "name": "",
    # "value": str(session_dict.number_of_red_flags),
    # },
    # session_dict.equal_car_performance: {
    # "name": "",
    # "value": str(session_dict.equal_car_performance),
    # },
    # session_dict.recovery_mode: {"name": "", "value": str(session_dict.recovery_mode)},
    # session_dict.flashback_limit: {
    # "name": "",
    # "value": str(session_dict.flashback_limit),
    # },
    # session_dict.surface_type: {"name": "", "value": str(session_dict.surface_type)},
    # session_dict.low_fuel_mode: {"name": "", "value": str(session_dict.low_fuel_mode)},
    # session_dict.race_starts: {"name": "", "value": str(session_dict.race_starts)},
    # session_dict.tyre_temps: {"name": "", "value": str(session_dict.tyre_temps)},
    # session_dict.pit_lane_tyre_sim: {"name": "", "value": str(_dict.pit_lane_tyre_sim)},
    # session_dict.car_damage: {"name": "", "value": str(session_dict.car_damage)},
    # session_dict.car_damage_rate: {
    # "name": "",
    # "value": str(session_dict.car_damage_rate),
    # },
    # session_dict.collisions: {"name": "", "value": str(session_dict.collisions)},
    # session_dict.collisions_first_lap_only: {
    # "name": "",
    # "value": str(session_dict.collisions_first_lap_only),
    # },
    # session_dict.multiplayer_unsafe_pit_release: {
    # "name": "",
    # "value": str(session_dict.multiplayer_unsafe_pit_release),
    # },
    # session_dict.multiplayer_kick_for_griefing: {
    # "name": "",
    # "value": str(session_dict.multiplayer_kick_for_griefing),
    # },
    # session_dict.corner_cutting_stringency: {
    # "name": "",
    # "value": str(session_dict.corner_cutting_stringency),
    # },
    # session_dict.parc_ferme: {"name": "", "value": str(session_dict.parc_ferme)},
    # session_dict.pit_stop_experience: {
    # "name": "",
    # "value": str(session_dict.pit_stop_experience),
    # },
    # session_dict.safety_car: {"name": "", "value": str(session_dict.safety_car)},
    # session_dict.safety_car_experience: {
    # "name": "",
    # "value": str(session_dict.safety_car_experience),
    # },
    # session_dict.formation_lap: {"name": "", "value": str(session_dict.formation_lap)},
    # session_dict.formation_lap_experience: {
    # "name": "",
    # "value": str(session_dict.formation_lap_experience),
    # },
    # session_dict.red_flags: {"name": "", "value": str(session_dict.red_flags)},
    # session_dict.sector_2_start_distance_m: {
    # "name": "",
    # "value": str(session_dict.sector_2_start_distance_m),
    # },
    # session_dict.sector_3_start_distance_m: {
    # "name": "",
    # "value": str(session_dict.sector_3_start_distance_m),
    # },
    # session_dict.safety_car_data: {
    # "name": "",
    # "value": str(session_dict.safety_car_data),
    # },
    # session_dict.drs_status: {"name": "", "value": str(session_dict.drs_status)},
    # session_dict.session_top_speedtrap: {
    # "name": "",
    # "value": str(session_dict.session_top_speedtrap),
    # },
    # session_dict.session_top_speedtrap_driver: {
    # "name": "",
    # "value": str(session_dict.session_top_speedtrap_driver),
    # },
}
