#!/usr/bin/env python
"""All info from https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-udp-specification/12187347"""

from typing import Final

import rich

from models import classes

PACKET_HEADER_LENGTH: Final[int] = 29  # <HBBBBBQfLLBB

GRID_SIZE: Final[int] = 22  # cars in the race

TIRE_COUNT: Final[int] = 4  # ruff insists

MAX_MARSHAL_ZONES: Final[int] = 21  # per track

MAX_WEATHER_SAMPLES: Final[int] = 56  # per session

MAX_TYRE_STINTS: Final[int] = 8  # per session

MAX_LAP_HISTORIES: Final[int] = 100  # per session

NULL_BYTE_VALUE: Final[int] = 255  # as per documentation

NAME_SIZE: Final[int] = 48  # max driver name len


# Where they don't have a class, its because I skipped them in the classes file
# This allows me to use it as a crude lookup-table to recursively decode them
PACKET_CLASS_DICT: Final[dict[int:type]] = {
    0: classes.Motion,
    1: classes.SessionData,
    2: classes.LapDataPacket,
    3: classes.EventPacket,
    4: classes.ParticipantsPacket,
    5: classes.CarSetupPacket,
    6: classes.CarTelemetryPacket,
    7: classes.CarStatusPacket,
    # 8: classes.FinalClassificationPacket,
    # 9: classes.LobbyInfoPacket,
    10: classes.CarDamagePacket,
    11: classes.SessionHistoryPacket,
    12: classes.TyreSetsPacket,
    # 13: classes.ExtendedMotionPacket
    # 14: classes.TimeTrialPacket
    # 15: classes.LapPositionsPacket
}

EVENT_DICT: Final[dict[str:type]] = {
    "SSTA": "SESSION_START",
    "SEND": "SESSION_END",
    "FTLP": classes.FastestLapData,
    "RTMT": classes.CarRetirementData,
    "DRSE": "DRS_ENABLED",
    "DRSD": classes.DrsDisabledData,
    "TMPT": classes.TeammateInPitData,
    "CHQF": "CHEQUERED_FLAG",
    "RCWN": classes.RaceWinnerData,
    "PENA": classes.PenaltyData,
    "SPTP": classes.SpeedTrapData,
    "STLG": classes.StartLightsData,
    "LGOT": "LIGHTS_OUT",
    "DTSV": classes.DriveThroughPenaltyData,
    "SGSV": classes.StopGoPenaltyServedData,
    "FLBK": classes.FlashbackData,
    "BUTN": classes.ButtonPressedData,
}

FORMULA_CLASSIFICATION_DICT: Final[dict[int:str]] = {
    0: "Modern F1",
    1: "Classic F1",
    2: "F2",
    3: "Generic F1",
    4: "Beta",
    6: "E-Sports",
    8: "F1 World",
    9: "F1 Elimination",
}

TEAM_ID_DICT: Final[dict[int:str]] = {
    0: "Mercedes",
    1: "Ferrari",
    2: "Red Bull Racing",
    3: "Williams",
    4: "Aston Martin",
    5: "Alpine",
    6: "RB",
    7: "Haas",
    8: "McLaren",
    9: "Sauber",
    41: "F1 Generic",
    104: "F1 Custom Team",
    129: "Konnersport",
    142: "APXGP 24",
    154: "APXGP 25",
    155: "Konnersport 24",
    158: "Art GP 24",
    159: "Campos 24",
    160: "Rodin Motorsport 24",
    161: "AIX Racing 24",
    162: "DAMS 24",
    163: "Hitech 24",
    164: "MP Motorsport 24",
    165: "Prema 24",
    166: "Trident 24",
    167: "Van Amersfoort Racing 24",
    168: "Invicta 24",
    185: "Mercedes 24",
    186: "Ferrari 24",
    187: "Red Bull Racing 24",
    188: "Williams 24",
    189: "Aston Martin 24",
    190: "Alpine 24",
    191: "RB 24",
    192: "Haas 24",
    193: "McLaren 24",
    194: "Sauber 24",
}


