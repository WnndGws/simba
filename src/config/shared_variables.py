#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

# Header
header = None

# Header 0
prev_motion = None
motion = None

# Header 1
prev_session = None
session = None

# Header 2
prev_lapdata = None
lapdata = None

# Header 3
event = None
event_fastest_lap = None

# Header 4
participants_cache = 0
participants = None

# Header 5
prev_setup = None
setup = None

# Header 6
prev_telemetry = None
telemetry = None

# Header 7
prev_status = None
status = None

# Header 8
prev_classification = None
classification = None

# Header 9
lobby_cache = 0
lobby = None

# Header 10
prev_damage = None
damage = None

# Header 11
player_histories = 0
history = [None] * 22

# Header 12
tyres = [None] * 22

# Header 13
prev_exmotion = None
exmotion = None

# Header 14
prev_timetrial = None
timetrial = None

# Header 15
position_history = None
