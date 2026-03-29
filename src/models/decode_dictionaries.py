#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

### --------------- ###
### --- General --- ###
### --------------- ###
tyre_dict = {
    0: "Rear Left (RL)",
    1: "Rear Right (RR)",
    2: "Front Left (FL)",
    3: "Front Right (FR)",
    255: "N/A",
}

teams_dict = {
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
    142: "APXGP '24",
    154: "APXGP '25",
    155: "Konnersport '24",
    158: "Art GP '24",
    159: "Campos '24",
    160: "Rodin Motorsport '24",
    161: "AIX Racing '24",
    162: "DAMS '24",
    163: "Hitech '24",
    164: "MP Motorsport '24",
    165: "Prema '24",
    166: "Trident '24",
    167: "Van Amersfoort Racing '24",
    168: "Invicta '24",
    185: "Mercedes '24",
    186: "Ferrari '24",
    187: "Red Bull Racing '24",
    188: "Williams '24",
    189: "Aston Martin '24",
    190: "Alpine '24",
    191: "RB '24",
    192: "Haas '24",
    193: "McLaren '24",
    194: "Sauber '24",
    255: "N/A",
}

drivers_dict = {
    0: "Carlos Sainz ",
    2: "Daniel Ricciardo ",
    3: "Fernando Alonso ",
    4: "Felipe Massa ",
    7: "Lewis Hamilton ",
    9: "Max Verstappen ",
    10: "Nico Hülkenburg ",
    11: "Kevin Magnussen ",
    14: "Sergio Pérez ",
    15: "Valtteri Bottas ",
    17: "Esteban Ocon ",
    19: "Lance Stroll ",
    20: "Arron Barnes ",
    21: "Martin Giles ",
    22: "Alex Murray ",
    23: "Lucas Roth ",
    24: "Igor Correia ",
    25: "Sophie Levasseur ",
    26: "Jonas Schiffer ",
    27: "Alain Forest ",
    28: "Jay Letourneau ",
    29: "Esto Saari ",
    30: "Yasar Atiyeh ",
    31: "Callisto Calabresi ",
    32: "Naota Izumi ",
    33: "Howard Clarke ",
    34: "Lars Kaufmann ",
    35: "Marie Laursen ",
    36: "Flavio Nieves ",
    38: "Klimek Michalski ",
    39: "Santiago Moreno ",
    40: "Benjamin Coppens ",
    41: "Noah Visser ",
    50: "George Russell ",
    54: "Lando Norris ",
    58: "Charles Leclerc ",
    59: "Pierre Gasly ",
    62: "Alexander Albon ",
    70: "Rashid Nair ",
    71: "Jack Tremblay ",
    77: "Ayrton Senna ",
    80: "Guanyu Zhou ",
    83: "Juan Manuel Correa ",
    90: "Michael Schumacher ",
    94: "Yuki Tsunoda ",
    102: "Aidan Jackson ",
    109: "Jenson Button ",
    110: "David Coulthard ",
    112: "Oscar Piastri ",
    113: "Liam Lawson ",
    116: "Richard Verschoor",
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
    168: "Zak O'Sullivan",
    169: "Pepe Marti",
    170: "Sonny Hayes",
    171: "Joshua Pearce",
    172: "Callum Voisin",
    173: "Matias Zagazeta",
    174: "Nikola Tsolov",
    175: "Tim Tramnitz",
    185: "Luca Cortez",
    255: "N/A",
}

track_dict = {
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
    255: "N/A",
}