DRIVER_ID_DICT = {
    0: "Carlos Sainz",
    102: "Aidan Jackson",
    109: "Jenson Button",
    10: "Nico Hülkenburg",
    110: "David Coulthard",
    112: "Oscar Piastri",
    113: "Liam Lawson",
    116: "Richard Verschoor",
    11: "Kevin Magnussen",
    123: "Enzo Fittipaldi",
    125: "Mark Webber",
    126: "Jacques Villeneuve",
    127: "Callie Mayer",
    132: "Logan Sargeant",
    136: "Jack Doohan",
    137: "Amaury Cordeel",
    138: "Dennis Hauger",
    145: "Zane Maloney",
    146: "Victor Martins",
    147: "Oliver Bearman",
    148: "Jak Crawford",
    149: "Isack Hadjar",
    14: "Sergio Pérez",
    152: "Roman Stanek",
    153: "Kush Maini",
    156: "Brendon Leigh",
    157: "David Tonizza",
    158: "Jarno Opmeer",
    159: "Lucas Blakeley",
    15: "Valtteri Bottas",
    160: "Paul Aron",
    161: "Gabriel Bortoleto",
    162: "Franco Colapinto",
    163: "Taylor Barnard",
    164: "Joshua Dürksen",
    165: "Andrea-Kimi Antonelli",
    166: "Ritomo Miyata",
    167: "Rafael Villagómez",
    168: "Zak O`Sullivan",
    169: "Pepe Marti",
    170: "Sonny Hayes",
    171: "Joshua Pearce",
    172: "Callum Voisin",
    173: "Matias Zagazeta",
    174: "Nikola Tsolov",
    175: "Tim Tramnitz",
    17: "Esteban Ocon",
    185: "Luca Cortez",
    19: "Lance Stroll",
    20: "Arron Barnes",
    21: "Martin Giles",
    22: "Alex Murray",
    23: "Lucas Roth",
    24: "Igor Correia",
    25: "Sophie Levasseur",
    26: "Jonas Schiffer",
    27: "Alain Forest",
    28: "Jay Letourneau",
    29: "Esto Saari",
    2: "Daniel Ricciardo",
    30: "Yasar Atiyeh",
    31: "Callisto Calabresi",
    32: "Naota Izumi",
    33: "Howard Clarke",
    34: "Lars Kaufmann",
    35: "Marie Laursen",
    36: "Flavio Nieves",
    38: "Klimek Michalski",
    39: "Santiago Moreno",
    3: "Fernando Alonso",
    40: "Benjamin Coppens",
    41: "Noah Visser",
    4: "Felipe Massa",
    50: "George Russell",
    54: "Lando Norris",
    58: "Charles Leclerc",
    59: "Pierre Gasly",
    62: "Alexander Albon",
    70: "Rashid Nair",
    71: "Jack Tremblay",
    77: "Ayrton Senna",
    7: "Lewis Hamilton",
    80: "Guanyu Zhou",
    83: "Juan Manuel Correa",
    90: "Michael Schumacher",
    94: "Yuki Tsunoda",
    9: "Max Verstappen",
}

TRACK_DICT: Final[dict[int, str]] = {
    0: "Melbourne",
    2: "Shanghai",
    3: "Sakhir (Bahrain)",
    4: "Catalunya",
    5: "Monaco",
    6: "Montreal",
    7: "Silverstone",
    9: "Hungaroring",
    10: "Spa",
    11: "Monza",
    12: "Singapore",
    13: "Suzuka",
    14: "Abu Dhabi",
    15: "Texas",
    16: "Brazil",
    17: "Austria",
    19: "Mexico",
    20: "Baku (Azerbaijan)",
    26: "Zandvoort",
    27: "Imola",
    29: "Jeddah",
    30: "Miami",
    31: "Las Vegas",
    32: "Losail",
    39: "Silverstone (Reverse)",
    40: "Austria (Reverse)",
    41: "Zandvoort (Reverse)",
}


NATIONALITY_DICT: Final[dict[int, str]] = {
    1: "American",
    31: "Greek",
    61: "Paraguayan",
    2: "Argentinean",
    32: "Guatemalan",
    62: "Peruvian",
    3: "Australian",
    33: "Honduran",
    63: "Polish",
    4: "Austrian",
    34: "Hong Konger",
    64: "Portuguese",
    5: "Azerbaijani",
    35: "Hungarian",
    65: "Qatari",
    6: "Bahraini",
    36: "Icelander",
    66: "Romanian",
    7: "Belgian",
    37: "Indian",
    68: "Salvadoran",
    8: "Bolivian",
    38: "Indonesian",
    69: "Saudi",
    9: "Brazilian",
    39: "Irish",
    70: "Scottish",
    10: "British",
    40: "Israeli",
    71: "Serbian",
    11: "Bulgarian",
    41: "Italian",
    72: "Singaporean",
    12: "Cameroonian",
    42: "Jamaican",
    73: "Slovakian",
    13: "Canadian",
    43: "Japanese",
    74: "Slovenian",
    14: "Chilean",
    44: "Jordanian",
    75: "South Korean",
    15: "Chinese",
    45: "Kuwaiti",
    76: "South African",
    16: "Colombian",
    46: "Latvian",
    77: "Spanish",
    17: "Costa Rican",
    47: "Lebanese",
    78: "Swedish",
    18: "Croatian",
    48: "Lithuanian",
    79: "Swiss",
    19: "Cypriot",
    49: "Luxembourger",
    80: "Thai",
    20: "Czech",
    50: "Malaysian",
    81: "Turkish",
    21: "Danish",
    51: "Maltese",
    82: "Uruguayan",
    22: "Dutch",
    52: "Mexican",
    83: "Ukrainian",
    23: "Ecuadorian",
    53: "Monegasque",
    84: "Venezuelan",
    24: "English",
    54: "New Zealander",
    85: "Barbadian",
    25: "Emirian",
    55: "Nicaraguan",
    86: "Welsh",
    26: "Estonian",
    56: "Northern Irish",
    87: "Vietnamese",
    27: "Finnish",
    57: "Norwegian",
    88: "Algerian",
    28: "French",
    58: "Omani",
    89: "Bosnian",
    29: "German",
    59: "Pakistani",
    90: "Filipino",
    30: "Ghanaian",
    60: "Panamanian",
}

SPEED_UNIT_DICT: Final[dict[int, str]] = {
    0: "MPH",
    1: "KPH",
}

TEMPERATURE_UNIT_DICT: Final[dict[int, str]] = {
    0: "Celsius",
    1: "Fahrenheit",
}

EQUAL_CAR_PERFORMANCE_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "On",
}

