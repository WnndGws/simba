#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

zone_flag_dict = {
    -1: "Unknown",
    0: "None",
    1: "Green",
    2: "Blue",
    3: "Yellow",
}

weather_dict = {
    0: "Clear",
    1: "Light Cloud",
    2: "Overcast",
    3: "Light Rain",
    4: "Heavy Rain",
    5: "Storm",
}

formula_classification_dict = {
    0: "F1 Modern",
    1: "F1 Classic",
    2: "F2",
    3: "F1 Generic",
    4: "Beta",
    6: "Esports",
    8: "F1 World",
    9: "F1 Elimination",
}

safety_car_status_dict = {
    0: "No Safety Car",
    1: "Full",
    2: "Virtual",
    3: "Formation Lap",
}

forecast_accuracy_dict = {0: "Perfect", 1: "Approximate"}

steering_assist_dict = {
    0: "Off",
    1: "On",
}
braking_assist_dict = {
    0: "Off",
    1: "Low",
    2: "Medium",
    3: "High",
}
gearbox_assist_dict = {
    1: "Manual",
    2: "Manual Suggested Gear",
    3: "Auto",
}
pit_assist_dict = {
    0: "Off",
    1: "On",
}
pit_release_assist_dict = {
    0: "Off",
    1: "On",
}
ers_assist_dict = {
    0: "Off",
    1: "On",
}
d_r_s_assist_dict = {
    0: "Off",
    1: "On",
}
dynamic_racing_line_dict = {
    0: "Off",
    1: "Corners Only",
    2: "Full",
}
dynamic_racing_line_type_dict = {
    0: "2D",
    1: "3D",
}
session_length_dict = {
    0: "None",
    2: "Very Short",
    3: "Short",
    4: "Medium",
    5: "Medium Long",
    6: "Long",
    7: "Full",
}
equal_car_performance_dict = {
    0: "Off",
    1: "On",
}
recovery_mode_dict = {
    0: "None",
    1: "Flashbacks",
    2: "Auto-recovery",
}
flashback_limit_dict = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Unlimited",
}
surface_type_dict = {
    0: "Simplified",
    1: "Realistic",
}
low_fuel_mode_dict = {
    0: "Easy",
    1: "Hard",
}
race_starts_dict = {
    0: "Manual",
    1: "Assisted",
}
tyre_temperature_dict = {
    0: "Surface only",
    1: "Surface & Carcass",
}
pit_lane_tyre_sim_dict = {
    0: "On",
    1: "Off",
}
car_damage_dict = {
    0: "Off",
    1: "Reduced",
    2: "Standard",
    3: "Simulation",
}
car_damage_rate_dict = {
    0: "Reduced",
    1: "Standard",
    2: "Simulation",
}
collisions_dict = {
    0: "Off",
    1: "Player-to-Player Off",
    2: "On",
}
collisions_off_for_first_lap_only_dict = {
    0: "Disabled",
    1: "Enabled",
}
mp_unsafe_pit_release_dict = {
    0: "On",
    1: "Off (Multiplayer)",
}
mp_off_for_griefing_dict = {
    0: "Disabled",
    1: "Enabled (Multiplayer)",
}
corner_cutting_stringency_dict = {
    0: "Regular",
    1: "Strict",
}
parc_ferme_rules_dict = {
    0: "Off",
    1: "On",
}

pit_stop_experience_dict = {
    0: "Automatic",
    1: "Broadcast",
    2: "Immersive",
}
safety_car_dict = {
    0: "Off",
    1: "Reduced",
    2: "Standard",
    3: "Increased",
}
safety_car_experience_dict = {
    0: "Broadcast",
    1: "Immersive",
}
formation_lap_dict = {
    0: "Off",
    1: "On",
}
formation_lap_experience_dict = {
    0: "Broadcast",
    1: "Immersive",
}
red_flags_dict = {
    0: "Off",
    1: "Reduced",
    2: "Standard",
    3: "Increased",
}
affects_licence_level_solo_dict = {
    0: "Off",
    1: "On",
}
affects_licence_level_m_p_dict = {
    0: "Off",
    1: "On",
}

pit_status_dict = {
    0: "None",
    1: "Pitting",
    2: "In Pit Area",
}
sector_dict = {
    0: "Sector1",
    1: "Sector2",
    2: "Sector3",
}
current_lap_invalid_dict = {
    0: "Valid",
    1: "Invalid",
}