nationality_dict = {
    0: "N/A",
    1: "American ,",
    2: "Argentinean ,",
    3: "Australian ,",
    4: "Austrian ,",
    5: "Azerbaijani ,",
    6: "Bahraini ,",
    7: "Belgian ,",
    8: "Bolivian ,",
    9: "Brazilian ,",
    10: "British ,",
    11: "Bulgarian ,",
    12: "Cameroonian ,",
    13: "Canadian ,",
    14: "Chilean ,",
    15: "Chinese ,",
    16: "Colombian ,",
    17: "Costa Rican ,",
    18: "Croatian ,",
    19: "Cypriot ,",
    20: "Czech ,",
    21: "Danish ,",
    22: "Dutch ,",
    23: "Ecuadorian ,",
    24: "English ,",
    25: "Emirian ,",
    26: "Estonian ,",
    27: "Finnish ,",
    28: "French ,",
    29: "German ,",
    30: "Ghanaian ,",
    31: "Greek ,",
    32: "Guatemalan ,",
    33: "Honduran ,",
    34: "Hong Konger ,",
    35: "Hungarian ,",
    36: "Icelander ,",
    37: "Indian ,",
    38: "Indonesian ,",
    39: "Irish ,",
    40: "Israeli ,",
    41: "Italian ,",
    42: "Jamaican ,",
    43: "Japanese ,",
    44: "Jordanian ,",
    45: "Kuwaiti ,",
    46: "Latvian ,",
    47: "Lebanese ,",
    48: "Lithuanian ,",
    49: "Luxembourger ,",
    50: "Malaysian ,",
    51: "Maltese ,",
    52: "Mexican ,",
    53: "Monegasque ,",
    54: "New Zealander ,",
    55: "Nicaraguan ,",
    56: "Northern Irish ,",
    57: "Norwegian ,",
    58: "Omani ,",
    59: "Pakistani ,",
    60: "Panamanian,",
    61: "Paraguayan,",
    62: "Peruvian,",
    63: "Polish,",
    64: "Portuguese,",
    65: "Qatari,",
    66: "Romanian,",
    68: "Salvadoran,",
    69: "Saudi,",
    70: "Scottish,",
    71: "Serbian,",
    72: "Singaporean,",
    73: "Slovakian,",
    74: "Slovenian,",
    75: "South Korean,",
    76: "South African,",
    77: "Spanish,",
    78: "Swedish,",
    79: "Swiss,",
    80: "Thai,",
    81: "Turkish,",
    82: "Uruguayan,",
    83: "Ukrainian,",
    84: "Venezuelan",
    85: "Barbadian,",
    86: "Welsh,",
    87: "Vietnamese,",
    88: "Algerian,",
    89: "Bosnian,",
    90: "Filipino,",
    255: "N/A",
}

gamemode_dict = {
    4: "Grand Prix '23",
    5: "Time Trial",
    6: "Splitscreen",
    7: "Online Custom",
    15: "Online Weekly Event",
    17: "Story Mode (Braking Point)",
    27: "My Team Career '25",
    28: "Driver Career '25",
    29: "Career '25 Online",
    30: "Challenge Career '25",
    75: "Story Mode (APXGP)",
    127: "Benchmark",
    255: "N/A",
}

sessiontype_dict = {
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
    255: "N/A",
}

ruleset_dict = {
    0: "Practice & Qualifying",
    1: "Race",
    2: "Time Trial",
    12: "Elimination",
    255: "N/A",
}

suracetype_dict = {
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
    255: "N/A",
}

penaltytype_dict = {
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
    255: "N/A",
}

infringementtype_dict = {
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
    255: "N/A",
}

### --------------- ###
### --- Session --- ###
### --------------- ###
marshal_zone_flag_dict = {
    -1: "invalid/unknown",
    0: "none",
    1: "green",
    2: "blue",
    3: "yellow",
    255: "N/A",
}
weather_forecast_dict = {
    0: "clear",
    1: "light cloud",
    2: "overcast",
    3: "light rain",
    4: "heavy rain",
    5: "storm",
    255: "N/A",
}
weather_forecast_change_dict = {0: "up", 1: "down", 2: "no change", 255: "N/A"}

