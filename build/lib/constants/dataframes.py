#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import polars

session_info_dataframe = polars.DataFrame(
    {
        "key": [
            "session_type",
            "track_temp",
            "air_temp",
            "rain_percentage",
            "track_length_m",
            "total_race_laps",
            "session_duration_s",
            "session_time_remaining_s",
            "difficulty",
            "parc_ferme",
            "fastest_lap_driver",
            "fastest_lap_time",
        ],
        "value": ["", "", "", "", "", "", "", "", "", "", "", ""],
    }
)
race_timing_dataframe = polars.DataFrame(
    {
        "player": ["WG", "SG"],
        "current_lap_ms": [0, 0],
        "last_lap_ms": [0, 0],
        "s1_ms": [0, 0],
        "s2_ms": [0, 0],
        "s3_ms": [0, 0],
        "delta_to_front": [0, 0],
        "delta_to_leader": [0, 0],
        "position": [1, 2],
        "penalties": ["", ""],
        "total_warnings": [0, 0],
        "grid position": [1, 2],
        "driver_status": ["", ""],
        "fastest_speedtrap": [0, 0],
        "ideal_pitstop_lap": [0, 0],
        "latest_recommended_pitstop": [0, 0],
        "predicted_rejoin_position": [1, 2],
    }
)

car_info_dataframe = polars.DataFrame(
    {
        "player": ["WG", "SG"],
        "fuel_remaining_laps": [0, 0],
        "visual_tyre_compound": ["", ""],
        "tyre_age_laps": [0, 0],
        "tyre_wear_percentage": [0, 0],
        "tyre_blister_percentage": [0, 0],
        "front_wing_damage_percentage": [0, 0],
        "rear_wing_damage_percentage": [0, 0],
    }
)