driver_status_dict = {
    0: "In Garage",
    1: "Flying Lap",
    2: "In Lap",
    3: "Out Lap",
    4: "On Track",
}
result_status_dict = {
    0: "Invalid",
    1: "Inactive",
    2: "Active",
    3: "Finished",
    4: "Didnotfinish",
    5: "Disqualified",
    6: "Not Classified",
    7: "Retired",
}
pit_lane_timer_active_dict = {
    0: "Inactive",
    1: "Active",
}

retirement_reason_dict = {
    0: "Invalid",
    1: "Retired",
    2: "Finished",
    3: "Terminal Damage",
    4: "Inactive",
    5: "Not Enough Laps Completed",
    6: "Black Flagged",
    7: "Red Flagged",
    8: "Mechanical Failure",
    9: "Session Skipped",
    10: "Session Simulated",
}

drs_reason_dict = {
    0: "Wet track",
    1: "Safety car deployed",
    2: "Red flag",
    3: "Min lap not reached",
}

safety_car_type_dict = {
    0: "No Safety Car",
    1: "Full Safety Car",
    2: "Virtual Safety Car",
    3: "Formation Lap Safety Car",
}
ent_type_dict = {
    0: "Deployed",
    1: "Returning",
    2: "Returned",
    3: "Resume Race",
}

my_team_dict = {1: "My Team", 0: "Otherwise"}

platform_dict = {
    1: "Steam",
    3: "PlayStation",
    4: "Xbox",
    6: "Origin",
    255: "Unknown",
}

traction_control_dict = {
    0: "Off",
    1: "Medium",
    2: "Full",
}
anti_lock_brakes_dict = {
    0: "Off ",
    1: "On",
}
fuel_mix_dict = {
    0: "Lean",
    1: "Standard",
    2: "Rich",
    3: "Max",
}

pit_limiter_status_dict = {
    0: "Off",
    1: "On",
}

drs_allowed_dict = {
    0: "NO DRS",
    1: "DRS active",
}

actual_tyre_compound_dict = {
    16: "C5",
    17: "C4",
    18: "C3",
    19: "C2",
    20: "C1",
    21: "C0",
    22: "C6",
    7: "Inter",
    8: "Wet",
    9: "Dry",
    10: "Wet",
    11: "Super Soft",
    12: "Soft",
    13: "Medium",
    14: "Hard",
    15: "Wet",
}
visual_tyre_compound_dict = {
    16: "Soft",
    17: "Medium",
    18: "Hard",
    7: "Inter",
    8: "Wet",
    15: "Wet",
    19: "Super Soft",
    20: "Soft",
    21: "Medium",
    22: "Hard",
}

ers_deploy_mode_dict = {
    0: "None",
    1: "Medium",
    2: "Hotlap",
    3: "Overtake",
}

result_status_dict = {
    0: "Invalid",
    1: "Inactive",
    2: "Active",
    3: "Finished",
    4: "DNF",
    5: "Disqualified",
    6: "Not Classified",
    7: "Retired",
}
result_reason_dict = {
    0: "Invalid",
    1: "Retired",
    2: "Finished",
    3: "Terminal Damage",
    4: "Inactive",
    5: "Not Enough Laps Completed",
    6: "Black Flagged",
    7: "Red Flagged",
    8: "Mechanical Failure",
    9: "Session Skipped",
    10: "Session Simulated",
}

ers_status_dict = {
    0: "OK",
    1: "Fault",
}

engine_blown_dict = {
    0: "OK",
    1: "Fault",
}
engine_seized_dict = {
    0: "OK",
    1: "Fault",
}