RECOVERY_MODE_DICT: Final[dict[int, str]] = {
    0: "None",
    1: "Flashbacks",
    2: "Auto-recovery",
}

FLASHBACK_LIMIT_DICT: Final[dict[int, str]] = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Unlimited",
}

SURFACE_TYPE_DICT: Final[dict[int, str]] = {
    0: "Simplified",
    1: "Realistic",
}

LOW_FUEL_MODE_DICT: Final[dict[int, str]] = {
    0: "Easy",
    1: "Hard",
}

RACE_START_TYPE_DICT: Final[dict[int, str]] = {
    0: "Manual",
    1: "Assisted",
}

TYRE_TEMP_TYPE_DICT: Final[dict[int, str]] = {
    0: "Surface only",
    1: "Surface and Carcass",
}

PIT_LANE_TYRE_SIM_DICT: Final[dict[int, str]] = {
    0: "On",
    1: "Off",
}

CAR_DAMAGE_TYPE_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Reduced",
    2: "Standard",
    3: "Simulation",
}

CAR_DAMAGE_RATE_DICT: Final[dict[int, str]] = {
    0: "Reduced",
    1: "Standard",
    2: "Simulation",
}

COLLISIONS_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Player-to-Player",
    2: "On",
}

COLLISIONS_FIRST_LAP_DICT: Final[dict[int, str]] = {
    0: "Disabled",
    1: "Enabled",
}

UNSAFE_PIT_RELEASE_DICT: Final[dict[int, str]] = {
    0: "On",
    1: "Off",
}

KICK_FOR_GRIEFING_DICT: Final[dict[int, str]] = {
    0: "Disabled",
    1: "Enabled",
}

CORNER_CUTTING_STRINGENCY_DICT: Final[dict[int, str]] = {
    0: "Regular",
    1: "Strict",
}

PARC_FERME_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "On",
}

PIT_STOP_EXPERIENCE_DICT: Final[dict[int, str]] = {
    0: "Automatic",
    1: "Broadcast",
    2: "Immersive",
}

SAFETY_CAR_RATE_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Reduced",
    2: "Standard",
    3: "Increased",
}

SAFETY_CAR_STATUS_DICT: Final[dict[int, str]] = {
    0: "No Safety Car",
    1: "Full Safety Car",
    2: "Virtual Safety Car",
    3: "Formation Lap",
}

NETWORK_GAME_STATUS_DICT: Final[dict[int, str]] = {
    0: "Offline",
    1: "Online",
}

WEATHER_FORCAST_ACCURACY_DICT: Final[dict[int, str]] = {
    0: "Perfect",
    1: "Approximate",
}

ASSIT_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "On",
}

BRAKING_ASSIT_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Low",
    2: "Medium",
    3: "High",
}

GEARBOX_ASSIT_DICT: Final[dict[int, str]] = {
    1: "Manual",
    2: "Manual and Suggested Gear",
    3: "Automatic",
}

DYNAMIC_RACING_LINE_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Corners Only",
    2: "Full",
}

DYNAMIC_RACING_LINE_TYPE_DICT: Final[dict[int, str]] = {
    0: "2D",
    1: "3D",
}

LAP_VALID_DICT: Final[dict[int, str]] = {
    0: "Valid",
    1: "Invalid",
}

DRIVER_STATUS_DICT: Final[dict[int, str]] = {
    0: "In Garage",
    1: "Flying Lap",
    2: "In Lap",
    3: "Out Lap",
    4: "On Track",
}

RESULT_STATUS_DICT: Final[dict[int, str]] = {
    0: "Invalid",
    1: "Inactive",
    2: "Active",
    3: "Finished",
    4: "DNF",
    5: "Disqualified",
    6: "Not Classified",
    7: "Retired",
}

TRACTION_CONTROL_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Medium",
    2: "Full",
}

ANTI_LOCK_BRAKES_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "On",
}

FUEL_MIX_DICT: Final[dict[int, str]] = {
    0: "Lean",
    1: "Standard",
    2: "Rich",
    3: "Max",
}

PIT_LIMITER_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "On",
}

TYRE_COMPOUND_DICT: Final[dict[int, str]] = {
    16: "C5",
    17: "C4",
    18: "C3",
    19: "C2",
    20: "C1",
    21: "C0",
    22: "C6",
    7: "Inter",
    8: "Wet",
}

TYRE_VISUAL_DICT: Final[dict[int, str]] = {
    16: "Soft",
    17: "Medium",
    18: "Hard",
    7: "Inter",
    8: "Wet",
}

VEHICLE_FLAG_SHOWN_DICT: Final[dict[int, str]] = {
    0: "None",
    1: "Green",
    2: "Blue",
    3: "Yellow",
}

FAULT_DICT: Final[dict[int, str]] = {
    0: "OK",
    1: "Fault",
}

PIT_STATUS_DICT: Final[dict[int, str]] = {
    0: "None",
    1: "Pitting",
    2: "In Pit",
}

SECTOR_NUMBER_DICT: Final[dict[int, str]] = {
    0: "S1",
    1: "S2",
    2: "S3",
}

RED_FLAG_RATES_DICT: Final[dict[int, str]] = {
    0: "Off",
    1: "Reduced",
    2: "Standard",
    3: "Increased",
}

SESSION_LENGTH_DICT: Final[dict[int, str]] = {
    0: "None",
    2: "Very Short",
    3: "Short",
    4: "Medium",
    5: "Medium Long",
    6: "Long",
    7: "Full",
}