formula_dict = {
    0: "F1 Modern",
    1: "F1 Classic",
    2: "F2",
    3: "F1 Generic",
    4: "Beta",
    6: "Esports",
    8: "F1 World",
    9: "F1 Elimination",
    255: "N/A",
}
sli_dict = {0: "inactive", 1: "active", 255: "N/A"}
safetycarstatus_dict = {
    0: "no safety car",
    1: "full",
    2: "virtual",
    3: "formation lap",
    255: "N/A",
}
networkgame_dict = {0: "offline", 1: "online", 255: "N/A"}
forecastaccuracy_dict = {0: "Perfect", 1: "Approximate", 255: "N/A"}
steeringassist_dict = {0: "off", 1: "on", 255: "N/A"}
brakingassist_dict = {0: "off", 1: "low", 2: "medium", 3: "high", 255: "N/A"}
gearboxassist_dict = {
    0: "N/A",
    1: "manual",
    2: "manual & suggested gear",
    3: "auto",
    255: "N/A",
}
pitassist_dict = {0: "off", 1: "on", 255: "N/A"}
pitreleaseassist_dict = {0: "off", 1: "on", 255: "N/A"}
ersassist_dict = {0: "off", 1: "on", 255: "N/A"}
drsassist_dict = {0: "off", 1: "on", 255: "N/A"}
dynamicracingline_dict = {0: "off", 1: "corners only", 2: "full", 255: "N/A"}
dynamicracinglinetype_dict = {0: "2D", 1: "3D", 255: "N/A"}
sessionlength_dict = {
    0: "None",
    2: "Very Short",
    3: "Short",
    4: "Medium",
    5: "Medium Long",
    6: "Long",
    7: "Full",
    255: "N/A",
}
speedunitsplayer_dict = {0: "MPH", 1: "KPH", 255: "N/A"}
temperatureunitsplayer_dict = {0: "Celsius", 1: "Fahrenheit", 255: "N/A"}
equalcarperformance_dict = {0: "Off", 1: "On", 255: "N/A"}
recoverymode_dict = {0: "None", 1: "Flashbacks", 2: "Auto-recovery", 255: "N/A"}
flashbacklimit_dict = {0: "Low", 1: "Medium", 2: "High", 3: "Unlimited", 255: "N/A"}
surfacetype_dict = {0: "Simplified", 1: "Realistic", 255: "N/A"}
lowfuelmode_dict = {0: "Easy", 1: "Hard", 255: "N/A"}
racestarts_dict = {0: "Manual", 1: "Assisted", 255: "N/A"}
tyretemperature_dict = {0: "Surface only", 1: "Surface & Carcass", 255: "N/A"}
pitlanetyresim_dict = {0: "On", 1: "Off", 255: "N/A"}
cardamage_dict = {0: "Off", 1: "Reduced", 2: "Standard", 3: "Simulation", 255: "N/A"}
cardamagerate_dict = {0: "Reduced", 1: "Standard", 2: "Simulation", 255: "N/A"}
collisions_dict = {0: "Off", 1: "Player-to-Player Off", 2: "On", 255: "N/A"}
collisionsoffforfirstlaponly_dict = {0: "Disabled", 1: "Enabled", 255: "N/A"}
mpunsafepitrelease_dict = {0: "On", 1: "Off (Multiplayer)", 255: "N/A"}
mpoffforgriefing_dict = {0: "Disabled", 1: "Enabled (Multiplayer)", 255: "N/A"}
cornercuttingstringency_dict = {0: "Regular", 1: "Strict", 255: "N/A"}
parcfermerules_dict = {0: "Off", 1: "On", 255: "N/A"}
pitstopexperience_dict = {0: "Automatic", 1: "Broadcast", 2: "Immersive", 255: "N/A"}
safetycar_dict = {0: "Off", 1: "Reduced", 2: "Standard", 3: "Increased", 255: "N/A"}
safetycarexperience_dict = {0: "Broadcast", 1: "Immersive", 255: "N/A"}
formationlap_dict = {0: "Off", 1: "On", 255: "N/A"}
formationlapexperience_dict = {0: "Broadcast", 1: "Immersive", 255: "N/A"}
redflags_dict = {0: "Off", 1: "Reduced", 2: "Standard", 3: "Increased", 255: "N/A"}
affectslicencelevelsolo_dict = {0: "Off", 1: "On", 255: "N/A"}
affectslicencelevelmp_dict = {0: "Off", 1: "On", 255: "N/A"}

### ---------------- ###
### --- Lap Data --- ###
### ---------------- ###
pitstatus_dict = {0: "none", 1: "pitting", 2: "in pit area", 255: "N/A"}
sector_dict = {0: "sector1", 1: "sector2", 2: "sector3", 255: "N/A"}
currentlapinvalid_dict = {0: "valid", 1: "invalid", 255: "N/A"}
driverstatus_dict = {
    0: "in garage",
    1: "flying lap",
    2: "in lap",
    3: "out lap",
    4: "on track",
    255: "N/A",
}
result_dict = {
    0: "invalid",
    1: "inactive",
    2: "active",
    3: "finished",
    4: "didnotfinish",
    5: "disqualified",
    6: "not classified",
    7: "retired",
    255: "N/A",
}
pit_dict = {0: "inactive", 1: "active", 255: "N/A"}

