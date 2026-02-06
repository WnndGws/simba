#!/usr/bin/env python
"""All info from https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-udp-specification/12187347"""

from typing import Final

PACKET_HEADER_LENGTH: Final[int] = 29  # <HBBBBBQfLLBB

GRID_SIZE: Final[int] = 22  # cars in the race

TIRE_COUNT: Final[int] = 4  # ruff insists

MAX_MARSHAL_ZONES: Final[int] = 21  # per track

MAX_WEATHER_SAMPLES: Final[int] = 56  # per session

MAX_TYRE_STINTS: Final[int] = 8  # per session

MAX_LAP_HISTORIES: Final[int] = 100  # per session

NULL_BYTE_VALUE: Final[int] = 255  # as per documentation

NAME_SIZE: Final[int] = 48  # max driver name len

PACKET_ID_DICT: Final[dict[int:str]] = {
    0: "MOTION",
    1: "SESSION",
    2: "LAP_DATA",
    3: "EVENT",
    4: "PARTICIPANTS",
    5: "CAR_SETUPS",
    6: "CAR_TELEMETRY",
    7: "CAR_STATUS",
    8: "FINAL_CLASSIFICATION",
    9: "LOBBY_INFO",
    10: "CAR_DAMAGE",
    11: "SESSION_HISTORY",
}

EVENT_DICT: Final[dict[str:str]] = {
    "SSTA": "SESSION_START",
    "SEND": "SESSION_END",
    "FTLP": "FASTEST_LAP",
    "RTMT": "RETIREMENT",
    "DRSE": "DRS_ENABLED",
    "DRSD": "DRS_DISABLED",
    "TMPT": "TEAM_MATE_IN_PITS",
    "CHQF": "CHEQUERED_FLAG",
    "RCWN": "RACE_WINNER",
    "PENA": "PENALTY",
    "SPTP": "SPEED_TRAP",
    "STLG": "START_LIGHTS",
    "LGOT": "LIGHTS_OUT",
    "DTSV": "DRIVE_THROUGH_SERVED",
    "SGSV": "STOP_GO_SERVED",
    "FLBK": "FLASHBACK",
    "BUTN": "BUTTON",
}

FORMALA_CLASSIFICATION_DICT: Final[dict[int:str]] = {
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
    168: "Zak O’Sullivan",
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