SESSION_TYPE_DICT: Final[dict[int, str]] = {
    0: "Unknown",
    1: "Practice 1",
    2: "Practice 2",
    3: "Practice 3",
    4: "Short Practice",
    5: "Qualifying 1",
    6: "Qualifying 2",
    7: "Qualifying 3",
    8: "Short Qualifying",
    9: "One-Shot Qualifying",
    10: "Sprint Shootout 1",
    11: "Sprint Shootout 2",
    12: "Sprint Shootout 3",
    13: "Short Sprint Shootout",
    14: "One-Shot Sprint Shootout",
    15: "Race",
    16: "Race 2",
    17: "Race 3",
    18: "Time Trial",
}

RULESET_TYPE_DICT: Final[dict[int, str]] = {
    0: "Practice and Qualifying",
    1: "Race",
    2: "Time Trial",
    12: "Elimination",
}

SURFACE_TYPE_DICT: Final[dict[int, str]] = {
    0: "Tarmac",
    1: "Rumble strip",
    2: "Concrete",
    3: "Rock",
    4: "Gravel",
    5: "Mud",
    6: "Sand",
    7: "Grass",
    8: "Water",
    9: "Cobblestone",
    10: "Metal",
    11: "Ridged",
}

PENALTY_TYPE_DICT: Final[dict[int, str]] = {
    0: "Drive through",
    1: "Stop Go",
    2: "Grid penalty",
    3: "Penalty reminder",
    4: "Time penalty",
    5: "Warning",
    6: "Disqualified",
    7: "Removed from formation lap",
    8: "Parked too long timer",
    9: "Tyre regulations",
    10: "This lap invalidated",
    11: "This and next lap invalidated",
    12: "This lap invalidated without reason",
    13: "This and next lap invalidated without reason",
    14: "This and previous lap invalidated",
    15: "This and previous lap invalidated without reason",
    16: "Retired",
    17: "Black flag time",
}

FLAG_TYPE_DICT: Final[dict[int, str]] = {
    0: "None",
    1: "Green",
    2: "Blue",
    3: "Yellow",
}

WEATHER_TYPE_DICT: Final[dict[int, str]] = {
    0: "Clear",
    1: "Light Cloud",
    2: "Overcast",
    3: "Light Rain",
    4: "Heavy Rain",
    5: "Stormy",
}

INFRINGEMENT_TYPE_DICT: Final[dict[int, str]] = {
    0: "Blocking by slow driving",
    1: "Blocking by wrong way driving",
    2: "Reversing off the start line",
    3: "Big Collision",
    4: "Small Collision",
    5: "Collision failed to hand back position single",
    6: "Collision failed to hand back position multiple",
    7: "Corner cutting gained time",
    8: "Corner cutting overtake single",
    9: "Corner cutting overtake multiple",
    10: "Crossed pit exit lane",
    11: "Ignoring blue flags",
    12: "Ignoring yellow flags",
    13: "Ignoring drive through",
    14: "Too many drive throughs",
    15: "Drive through reminder serve within n laps",
    16: "Drive through reminder serve this lap",
    17: "Pit lane speeding",
    18: "Parked for too long",
    19: "Ignoring tyre regulations",
    20: "Too many penalties",
    21: "Multiple warnings",
    22: "Approaching disqualification",
    23: "Tyre regulations select single",
    24: "Tyre regulations select multiple",
    25: "Lap invalidated corner cutting",
    26: "Lap invalidated running wide",
    27: "Corner cutting ran wide gained time minor",
    28: "Corner cutting ran wide gained time significant",
    29: "Corner cutting ran wide gained time extreme",
    30: "Lap invalidated wall riding",
    31: "Lap invalidated flashback used",
    32: "Lap invalidated reset to track",
    33: "Blocking the pitlane",
    34: "Jump start",
    35: "Safety car to car collision",
    36: "Safety car illegal overtake",
    37: "Safety car exceeding allowed pace",
    38: "Virtual safety car exceeding allowed pace",
    39: "Formation lap below allowed speed",
    40: "Formation lap parking",
    41: "Retired mechanical failure",
    42: "Retired terminally damaged",
    43: "Safety car falling too far back",
    44: "Black flag timer",
    45: "Unserved stop go penalty",
    46: "Unserved drive through penalty",
    47: "Engine component change",
    48: "Gearbox change",
    49: "Parc Fermé change",
    50: "League grid penalty",
    51: "Retry penalty",
    52: "Illegal time gain",
    53: "Mandatory pitstop",
    54: "Attribute assigned",
}