### ------------- ###
### --- Event --- ###
### ------------- ###
retirementreason_dict = {
    0: "invalid",
    1: "retired",
    2: "finished",
    3: "terminal damage",
    4: "inactive",
    5: "not enough laps completed",
    6: "black flagged",
    7: "red flagged",
    8: "mechanical failure",
    9: "session skipped",
    10: "session simulated",
    255: "N/A",
}
drsdeactivatedreason_dict = {
    0: "Wet track",
    1: "Safety car deployed",
    2: "Red flag",
    3: "Min lap not reached",
    255: "N/A",
}
safetycartype_dict = {
    0: "No Safety Car",
    1: "Full Safety Car",
    2: "Virtual Safety Car",
    3: "Formation Lap Safety Car",
    255: "N/A",
}
safetycarstatus_dict = {
    0: "Deployed",
    1: "Returning",
    2: "Returned",
    3: "Resume Race",
    255: "N/A",
}

### -------------------- ###
### --- Participants --- ###
### -------------------- ###
telemetry_dict = {0: "restricted", 1: "public", 255: "N/A"}
platform_dict = {
    0: "N/A",
    1: "Steam",
    3: "PlayStation",
    4: "Xbox",
    6: "Origin",
    255: "N/A",
}

### ----------------- ###
### --- Telemetry --- ###
### ----------------- ###
drsstatus_dict = {0: "off", 1: "on", 255: "N/A"}


### -------------- ###
### --- Status --- ###
### -------------- ###
tractioncontrol_dict = {0: "off", 1: "medium", 2: "full", 255: "N/A"}
antilockbrakes_dict = {0: "off", 1: "on", 255: "N/A"}
fuelmix_dict = {0: "lean", 1: "standard", 2: "rich", 3: "max", 255: "N/A"}
pitlimiterstatus_dict = {0: "off", 1: "on", 255: "N/A"}
drsallowed_dict = {0: "not allowed", 1: "allowed", 255: "N/A"}
actualtyrecompound_dict = {
    16: "C5",
    17: "C4",
    18: "C3",
    19: "C2",
    20: "C1",
    21: "C0",
    22: "C6",
    7: "inter",
    8: "wet",
    9: "dry",
    10: "wet",
    11: "super soft",
    12: "soft",
    13: "medium",
    14: "hard",
    15: "wet",
    255: "N/A",
    0: "N/A",
}
visualtyrecompound_dict = {
    16: "soft",
    17: "medium",
    18: "hard",
    7: "inter",
    8: "wet",
    15: "wet",
    19: "super soft",
    20: "soft",
    21: "medium",
    22: "hard",
    255: "N/A",
    0: "N/A",
}
vehiclefiaflags_dict = {
    -1: "invalid/unknown",
    0: "none",
    1: "green",
    2: "blue",
    3: "yellow",
    255: "N/A",
}
ersdeploymode_dict = {0: "none", 1: "medium", 2: "hotlap", 3: "overtake", 255: "N/A"}

### ---------------------- ###
### --- Classification --- ###
### ---------------------- ###
resultstatus_dict = {
    0: "invalid",
    1: "inactive",
    2: "active",
    3: "finished",
    4: "didnotfinish",
    5: "disqualified",
    6: "not classified",
    7: "retired",
    255: "N/A",
}
resultreason_dict = {
    0: "invalid",
    1: "retired",
    2: "finished",
    3: "terminal damage",
    4: "inactive",
    5: "not enough laps completed",
    6: "black flagged",
    7: "red flagged",
    8: "mechanical failure",
    9: "session skipped",
    10: "session simulated",
    255: "N/A",
}

### ------------- ###
### --- Lobby --- ###
### ------------- ###
platform_dict = {
    0: "N/A",
    1: "Steam",
    3: "PlayStation",
    4: "Xbox",
    6: "Origin",
    255: "N/A",
}
yourtelemetry_dict = {0: "restricted", 1: "public", 255: "N/A"}
showonlinenames_dict = {0: "off", 1: "on", 255: "N/A"}
readystatus_dict = {0: "not ready", 1: "ready", 2: "spectating", 255: "N/A"}

### -------------- ###
### --- Damage --- ###
### -------------- ###
drsfault_dict = {0: "OK", 1: "fault", 255: "N/A"}
ersfault_dict = {0: "OK", 1: "fault", 255: "N/A"}
engineblown_dict = {0: "OK", 1: "fault", 255: "N/A"}
engineseized_dict = {0: "OK", 1: "fault", 255: "N/A"}