team_dict = {
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

driver_dict = {
    0: "Carlos Sainz",
    10: "Nico Hülkenburg",
    102: "Aidan Jackson",
    109: "Jenson Button",
    11: "Kevin Magnussen",
    110: "David Coulthard",
    112: "Oscar Piastri",
    113: "Liam Lawson",
    116: "Richard Verschoor",
    123: "Enzo Fittipaldi",
    125: "Mark Webber",
    126: "Jacques Villeneuve",
    127: "Callie Mayer",
    132: "Logan Sargeant",
    136: "Jack Doohan",
    137: "Amaury Cordeel",
    138: "Dennis Hauger",
    14: "Sergio Pérez",
    145: "Zane Maloney",
    146: "Victor Martins",
    147: "Oliver Bearman",
    148: "Jak Crawford",
    149: "Isack Hadjar",
    15: "Valtteri Bottas",
    152: "Roman Stanek",
    153: "Kush Maini",
    156: "Brendon Leigh",
    157: "David Tonizza",
    158: "Jarno Opmeer",
    159: "Lucas Blakeley",
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
    17: "Esteban Ocon",
    170: "Sonny Hayes",
    171: "Joshua Pearce",
    172: "Callum Voisin",
    173: "Matias Zagazeta",
    174: "Nikola Tsolov",
    175: "Tim Tramnitz",
    185: "Luca Cortez",
    19: "Lance Stroll",
    2: "Daniel Ricciardo",
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
    3: "Fernando Alonso",
    30: "Yasar Atiyeh",
    31: "Callisto Calabresi",
    32: "Naota Izumi",
    33: "Howard Clarke",
    34: "Lars Kaufmann",
    35: "Marie Laursen",
    36: "Flavio Nieves",
    38: "Klimek Michalski",
    39: "Santiago Moreno",
    4: "Felipe Massa",
    40: "Benjamin Coppens",
    41: "Noah Visser",
    50: "George Russell",
    54: "Lando Norris",
    58: "Charles Leclerc",
    59: "Pierre Gasly",
    62: "Alexander Albon",
    7: "Lewis Hamilton",
    70: "Rashid Nair",
    71: "Jack Tremblay",
    77: "Ayrton Senna",
    80: "Guanyu Zhou",
    83: "Juan Manuel Correa",
    9: "Max Verstappen",
    90: "Michael Schumacher",
    94: "Yuki Tsunoda",
}

tract_dict = {
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

nationality_dict = {
    1: "American",
    10: "British",
    11: "Bulgarian",
    12: "Cameroonian",
    13: "Canadian",
    14: "Chilean",
    15: "Chinese",
    16: "Colombian",
    17: "Costa Rican",
    18: "Croatian",
    19: "Cypriot",
    2: "Argentinean",
    20: "Czech",
    21: "Danish",
    22: "Dutch",
    23: "Ecuadorian",
    24: "English",
    25: "Emirian",
    26: "Estonian",
    27: "Finnish",
    28: "French",
    29: "German",
    3: "Australian",
    30: "Ghanaian",
    31: "Greek",
    32: "Guatemalan",
    33: "Honduran",
    34: "Hong Konger",
    35: "Hungarian",
    36: "Icelander",
    37: "Indian",
    38: "Indonesian",
    39: "Irish",
    4: "Austrian",
    40: "Israeli",
    41: "Italian",
    42: "Jamaican",
    43: "Japanese",
    44: "Jordanian",
    45: "Kuwaiti",
    46: "Latvian",
    47: "Lebanese",
    48: "Lithuanian",
    49: "Luxembourger",
    5: "Azerbaijani",
    50: "Malaysian",
    51: "Maltese",
    52: "Mexican",
    53: "Monegasque",
    54: "New Zealander",
    55: "Nicaraguan",
    56: "Northern Irish",
    57: "Norwegian",
    58: "Omani",
    59: "Pakistani",
    6: "Bahraini",
    60: "Panamanian",
    61: "Paraguayan",
    62: "Peruvian",
    63: "Polish",
    64: "Portuguese",
    65: "Qatari",
    66: "Romanian",
    68: "Salvadoran",
    69: "Saudi",
    7: "Belgian",
    70: "Scottish",
    71: "Serbian",
    72: "Singaporean",
    73: "Slovakian",
    74: "Slovenian",
    75: "South Korean",
    76: "South African",
    77: "Spanish",
    78: "Swedish",
    79: "Swiss",
    8: "Bolivian",
    80: "Thai",
    81: "Turkish",
    82: "Uruguayan",
    83: "Ukrainian",
    84: "Venezuelan",
    85: "Barbadian",
    86: "Welsh",
    87: "Vietnamese",
    88: "Algerian",
    89: "Bosnian",
    9: "Brazilian",
    90: "Filipino",
}

mode_dict = {
    4: "Grand Prix 23",
    5: "Time Trial",
    6: "Splitscreen",
    7: "Online Custom",
    15: "Online Weekly Event",
    17: "Story Mode (Braking Point)",
    27: "My Team Career 25",
    28: "Driver Career 25",
    29: "Career ’25 Online",
    30: "Challenge Career 25",
    75: "Story Mode (APXGP)",
    127: "Benchmark",
}

session_type_dict = {
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

ruleset_dict = {
    0: "Practice & Qualifying",
    1: "Race",
    2: "Time Trial",
    12: "Elimination",
}

surface_dict = {
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

penalty_dict = {
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
    17: "Black flag timer",
}

infringement_dict = {
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

# manually measured
drs_detection_zones_dict = {0: [1959, 4555], 2: [3222, 5110], 13: [5080]}