DATA_TO_HEADER_DICT = {
    "actual_tyre_compound": 12,  # TyreSetsPacket
    "ai_difficulty_level": 1,  # SessionData
    "air_temp_c": 1,  # SessionData
    "anti_lock_brakes": 5,  # CarSetupPacket
    "available": 12,  # TyreSetsPacket
    "ballast": 5,  # CarSetupPacket
    "best_lap_number": 11,  # SessionHistoryPacket
    "best_s1_lap_number": 11,  # SessionHistoryPacket
    "best_s2_lap_number": 11,  # SessionHistoryPacket
    "best_s3_lap_number": 11,  # SessionHistoryPacket
    "brake": 6,  # CarTelemetryPacket
    "brake_bias": 5,  # CarSetupPacket
    "brake_pressure": 5,  # CarSetupPacket
    "brakes_damage_percentage": 10,  # CarDamagePacket
    "brakes_temperature": 6,  # CarTelemetryPacket
    "braking_assist": 1,  # SessionData
    "car_damage": 1,  # SessionData
    "car_damage_rate": 1,  # SessionData
    "car_id_of_criminal": 3,  # EventPacket (PenaltyData)
    "car_id_of_victim": 3,  # EventPacket (PenaltyData)
    "car_position": 2,  # LapDataPacket
    "clutch": 6,  # CarTelemetryPacket
    "collisions": 1,  # SessionData
    "collisions_first_lap_only": 1,  # SessionData
    "corner_cutting_stringency": 1,  # SessionData
    "corner_cutting_warnings": 2,  # LapDataPacket
    "current_fuel_in_tank_kg": 7,  # CarStatusPacket
    "current_lap_invalid": 2,  # LapDataPacket
    "current_lap_number": 2,  # LapDataPacket
    "current_lap_time_ms": 2,  # LapDataPacket
    "current_tyre_index": 12,  # TyreSetsPacket
    "delta_to_car_in_front_minutes_component": 2,  # LapDataPacket
    "delta_to_car_in_front_ms_component": 2,  # LapDataPacket
    "delta_to_leader_minutes_component": 2,  # LapDataPacket
    "delta_to_leader_ms_component": 2,  # LapDataPacket
    "delta_to_car_behind_ms": 2,  # LapDataPacket
    "diffuser_damage_percentage": 10,  # CarDamagePacket
    "driver_id": 4,  # ParticipantsPacket
    "driver_status": 2,  # LapDataPacket
    "drs": 6,  # CarTelemetryPacket
    "drs_activated_in_distance": 7,  # CarStatusPacket
    "drs_allowed": 7,  # CarStatusPacket
    "drs_assist": 1,  # SessionData
    "drs_fault": 10,  # CarDamagePacket
    "drs_status": 1,  # SessionData
    "dynamic_racing_line": 1,  # SessionData
    "dynamic_racing_line_type": 1,  # SessionData
    "engine_blown": 10,  # CarDamagePacket
    "engine_braking": 5,  # CarSetupPacket
    "engine_ce_wear_percentage": 10,  # CarDamagePacket
    "engine_damage_percentage": 10,  # CarDamagePacket
    "engine_es_wear_percentage": 10,  # CarDamagePacket
    "engine_ice_wear_percentage": 10,  # CarDamagePacket
    "engine_mguh_wear_percentage": 10,  # CarDamagePacket
    "engine_mguk_wear_percentage": 10,  # CarDamagePacket
    "engine_power_ice": 7,  # CarStatusPacket
    "engine_power_mguk": 7,  # CarStatusPacket
    "engine_rpm": 6,  # CarTelemetryPacket
    "engine_seized": 10,  # CarDamagePacket
    "engine_tc_wear_percentage": 10,  # CarDamagePacket
    "engine_temperature": 6,  # CarTelemetryPacket
    "equal_car_performance": 1,  # SessionData
    "ers_assist": 1,  # SessionData
    "ers_deploy_mode": 7,  # CarStatusPacket
    "ers_fault": 10,  # CarDamagePacket
    "ers_harvested_mgu_h": 7,  # CarStatusPacket
    "ers_harvested_mguk": 7,  # CarStatusPacket
    "ers_store_energy": 7,  # CarStatusPacket
    "fastest_lap_flag": 3,  # EventPacket (FastestLapData)
    "fastest_lap_time": 11,  # SessionHistoryPacket
    "fastest_speed_trap_lap": 2,  # LapDataPacket
    "fastest_speed_trap_speed_kph": 2,  # LapDataPacket
    "flashback_limit": 1,  # SessionData
    "floor_damage_percentage": 10,  # CarDamagePacket
    "formation_lap": 1,  # SessionData
    "formation_lap_experience": 1,  # SessionData
    "formula": 1,  # SessionData
    "frame_id": 0,  # Header (in all packets)
    "front_anti_roll_bar": 5,  # CarSetupPacket
    "front_brake_bias": 7,  # CarStatusPacket
    "front_camber": 5,  # CarSetupPacket
    "front_left_tyre_pressure": 5,  # CarSetupPacket
    "front_right_tyre_pressure": 5,  # CarSetupPacket
    "front_suspension": 5,  # CarSetupPacket
    "front_suspension_height": 5,  # CarSetupPacket
    "front_toe": 5,  # CarSetupPacket
    "front_wing": 5,  # CarSetupPacket
    "front_wing_damage_percentage": 10,  # CarDamagePacket
    "fuel_capacity": 7,  # CarStatusPacket
    "fuel_load": 5,  # CarSetupPacket
    "fuel_mix": 7,  # CarStatusPacket
    "fuel_remaining_laps": 7,  # CarStatusPacket
    "g_force_lateral": 0,  # Motion
    "g_force_longitudinal": 0,  # Motion
    "g_force_vertical": 0,  # Motion
    "game_major_version": 0,  # Header (in all packets)
    "game_minor_version": 0,  # Header (in all packets)
    "game_mode": 1,  # SessionData
    "game_paused": 1,  # SessionData
    "game_year": 0,  # Header (in all packets)
    "gear": 6,  # CarTelemetryPacket
    "gearbox_assist": 1,  # SessionData
    "gearbox_damage_percentage": 10,  # CarDamagePacket
    "grid_position": 2,  # LapDataPacket
    "idle_rpm": 7,  # CarStatusPacket
    "infringement_type": 3,  # EventPacket (PenaltyData)
    "is_ai_controlled_flag": 4,  # ParticipantsPacket
    "is_fastest_speedtrap_flag": 2,  # LapDataPacket
    "is_spectating": 1,  # SessionData
    "lap_delta_time": 12,  # TyreSetsPacket
    "lap_distance_travelled_m": 2,  # LapDataPacket
    "lap_number_of_offence": 3,  # EventPacket (PenaltyData)
    "lap_time_ms": 11,  # SessionHistoryPacket
    "lap_valid_bit_flags": 11,  # SessionHistoryPacket
    "last_lap_time_ms": 2,  # LapDataPacket
    "life_span": 12,  # TyreSetsPacket
    "livery_blue": 4,  # ParticipantsPacket
    "livery_green": 4,  # ParticipantsPacket
    "livery_red": 4,  # ParticipantsPacket
    "low_fuel_mode": 1,  # SessionData
    "marshal_zones": 1,  # SessionData
    "max_gears": 7,  # CarStatusPacket
    "max_rpm": 7,  # CarStatusPacket
    "multiplayer_kick_for_griefing": 1,  # SessionData
    "multiplayer_unsafe_pit_release": 1,  # SessionData
    "my_team_flag": 4,  # ParticipantsPacket
    "name": 4,  # ParticipantsPacket
    "nationality": 4,  # ParticipantsPacket
    "network_game": 1,  # SessionData
    "network_id": 4,  # ParticipantsPacket
    "number_of_laps_in_data": 11,  # SessionHistoryPacket
    "number_of_pit_stops": 2,  # LapDataPacket
    "number_of_red_flags": 1,  # SessionData
    "number_of_safetycar_incidents": 1,  # SessionData
    "number_of_tyre_stints": 11,  # SessionHistoryPacket
    "number_of_virtualsafetycar_incidents": 1,  # SessionData
    "number_unserved_drive_through_pens": 2,  # LapDataPacket
    "number_unserved_stop_go_pens": 2,  # LapDataPacket
    "off_throttle": 5,  # CarSetupPacket
    "on_throttle": 5,  # CarSetupPacket
    "overall_frame": 0,  # Header (in all packets)
    "packet_format": 0,  # Header (in all packets)
    "packet_id": 0,  # Header (in all packets)
    "packet_version": 0,  # Header (in all packets)
    "parc_ferme": 1,  # SessionData
    "penalties": 2,  # LapDataPacket
    "penalty_type": 3,  # EventPacket (PenaltyData)
    "pit_assist": 1,  # SessionData
    "pit_lane_stop_time_ms": 2,  # LapDataPacket
    "pit_lane_time_ms": 2,  # LapDataPacket
    "pit_lane_timer_active": 2,  # LapDataPacket
    "pit_lane_tyre_sim": 1,  # SessionData
    "pit_limiter_status": 7,  # CarStatusPacket
    "pit_release_assist": 1,  # SessionData
    "pit_speed_limit_kph": 1,  # SessionData
    "pit_status": 2,  # LapDataPacket
    "pit_stop_experience": 1,  # SessionData
    "pit_stop_ideal_lap": 1,  # SessionData
    "pit_stop_latest_lap": 1,  # SessionData
    "pit_stop_must_serve_pen": 2,  # LapDataPacket
    "pit_stop_rejoin_position": 1,  # SessionData
    "pitch_radians": 0,  # Motion
    "places_gained": 3,  # EventPacket (PenaltyData)
    "platform": 4,  # ParticipantsPacket
    "player2_car_index": 0,  # Header (in all packets)
    "player_car_index": 0,  # Header (in all packets)
    "race_number": 4,  # ParticipantsPacket
    "race_starts": 1,  # SessionData
    "rear_anti_roll_bar": 5,  # CarSetupPacket
    "rear_camber": 5,  # CarSetupPacket
    "rear_left_tyre_pressure": 5,  # CarSetupPacket
    "rear_right_tyre_pressure": 5,  # CarSetupPacket
    "rear_suspension": 5,  # CarSetupPacket
    "rear_suspension_height": 5,  # CarSetupPacket
    "rear_toe": 5,  # CarSetupPacket
    "rear_wing": 5,  # CarSetupPacket
    "rear_wing_damage_percentage": 10,  # CarDamagePacket
    "recommended_session": 12,  # TyreSetsPacket
    "recovery_mode": 1,  # SessionData
    "red_flags": 1,  # SessionData
    "result_status": 2,  # LapDataPacket
    "retired_flag": 3,  # EventPacket (CarRetirementData)
    "retired_reason": 3,  # EventPacket (CarRetirementData)
    "rev_lights_bit_value": 6,  # CarTelemetryPacket
    "rev_lights_percent": 6,  # CarTelemetryPacket
    "roll_radians": 0,  # Motion
    "ruleset": 1,  # SessionData
    "safety_car": 1,  # SessionData
    "safety_car_data": 3,  # EventPacket (SafetycarData)
    "safety_car_delta": 2,  # LapDataPacket
    "safety_car_experience": 1,  # SessionData
    "safety_car_status": 1,  # SessionData
    "season_link_id": 1,  # SessionData
    "sector": 2,  # LapDataPacket
    "sector1_time_minutes_component": 2,  # LapDataPacket
    "sector1_time_ms_component": 2,  # LapDataPacket
    "sector2_time_minutes_component": 2,  # LapDataPacket
    "sector2_time_ms_component": 2,  # LapDataPacket
    "sector3_time_minutes_component": 11,  # SessionHistoryPacket
    "sector3_time_ms_component": 11,  # SessionHistoryPacket
    "sector_2_start_distance_m": 1,  # SessionData
    "sector_3_start_distance_m": 1,  # SessionData
    "session_distance_travelled_m": 2,  # LapDataPacket
    "session_duration_seconds": 1,  # SessionData
    "session_length": 1,  # SessionData
    "session_link_id": 1,  # SessionData
    "session_time": 0,  # Header (in all packets)
    "session_time_remaining_seconds": 1,  # SessionData
    "session_top_speedtrap": 2,  # LapDataPacket
    "session_top_speedtrap_driver": 2,  # LapDataPacket
    "session_type": 1,  # SessionData
    "session_uuid": 0,  # Header (in all packets)
    "sidepod_damage_percentage": 10,  # CarDamagePacket
    "sli_pro_native_support": 1,  # SessionData
    "spectator_car_index": 1,  # SessionData
    "speed": 6,  # CarTelemetryPacket
    "speed_trap_speed": 2,  # LapDataPacket
    "speed_units_player1": 1,  # SessionData
    "speed_units_player2": 1,  # SessionData
    "steer": 6,  # CarTelemetryPacket
    "steering_assist": 1,  # SessionData
    "surface_type": 1,  # SessionData
    "team_id": 4,  # ParticipantsPacket
    "teammate_in_pits_flag": 3,  # EventPacket (TeammateInPitData)
    "temp_units_player1": 1,  # SessionData
    "temp_units_player2": 1,  # SessionData
    "throttle": 6,  # CarTelemetryPacket
    "time_gained": 3,  # EventPacket (PenaltyData)
    "time_of_day": 1,  # SessionData
    "total_race_laps": 1,  # SessionData
    "total_warnings": 2,  # LapDataPacket
    "track_id": 1,  # SessionData
    "track_length_m": 1,  # SessionData
    "track_temp_c": 1,  # SessionData
    "traction_control": 7,  # CarStatusPacket
    "tyre_actual_compound": 12,  # TyreSetsPacket
    "tyre_age_laps": 7,  # CarStatusPacket
    "tyre_blisters_percentage": 10,  # CarDamagePacket
    "tyre_damage_percentage": 10,  # CarDamagePacket
    "tyre_replaced_lap": 11,  # SessionHistoryPacket
    "tyre_temps": 1,  # SessionData
    "tyre_visual_compound": 12,  # TyreSetsPacket
    "tyre_wear_percentage": 10,  # CarDamagePacket
    "tyres_inner_temperature": 6,  # CarTelemetryPacket
    "tyres_pressure": 6,  # CarTelemetryPacket
    "tyres_surface_temperature": 6,  # CarTelemetryPacket
    "usable_life": 12,  # TyreSetsPacket
    "vehicle_flags_shown": 7,  # CarStatusPacket
    "visual_tyre_compound": 12,  # TyreSetsPacket
    "wear": 12,  # TyreSetsPacket
    "weather": 1,  # SessionData
    "weekend_link_id": 1,  # SessionData
    "world_forward_direction_x": 0,  # Motion
    "world_forward_direction_y": 0,  # Motion
    "world_forward_direction_z": 0,  # Motion
    "world_position_x": 0,  # Motion
    "world_position_y": 0,  # Motion
    "world_position_z": 0,  # Motion
    "world_right_direction_x": 0,  # Motion
    "world_right_direction_y": 0,  # Motion
    "world_right_direction_z": 0,  # Motion
    "world_velocity_x": 0,  # Motion
    "world_velocity_y": 0,  # Motion
    "world_velocity_z": 0,  # Motion
    "yaw_radians": 0,  # Motion
}


def humanise(ms: int) -> str:
    seconds = float(ms / 1000)
    return f"{seconds:02.03f}s"


def display_data(key, value):
    match key:
        # Weather and Track Conditions
        case "weather":
            return "Weather", WEATHER_TYPE_DICT.get(value, "Unknown")
        case "track_temp_c":
            return "Track Temp", f"{value}°C"
        case "air_temp_c":
            return "Air Temp", f"{value}°C"
        case "track_id":
            return "Track", TRACK_DICT.get(value, "Unknown")

        # Session Information
        case "session_type":
            return "Session", SESSION_TYPE_DICT.get(value, "Unknown")
        case "session_length":
            return "Session Length", SESSION_LENGTH_DICT.get(value, "Unknown")
        case "ruleset":
            return "Ruleset", RULESET_TYPE_DICT.get(value, "Unknown")
        case "total_race_laps":
            return "Race Length", f"{value} laps"
        case "session_time_remaining_seconds":
            return "Time Remaining", f"{value} seconds"
        case "time_of_day":
            return "Time of Day", f"{value}"

        # Driver and Team Information
        case "driver_id":
            return "Driver", DRIVER_ID_DICT.get(value, "Unknown")
        case "team_id":
            return "Team", TEAM_ID_DICT.get(value, "Unknown")
        case "nationality":
            return "Nationality", NATIONALITY_DICT.get(value, "Unknown")
        case "race_number":
            return "Race Number", str(value)

        # Car Status
        case "car_position":
            return "Position", str(value)
        case "grid_position":
            return "Grid Position", str(value)
        case "driver_status":
            return "Driver Status", DRIVER_STATUS_DICT.get(value, "Unknown")
        case "result_status":
            return "Result Status", RESULT_STATUS_DICT.get(value, "Unknown")
        case "pit_status":
            return "Pit Status", PIT_STATUS_DICT.get(value, "Unknown")
        case "current_lap_invalid":
            return "Lap Validity", LAP_VALID_DICT.get(value, "Unknown")

        # Tyre Information
        case "actual_tyre_compound":
            return "Tyre Compound", TYRE_COMPOUND_DICT.get(value, "Unknown")
        case "visual_tyre_compound":
            return "Visual Tyre", TYRE_VISUAL_DICT.get(value, "Unknown")
        case "tyre_age_laps":
            return "Tyre Age", f"{value} laps"

        # Vehicle Settings
        case "fuel_mix":
            return "Fuel Mix", FUEL_MIX_DICT.get(value, "Unknown")
        case "traction_control":
            return "Traction Control", TRACTION_CONTROL_DICT.get(value, "Unknown")
        case "anti_lock_brakes":
            return "ABS", ANTI_LOCK_BRAKES_DICT.get(value, "Unknown")
        case "pit_limiter_status":
            return "Pit Limiter", PIT_LIMITER_DICT.get(value, "Unknown")

        # Assists and Driving Aids
        case "steering_assist":
            return "Steering Assist", ASSIT_DICT.get(value, "Unknown")
        case "braking_assist":
            return "Braking Assist", BRAKING_ASSIT_DICT.get(value, "Unknown")
        case "gearbox_assist":
            return "Gearbox Assist", GEARBOX_ASSIT_DICT.get(value, "Unknown")
        case "drs_assist":
            return "DRS Assist", ASSIT_DICT.get(value, "Unknown")
        case "ers_assist":
            return "ERS Assist", ASSIT_DICT.get(value, "Unknown")
        case "pit_assist":
            return "Pit Assist", ASSIT_DICT.get(value, "Unknown")
        case "pit_release_assist":
            return "Pit Release Assist", ASSIT_DICT.get(value, "Unknown")

        # Race Control and Penalties
        case "safety_car_status":
            return "Safety Car", SAFETY_CAR_STATUS_DICT.get(value, "Unknown")
        case "vehicle_flags_shown":
            return "Flag Shown", VEHICLE_FLAG_SHOWN_DICT.get(value, "Unknown")
        case "penalty_type":
            return "Penalty Type", PENALTY_TYPE_DICT.get(value, "Unknown")
        case "infringement_type":
            return "Infringement", INFRINGEMENT_TYPE_DICT.get(value, "Unknown")
        case "penalties":
            return "Penalty Points", str(value)
        case "total_warnings":
            return "Warnings", str(value)

        # DRS Information
        case "drs":
            return "DRS", "Open" if value == 1 else "Closed"
        case "drs_allowed":
            return "DRS Allowed", "Yes" if value == 1 else "No"
        case "drs_status":
            return "DRS Status", str(value)

        # Timing Information
        case "last_lap_time_ms":
            return "Last Lap", humanise(value)
        case "current_lap_time_ms":
            return "Current Lap", humanise(value)
        case "delta_to_car_in_front_ms_component":
            return "Delta (Front)", humanise(value)
        case "delta_to_car_behind_ms":
            return "Delta (Behind)", humanise(value)
        case "delta_to_leader_ms_component":
            return "Delta (Leader)", humanise(value)
        case "sector1_time_ms_component":
            return "Sector 1", humanise(value)
        case "sector2_time_ms_component":
            return "Sector 2", humanise(value)
        case "sector3_time_ms_component":
            return "Sector 3", humanise(value)

        # Speed Information
        case "speed":
            return "Speed", f"{value} km/h"
        case "fastest_speed_trap_speed_kph":
            return "Fastest Speed Trap", f"{value} km/h"

        # Engine and Telemetry
        case "engine_rpm":
            return "Engine RPM", str(value)
        case "gear":
            return "Gear", str(value) if value >= 0 else "R"
        case "throttle":
            return "Throttle", f"{value * 100:.1f}%"
        case "brake":
            return "Brake", f"{value * 100:.1f}%"
        case "clutch":
            return "Clutch", f"{value}%"
        case "steer":
            return "Steering", f"{value * 100:.1f}%"

        # System and Configuration
        case "network_game":
            return "Network Game", NETWORK_GAME_STATUS_DICT.get(value, "Unknown")
        case "equal_car_performance":
            return "Equal Performance", EQUAL_CAR_PERFORMANCE_DICT.get(value, "Unknown")
        case "recovery_mode":
            return "Recovery Mode", RECOVERY_MODE_DICT.get(value, "Unknown")
        case "flashback_limit":
            return "Flashback Limit", FLASHBACK_LIMIT_DICT.get(value, "Unknown")
        case "temp_units_player1":
            return "Temperature Units", TEMPERATURE_UNIT_DICT.get(value, "Unknown")
        case "speed_units_player1":
            return "Speed Units", SPEED_UNIT_DICT.get(value, "Unknown")

        # Default case for unhandled keys
        case _:
            return key.replace("_", " ").title(), str(value)
