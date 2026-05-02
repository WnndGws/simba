#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import struct
import sys
from dataclasses import asdict, dataclass, field
from itertools import batched, islice
from typing import ClassVar, Self

from rich import print

from models import decode_dictionaries


## ------------------------------- ##
## ------ Helper Functions ------- ##
## ------------------------------- ##
def decode_decoded_enums(
    name_of_class: str,
    decode_mapping_dict: dict,
) -> list:
    try:
        return {
            k: (decode_mapping_dict[k][v] if k in decode_mapping_dict else v)
            for k, v in asdict(name_of_class).items()
        }
    except KeyError:
        for k, v in asdict(name_of_class).items():
            if k in decode_mapping_dict:
                try:
                    _new = decode_mapping_dict[k][v]
                except KeyError:
                    print(k)
                    print(v)
                    print(decode_mapping_dict[k])


session_decode_mapping = {
    "weather": decode_dictionaries.weather_forecast_dict,
    "session_type": decode_dictionaries.sessiontype_dict,
    "track_id": decode_dictionaries.track_dict,
    "formula": decode_dictionaries.formula_dict,
    "sli_pro_native_support": decode_dictionaries.sli_dict,
    "safety_car_status": decode_dictionaries.safetycar_dict,
    "network_game": decode_dictionaries.networkgame_dict,
    "weather_forecast_accuracy": decode_dictionaries.forecastaccuracy_dict,
    "steering_assist": decode_dictionaries.steeringassist_dict,
    "braking_assist": decode_dictionaries.brakingassist_dict,
    "gearbox_assist": decode_dictionaries.gearboxassist_dict,
    "pit_assist": decode_dictionaries.pitassist_dict,
    "pit_release_assist": decode_dictionaries.pitreleaseassist_dict,
    "ers_assist": decode_dictionaries.ersassist_dict,
    "drs_assist": decode_dictionaries.drsassist_dict,
    "dynamic_racing_line": decode_dictionaries.dynamicracingline_dict,
    "dynamic_racing_line_type": decode_dictionaries.dynamicracinglinetype_dict,
    "session_length": decode_dictionaries.sessionlength_dict,
    "speed_units_player1": decode_dictionaries.speedunitsplayer_dict,
    "temp_units_player1": decode_dictionaries.temperatureunitsplayer_dict,
    "speed_units_player2": decode_dictionaries.speedunitsplayer_dict,
    "temp_units_player2": decode_dictionaries.temperatureunitsplayer_dict,
    "equal_car_performance": decode_dictionaries.equalcarperformance_dict,
    "recovery_mode": decode_dictionaries.recoverymode_dict,
    "flashback_limit": decode_dictionaries.flashbacklimit_dict,
    "surface_type": decode_dictionaries.surfacetype_dict,
    "low_fuel_mode": decode_dictionaries.lowfuelmode_dict,
    "race_starts": decode_dictionaries.racestarts_dict,
    "tyre_temps": decode_dictionaries.tyretemperature_dict,
    "pit_lane_tyre_sim": decode_dictionaries.pitlanetyresim_dict,
    "car_damage": decode_dictionaries.cardamage_dict,
    "car_damage_rate": decode_dictionaries.cardamagerate_dict,
    "collisions": decode_dictionaries.collisions_dict,
    "collisions_first_lap_only": decode_dictionaries.collisionsoffforfirstlaponly_dict,
    "multiplayer_unsafe_pit_release": decode_dictionaries.mpunsafepitrelease_dict,
    "multiplayer_kick_for_griefing": decode_dictionaries.mpoffforgriefing_dict,
    "corner_cutting_stringency": decode_dictionaries.cornercuttingstringency_dict,
    "parc_ferme": decode_dictionaries.parcfermerules_dict,
    "pit_stop_experience": decode_dictionaries.pitstopexperience_dict,
    "safety_car": decode_dictionaries.safetycar_dict,
    "safety_car_experience": decode_dictionaries.safetycarexperience_dict,
    "formation_lap": decode_dictionaries.formationlap_dict,
    "formation_lap_experience": decode_dictionaries.formationlapexperience_dict,
    "red_flags": decode_dictionaries.redflags_dict,
    "affects_licence_level_solo": decode_dictionaries.affectslicencelevelsolo_dict,
    "affects_licence_level_multiplayer": decode_dictionaries.affectslicencelevelmp_dict,
}
marshalzone_decode_mapping = {
    "zone_flag_type": decode_dictionaries.marshal_zone_flag_dict
}
weather_decode_mapping = {
    "session_type": decode_dictionaries.sessiontype_dict,
    "weather": decode_dictionaries.weather_forecast_dict,
    "track_temp_change_c": decode_dictionaries.weather_forecast_change_dict,
    "air_temp_change_c": decode_dictionaries.weather_forecast_change_dict,
}
lapdata_decode_mapping = {
    "pit_status": decode_dictionaries.pitstatus_dict,
    "sector": decode_dictionaries.sector_dict,
    "current_lap_invalid": decode_dictionaries.currentlapinvalid_dict,
    "driver_status": decode_dictionaries.driverstatus_dict,
    "result_status": decode_dictionaries.result_dict,
}
penalties_decode_mapping = {
    "pentalty_type": decode_dictionaries.penaltytype_dict,
    "infringement_type": decode_dictionaries.infringementtype_dict,
}
safetycar_decode_mapping = {
    "safety_car_type": decode_dictionaries.safetycartype_dict,
    "safety_car_status": decode_dictionaries.safetycarstatus_dict,
}
participants_decode_mapping = {
    "network_telemetry_flag": decode_dictionaries.telemetry_dict,
    "platform": decode_dictionaries.platform_dict,
}
telemetry_decode_mapping = {"drs": decode_dictionaries.drsstatus_dict}
status_decode_mapping = {
    "traction_control": decode_dictionaries.tractioncontrol_dict,
    "anti_lock_brakes": decode_dictionaries.antilockbrakes_dict,
    "fuel_mix": decode_dictionaries.fuelmix_dict,
    "pit_limiter_status": decode_dictionaries.pitlimiterstatus_dict,
    "drs_allowed": decode_dictionaries.drsallowed_dict,
    "actual_tyre_compound": decode_dictionaries.actualtyrecompound_dict,
    "visual_tyre_compound": decode_dictionaries.visualtyrecompound_dict,
    "vehicle_flags_shown": decode_dictionaries.vehiclefiaflags_dict,
    "ers_deploy_mode": decode_dictionaries.ersdeploymode_dict,
}
classification_decode_mapping = {
    "result_status": decode_dictionaries.resultstatus_dict,
    "result_reason": decode_dictionaries.resultreason_dict,
}
lobby_decode_mapping = {
    "team_id": decode_dictionaries.teams_dict,
    "nationality": decode_dictionaries.nationality_dict,
    "platform": decode_dictionaries.platform_dict,
    "your_telemetry": decode_dictionaries.yourtelemetry_dict,
    "show_online_names": decode_dictionaries.showonlinenames_dict,
    "ready_status": decode_dictionaries.readystatus_dict,
}
damage_decode_mapping = {
    "drs_fault": decode_dictionaries.drsfault_dict,
    "ers_fault": decode_dictionaries.ersfault_dict,
    "engine_blown": decode_dictionaries.engineblown_dict,
    "engine_seized": decode_dictionaries.engineseized_dict,
}

## --------------------- ##
## ------ HEADER ------- ##
## --------------------- ##
# 29 bytes
HEADER_STRUCT = struct.Struct("<HBBBBBQfIIBB")


@dataclass(slots=True)
class Header:
    packet_format: int
    game_year: int
    game_major_version: int
    game_minor_version: int
    packet_version: int
    packet_id: int
    session_uuid: int | str
    session_time: float
    frame_id: int
    overall_frame: int
    player_car_index: int
    player2_car_index: int

    @classmethod
    def decode(cls, packet: bytes, offset: int = 0) -> Self:
        mem = memoryview(packet)
        values = HEADER_STRUCT.unpack(mem[:29])
        return {
            k: (str(v) if k == "session_uuid" else v)
            for k, v in asdict(cls(*values)).items()
        }


## --------------------- ##
## ------ MOTION ------- ##
## --------------------- ##
# Header 0
# 1349 bytes
MOTION_STRUCT = struct.Struct("<" + ("ffffffhhhhhhffffff" * 22))


@dataclass
class Motion:
    world_position_x: float
    world_position_y: float
    world_position_z: float
    world_velocity_x: float
    world_velocity_y: float
    world_velocity_z: float
    world_forward_direction_x: int
    world_forward_direction_y: int
    world_forward_direction_z: int
    world_right_direction_x: int
    world_right_direction_y: int
    world_right_direction_z: int
    g_force_lateral: float
    g_force_longitudinal: float
    g_force_vertical: float
    yaw_radians: float
    pitch_radians: float
    roll_radians: float


@dataclass
class MotionPacket:
    cars: list[Motion]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29) -> dict:
        mem = memoryview(packet)
        values = MOTION_STRUCT.unpack_from(mem, offset)
        length_of_data = 18
        number_of_repeats = 22
        decoded = [
            asdict(Motion(*chunk))
            for chunk in islice(
                batched(values, length_of_data, strict=True), number_of_repeats
            )
        ]
        return asdict(cls(decoded))


## ---------------------- ##
## ------ SESSION ------- ##
## ---------------------- ##
# Header 1
# 753 bytes
SESSION_STRUCT = struct.Struct(
    "<BbbBHBbBHHBBBBBB"
    + "fb" * 21
    + "BBB"
    + "BBBbbbbB" * 64
    + "BBIII"
    + "B" * 14
    + "I"
    + "B" * 34
    + "ff"
)


@dataclass
class Marshalzone:
    zone_start_at_lap_percentage: float
    zone_flag_type: int | str


@dataclass
class Weather:
    session_type: int | str
    time_offset: int
    weather: int | str
    track_temp_c: int
    track_temp_change_c: int | str
    air_temp_c: int
    air_temp_change_c: int | str
    rain_percentage: int


@dataclass
class SessionPacket:
    weather: int | str
    track_temp_c: int
    air_temp_c: int
    total_race_laps: int
    track_length_m: int
    session_type: int | str
    track_id: int | str
    formula: int | str
    session_time_remaining_seconds: int
    session_duration_seconds: int
    pit_speed_limit_kph: int
    game_paused: int
    is_spectating: int
    spectator_car_index: int
    sli_pro_native_support: int | str
    number_of_marshal_zones: int
    list_of_marshal_zones: list[Marshalzone]
    safety_car_status: int | str
    network_game: int | str
    number_of_weather_forecast_samples: int
    weather_forecasts: list[Weather]
    weather_forecast_accuracy: int | str
    ai_difficulty_level: int
    season_link_id: int | str
    weekend_link_id: int | str
    session_link_id: int | str
    pit_stop_ideal_lap: int
    pit_stop_latest_lap: int
    pit_stop_rejoin_position: int
    steering_assist: int | str
    braking_assist: int | str
    gearbox_assist: int | str
    pit_assist: int | str
    pit_release_assist: int | str
    ers_assist: int | str
    drs_assist: int | str
    dynamic_racing_line: int | str
    dynamic_racing_line_type: int | str
    game_mode: int
    ruleset: int
    time_of_day: int
    session_length: int | str
    speed_units_player1: int | str
    temp_units_player1: int | str
    speed_units_player2: int | str
    temp_units_player2: int | str
    number_of_safetycar_incidents: int
    number_of_virtualsafetycar_incidents: int
    number_of_red_flags: int
    equal_car_performance: int | str
    recovery_mode: int | str
    flashback_limit: int | str
    surface_type: int | str
    low_fuel_mode: int | str
    race_starts: int | str
    tyre_temps: int | str
    pit_lane_tyre_sim: int | str
    car_damage: int | str
    car_damage_rate: int | str
    collisions: int | str
    collisions_first_lap_only: int | str
    multiplayer_unsafe_pit_release: int | str
    multiplayer_kick_for_griefing: int | str
    corner_cutting_stringency: int | str
    parc_ferme: int | str
    pit_stop_experience: int | str
    safety_car: int | str
    safety_car_experience: int | str
    formation_lap: int | str
    formation_lap_experience: int | str
    red_flags: int | str
    affects_licence_level_solo: int | str
    affects_licence_level_multiplayer: int | str
    number_of_sessions_in_weekend: int
    weekend_structure: list[int]
    sector_2_start_distance_m: float
    sector_3_start_distance_m: float

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = SESSION_STRUCT.unpack_from(mem, offset)

        decoded = []

        for idx, item in enumerate(range(16)):
            item = values[idx]
            decoded.append(item)

        list_of_marshal_zones = [
            decode_decoded_enums(Marshalzone(*chunk), marshalzone_decode_mapping)
            for chunk in islice(batched(values[16:], 2, strict=True), 21)
        ]
        decoded.append(list_of_marshal_zones)

        decoded.extend(values[idx + 16 + 42] for idx in range(3))

        list_of_weather = [
            decode_decoded_enums(Weather(*chunk), weather_decode_mapping)
            for chunk in islice(batched(values[61:], 8, strict=True), 64)
        ]
        decoded.append(list_of_weather)

        decoded.extend(values[idx + 16 + 42 + 3 + 512] for idx in range(53))

        weekend_structure = [values[idx + 16 + 42 + 3 + 512 + 41] for idx in range(12)]
        decoded.append(weekend_structure)
        decoded.append(values[-2])
        decoded.append(values[-1])

        _session = decode_decoded_enums(cls(*decoded), session_decode_mapping)
        return {
            k: (
                str(v)
                if k in ["season_link_id", "weekend_link_id", "session_link_id"]
                else v
            )
            for k, v in _session.items()
        }


## ---------------------- ##
## ------ LAPDATA ------- ##
## ---------------------- ##
# Header 2
# 1285 bytes
LAPDATA_STRUCT = struct.Struct("<" + ("IIHBHBHBHBfffBBBBBBBBBBBBBBBHHBfB" * 22) + "BB")


@dataclass
class Carlap:
    last_lap_time_ms: int
    current_lap_time_ms: int
    sector1_time_ms_component: int
    sector1_time_minutes_component: int
    sector2_time_ms_component: int
    sector2_time_minutes_component: int
    delta_to_car_in_front_ms_component: int
    delta_to_car_in_front_minutes_component: int
    delta_to_leader_ms_component: int
    delta_to_leader_minutes_component: int
    lap_distance_travelled_m: float
    session_distance_travelled_m: float
    safety_car_delta: float
    car_position: int
    current_lap_number: int
    pit_status: int | str
    number_of_pit_stops: int
    sector: int | str
    current_lap_invalid: int | str
    penalties: int
    total_warnings: int
    corner_cutting_warnings: int
    number_unserved_drive_through_pens: int
    number_unserved_stop_go_pens: int
    grid_position: int
    driver_status: int | str
    result_status: int | str
    pit_lane_timer_active: int
    pit_lane_time_ms: int
    pit_lane_stop_time_ms: int
    pit_stop_must_serve_pen: int
    fastest_speed_trap_speed_kph: float
    fastest_speed_trap_lap: int


@dataclass
class LapdataPacket:
    cars: list[Carlap]
    time_trial_pb_car_idx: int
    rival_car_idx: int

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = LAPDATA_STRUCT.unpack_from(mem, offset)
        length_of_data = 33
        number_of_repeats = 22
        decoded = []
        laps = [
            decode_decoded_enums(Carlap(*chunk), lapdata_decode_mapping)
            for chunk in islice(batched(values, length_of_data), number_of_repeats)
        ]
        decoded.append(laps)
        # zero indexed
        decoded.append(values[(33 * 22) + 0])
        decoded.append(values[(33 * 22) + 1])

        return asdict(cls(*decoded))


## -------------------- ##
## ------ EVENT ------- ##
## -------------------- ##
# Header 3
# 45 bytes
EVENT_STRUCT = struct.Struct("<4s12s")


@dataclass
class EventPacket:
    event_code: str
    _registry: ClassVar[dict[str, type]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Auto-register any subclass that defines an event_code
        if hasattr(cls, "event_code"):
            EventPacket._registry[cls.event_code] = cls

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        # Entry point: reads the 4-byte event code, jumps to subclass decode logic.
        mem = memoryview(packet)
        code = struct.unpack_from("<4s", mem, offset)[0].decode("ASCII")
        payload_offset = offset + 4

        subclass = cls._registry.get(code)
        if subclass:
            return subclass._decode_payload(mem, payload_offset)

        # Simple events with no payload (SSTA, SEND, etc.)
        return asdict(cls(code))

    def _decode_payload(mem: memoryview, offset: int):
        # for subclasses that only have data
        raise NotImplementedError


@dataclass
class FastestLap(EventPacket):
    event_code: ClassVar[str] = "FTLP"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B f")  # carIdx, lapTime

    fastest_lap_car_id: int
    fastest_lap_seconds: float

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(*values))


@dataclass
class Retirement(EventPacket):
    event_code: ClassVar[str] = "RTMT"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B B")  # carIdx, reason

    retired_car_id: int
    retirement_reason: int | str

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = decode_dictionaries.retirementreason_dict[
            cls.STRUCT.unpack_from(mem, offset)
        ]
        return asdict(cls(*values))


@dataclass
class DrsDisabled(EventPacket):
    event_code: ClassVar[str] = "DRSD"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B")

    reason: int | str

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = decode_dictionaries.drsdeactivatedreason_dict[
            cls.STRUCT.unpack_from(mem, offset)
        ]
        return asdict(cls(val))


@dataclass
class Teammateinpit(EventPacket):
    event_code: ClassVar[str] = "TMPT"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B")

    car_idx_of_teammate: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(val))


@dataclass
class Racewinner(EventPacket):
    event_code: ClassVar[str] = "RCWN"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B")

    car_idx_of_winner: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(val))


@dataclass
class Penalty(EventPacket):
    event_code: ClassVar[str] = "PENA"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B B B B B B B")

    penalty_type: int | str
    infringement_type: int | str
    car_id_of_criminal: int
    car_id_of_victim: int
    time_gained: int
    lap_number_of_offence: int
    places_gained: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return decode_decoded_enums(cls(*values), penalties_decode_mapping)


@dataclass
class Speedtrap(EventPacket):
    event_code: ClassVar[str] = "SPTP"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B f B B B f")

    car_id: int
    speed_kph: float
    is_overall_fastest_in_session: int
    is_fastest_for_driver_session: int
    car_id_of_fastest_in_session: int
    fastest_speed_in_session_kph: float

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(*values))


@dataclass
class Startlights(EventPacket):
    event_code: ClassVar[str] = "STLG"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B")

    number_of_lit_lights: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(val))


@dataclass
class Drivethroughpenalty(EventPacket):
    event_code: ClassVar[str] = "DTSV"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B")

    car_idx_of_serving: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(val))


@dataclass
class Stopgopenalty(EventPacket):
    event_code: ClassVar[str] = "SGSV"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B")

    car_idx_of_serving: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(val))


@dataclass
class Flashback(EventPacket):
    event_code: ClassVar[str] = "FLBK"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<I f")

    flashback_frame_id: int
    flashback_to_time: float

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(*values))


@dataclass
class Buttonpressed(EventPacket):
    event_code: ClassVar[str] = "BUTN"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<I")

    button_pressed: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        (val,) = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(val))


@dataclass
class Overtake(EventPacket):
    event_code: ClassVar[str] = "OVTK"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B B")

    winning_car_idx: int
    losing_car_idx: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(*values))


@dataclass
class Collision(EventPacket):
    event_code: ClassVar[str] = "COLL"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B B")

    car_1_idx: int
    car_2_idx: int

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return asdict(cls(*values))


@dataclass
class Safetycar(EventPacket):
    event_code: ClassVar[str] = "SCAR"
    STRUCT: ClassVar[struct.Struct] = struct.Struct("<B B")

    safety_car_type: int | str
    safety_car_status: int | str

    @classmethod
    def _decode_payload(cls, mem: memoryview, offset: int):
        values = cls.STRUCT.unpack_from(mem, offset)
        return decode_decoded_enums(cls(*values), safetycar_decode_mapping)


## --------------------------- ##
## ------ PARTICIPANTS ------- ##
## --------------------------- ##
# Header 4
# 1284 bytes
PARTICIPANTS_STRUCT = struct.Struct("<B" + "BBBBBBB32sBBHBBBBBBBBBBBBBB" * 22)


@dataclass
class Participant:
    is_ai_controlled_flag: int
    driver_id: int
    network_id: int
    team_id: int
    my_team_flag: int
    race_number: int
    nationality: int
    name: str
    network_telemetry_flag: int | str
    show_online_names: int
    f1_world_tech_level: int
    platform: int | str
    number_of_colours: int
    livery_red_1: int
    livery_green_1: int
    livery_blue_1: int
    livery_red_2: int
    livery_green_2: int
    livery_blue_2: int
    livery_red_3: int
    livery_green_3: int
    livery_blue_3: int
    livery_red_4: int
    livery_green_4: int
    livery_blue_4: int


@dataclass
class ParticipantsPacket:
    number_of_active_cars: int
    cars: list[Participant]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = PARTICIPANTS_STRUCT.unpack_from(mem, offset)
        decoded = [values[0]]
        length_of_data = 25
        number_of_repeats = 22
        participants = [
            decode_decoded_enums(Participant(*chunk), participants_decode_mapping)
            for chunk in islice(
                batched(values[1:], length_of_data, strict=True), number_of_repeats
            )
        ]
        participants = [
            {
                k: (v.decode("utf-8").rstrip("\x00") if isinstance(v, bytes) else v)
                for participant in participants
                for k, v in participant.items()
            }
        ]
        decoded.append(participants)

        return asdict(cls(*decoded))


## ------------------------ ##
## ------ CAR SETUP ------- ##
## ------------------------ ##
# Header 5
# 1133 bytes
CARSETUP_STRUCT = struct.Struct("<" + "BBBBffffBBBBBBBBBffffBf" * 22 + "f")


@dataclass
class Setup:
    front_wing: int
    rear_wing: int
    on_throttle: int
    off_throttle: int
    front_camber: float
    rear_camber: float
    front_toe: float
    rear_toe: float
    front_suspension: int
    rear_suspension: int
    front_anti_roll_bar: int
    rear_anti_roll_bar: int
    front_suspension_height: int
    rear_suspension_height: int
    brake_pressure: int
    brake_bias: int
    engine_braking: int
    rear_left_tyre_pressure: float
    rear_right_tyre_pressure: float
    front_left_tyre_pressure: float
    front_right_tyre_pressure: float
    ballast: int
    fuel_load: float


@dataclass
class SetupPacket:
    setups: list[Setup]
    player_next_front_wing_value: float

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = CARSETUP_STRUCT.unpack_from(mem, offset)
        decoded = []
        length_of_data = 23
        number_of_repeats = 22
        setups = [
            asdict(Setup(*chunk))
            for chunk in islice(batched(values, length_of_data), number_of_repeats)
        ]
        decoded.append(setups)
        decoded.append(values[-1])

        return asdict(cls(*decoded))


## ---------------------------- ##
## ------ CAR TELEMETRY ------- ##
## ---------------------------- ##
# Header 6
# 1352 bytes
CARTELEMETRY_STRUCT = struct.Struct(
    "<" + "HfffBbHBBHHHHHBBBBBBBBHffffBBBB" * 22 + "BBb"
)


@dataclass
class Telemetry:
    speed: int
    throttle: float
    steer: float
    brake: float
    clutch: int
    gear: int
    engine_rpm: int
    drs: int | str
    rev_lights_percent: int
    rev_lights_bit_value: int
    brakes_rl_temperature: int
    brakes_rr_temperature: int
    brakes_fl_temperature: int
    brakes_fr_temperature: int
    tyres_rl_surface_temperature: int
    tyres_rr_surface_temperature: int
    tyres_fl_surface_temperature: int
    tyres_fr_surface_temperature: int
    tyres_rl_inner_temperature: int
    tyres_rr_inner_temperature: int
    tyres_fl_inner_temperature: int
    tyres_fr_inner_temperature: int
    engine_temperature: int
    tyres_rl_pressure: float
    tyres_rr_pressure: float
    tyres_fl_pressure: float
    tyres_fr_pressure: float
    surface_rl_type: int
    surface_rr_type: int
    surface_fl_type: int
    surface_fr_type: int


@dataclass
class TelemetryPacket:
    statuses: list[Telemetry]
    mfd_panel_index: int
    mfd_panel_index_secondary_player: int
    suggested_gear: int

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = CARTELEMETRY_STRUCT.unpack_from(mem, offset)
        decoded = []
        length_of_data = 31
        number_of_repeats = 22
        setups = [
            decode_decoded_enums(Telemetry(*chunk), telemetry_decode_mapping)
            for chunk in islice(
                batched(values, length_of_data, strict=True), number_of_repeats
            )
        ]
        decoded.append(setups)
        decoded.append(values[-3])
        decoded.append(values[-2])
        decoded.append(values[-1])

        return asdict(cls(*decoded))


## ------------------------- ##
## ------ CAR STATUS ------- ##
## ------------------------- ##
# Header 7
# 1239 bytes
CARSTATUS_STRUCT = struct.Struct("<" + "BBBBBfffHHBBHBBBbfffBfffB" * 22)


@dataclass
class Status:
    traction_control: int | str
    anti_lock_brakes: int | str
    fuel_mix: int | str
    front_brake_bias: int
    pit_limiter_status: int | str
    current_fuel_in_tank_kg: float
    fuel_capacity: float
    fuel_remaining_laps: float
    max_rpm: int
    idle_rpm: int
    max_gears: int
    drs_allowed: int | str
    drs_activated_in_distance: int
    actual_tyre_compound: int | str
    visual_tyre_compound: int | str
    tyre_age_laps: int
    vehicle_flags_shown: int | str
    engine_power_ice: float
    engine_power_mguk: float
    ers_store_energy: float
    ers_deploy_mode: int | str
    ers_harvested_mguk: float
    ers_harvested_mgu_h: float
    ers_deployed_this_lap: float
    network_paused: int


@dataclass
class StatusPacket:
    statuses: list[Status]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = CARSTATUS_STRUCT.unpack_from(mem, offset)
        decoded = []
        length_of_data = 25
        number_of_repeats = 22
        setups = [
            decode_decoded_enums(Status(*chunk), status_decode_mapping)
            for chunk in islice(batched(values, length_of_data), number_of_repeats)
        ]
        decoded.append(setups)

        return asdict(cls(*decoded))


## ----------------------------------- ##
## ------ FINAL CLASSIFICATION ------- ##
## ----------------------------------- ##
# Header 8
# 1042 bytes
FINALCLASSIFICATION_STRUCT = struct.Struct("<" + "B" + ("BBBBBBBId" + "B" * 27) * 22)


@dataclass
class Classification:
    position: int
    num_laps: int
    grid_position: int
    points: int
    num_pit_stops: int
    result_status: int | str
    result_reason: int | str
    best_lap_time_in_ms: int
    total_race_time: float
    penalties_time: int
    num_penalties: int
    num_tyre_stints: int
    tyre_stint_1_actual_tyre: int
    tyre_stint_1_visual_tyre: int
    tyre_stint_1_end_lap: int
    tyre_stint_2_actual_tyre: int
    tyre_stint_2_visual_tyre: int
    tyre_stint_2_end_lap: int
    tyre_stint_3_actual_tyre: int
    tyre_stint_3_visual_tyre: int
    tyre_stint_3_end_lap: int
    tyre_stint_4_actual_tyre: int
    tyre_stint_4_visual_tyre: int
    tyre_stint_4_end_lap: int
    tyre_stint_5_actual_tyre: int
    tyre_stint_5_visual_tyre: int
    tyre_stint_5_end_lap: int
    tyre_stint_6_actual_tyre: int
    tyre_stint_6_visual_tyre: int
    tyre_stint_6_end_lap: int
    tyre_stint_7_actual_tyre: int
    tyre_stint_7_visual_tyre: int
    tyre_stint_7_end_lap: int
    tyre_stint_8_actual_tyre: int
    tyre_stint_8_visual_tyre: int
    tyre_stint_8_end_lap: int


@dataclass
class ClassificationPacket:
    number_of_cars: int
    classification: list[Classification]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = FINALCLASSIFICATION_STRUCT.unpack_from(mem, offset)
        decoded = [values[0]]
        length_of_data = 36
        number_of_repeats = 22
        cars = [
            decode_decoded_enums(Classification(*chunk), classification_decode_mapping)
            for chunk in islice(batched(values[1:], length_of_data), number_of_repeats)
        ]
        decoded.append(cars)

        return asdict(cls(*decoded))


## ------------------------- ##
## ------ LOBBY INFO ------- ##
## ------------------------- ##
# Header 9
# 954 bytes
LOBBYINFO_STRUCT = struct.Struct("<B" + "BBBB32sBBBHB" * 22)


@dataclass
class Lobby:
    ai_controlled: int
    team_id: int | str
    nationality: int | str
    platform: int | str
    name: str
    car_number: int
    your_telemetry: int | str
    show_online_names: int | str
    f1_world_tech_level: int
    ready_status: int | str


@dataclass
class LobbyPacket:
    number_of_players: int
    statuses: list[Lobby]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = LOBBYINFO_STRUCT.unpack_from(mem, offset)
        decoded = [values[0]]
        length_of_data = 43
        number_of_repeats = 22
        setups = [
            decode_decoded_enums(Lobby(*chunk), lobby_decode_mapping)
            for chunk in islice(batched(values[1:], length_of_data), number_of_repeats)
        ]
        decoded.append(setups)

        return asdict(cls(decoded))


## ------------------------- ##
## ------ CAR DAMAGE ------- ##
## ------------------------- ##
# Header 10
# 1041 bytes
CARDAMAGE_STRUCT = struct.Struct("<" + "ffffBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" * 22)


@dataclass
class Damage:
    tyre_rl_wear_percentage: float
    tyre_rr_wear_percentage: float
    tyre_fl_wear_percentage: float
    tyre_fr_wear_percentage: float
    tyre_rl_damage_percentage: int
    tyre_rr_damage_percentage: int
    tyre_fl_damage_percentage: int
    tyre_fr_damage_percentage: int
    brakes_rl_damage_percentage: int
    brakes_rr_damage_percentage: int
    brakes_fl_damage_percentage: int
    brakes_fr_damage_percentage: int
    tyre_rl_blisters_percentage: int
    tyre_rr_blisters_percentage: int
    tyre_fl_blisters_percentage: int
    tyre_fr_blisters_percentage: int
    front_left_wing_damage_percentage: int
    front_right_wing_damage_percentage: int
    rear_wing_damage_percentage: int
    floor_damage_percentage: int
    diffuser_damage_percentage: int
    sidepod_damage_percentage: int
    drs_fault: int | str
    ers_fault: int | str
    gearbox_damage_percentage: int
    engine_damage_percentage: int
    engine_mguh_wear_percentage: int
    engine_es_wear_percentage: int
    engine_ce_wear_percentage: int
    engine_ice_wear_percentage: int
    engine_mguk_wear_percentage: int
    engine_tc_wear_percentage: int
    engine_blown: int | str
    engine_seized: int | str


@dataclass
class DamagePacket:
    statuses: list[Damage]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = CARDAMAGE_STRUCT.unpack_from(mem, offset)
        decoded = []
        length_of_data = 34
        number_of_repeats = 22
        setups = [
            decode_decoded_enums(Damage(*chunk), damage_decode_mapping)
            for chunk in islice(batched(values, length_of_data), number_of_repeats)
        ]
        decoded.append(setups)

        return asdict(cls(*decoded))


## ------------------------------ ##
## ------ SESSION HISTORY ------- ##
## ------------------------------ ##
# Header 11
# 1460 bytes
SESSIONHISTORY_STRUCT = struct.Struct("<BBBBBBB" + "IHBHBHBB" * 100 + "BBB" * 8)


@dataclass
class LapHistory:
    lap_time_ms: int
    sector1_time_ms_component: int
    sector1_time_minutes_component: int
    sector2_time_ms_component: int
    sector2_time_minutes_component: int
    sector3_time_ms_component: int
    sector3_time_minutes_component: int
    lap_valid_bit_flags: int


@dataclass
class TyreHistory:
    tyre_replaced_lap: int
    tyre_actual_compound: int
    tyre_visual_compound: int


@dataclass
class SessionHistoryPacket:
    relevant_car_id: int
    number_of_laps_in_data: int
    number_of_tyre_stints: int
    best_lap_number: int
    best_s1_lap_number: int
    best_s2_lap_number: int
    best_s3_lap_number: int
    lap_history_data: list[LapHistory]
    tyre_history_data: list[TyreHistory]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = SESSIONHISTORY_STRUCT.unpack_from(mem, offset)
        decoded = [values[idx] for idx in range(7)]
        length_of_laps = 8
        number_of_laps = 100
        laps = [
            asdict(LapHistory(*chunk))
            for chunk in islice(batched(values[7:], length_of_laps), number_of_laps)
        ]
        decoded.append(laps)

        length_of_tyres = 3
        number_of_tyres = 8
        tyres = [
            asdict(TyreHistory(*chunk))
            for chunk in islice(batched(values[807:], length_of_tyres), number_of_tyres)
        ]
        decoded.append(tyres)
        return asdict(cls(*decoded))


## ------------------------ ##
## ------ TYRE SETS ------- ##
## ------------------------ ##
# Header 12
# 231 bytes
TYRESETS_STRUCT = struct.Struct("<B" + "BBBBBBBhB" * 20 + "B")


@dataclass
class TyreSets:
    actual_tyre_compound: int | str
    visual_tyre_compound: int | str
    wear: int
    available: int
    recommended_session: int
    life_span: int
    usable_life: int
    lap_delta_time: int
    fitted: int


@dataclass
class TyreSetsPacket:
    car_idx: int
    tyre_set_data: list[TyreSets]
    fitted_idx: int

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = TYRESETS_STRUCT.unpack_from(mem, offset)
        decoded = [values[0]]
        length_of_data = 9
        number_of_repeats = 20
        setups = [
            asdict(TyreSets(*chunk))
            for chunk in islice(batched(values[1:], length_of_data), number_of_repeats)
        ]
        decoded.append(setups)
        decoded.append(values[-1])

        return asdict(cls(*decoded))


## ------------------------------ ##
## ------ EXTENDED MOTION ------- ##
## ------------------------------ ##
# Header 13
# 273 bytes
EXTENDEDMOTION_STRUCT = struct.Struct("<" + "f" * 61)


@dataclass
class ExMotionPacket:
    suspension_rl_position: float
    suspension_rr_position: float
    suspension_fl_position: float
    suspension_fr_position: float
    suspension_rl_velocity: float
    suspension_rr_velocity: float
    suspension_fl_velocity: float
    suspension_fr_velocity: float
    suspension_rl_acceleration: float
    suspension_rr_acceleration: float
    suspension_fl_acceleration: float
    suspension_fr_acceleration: float
    wheel_rl_speed: float
    wheel_rr_speed: float
    wheel_fl_speed: float
    wheel_fr_speed: float
    wheel_rl_slip_ratio: float
    wheel_rr_slip_ratio: float
    wheel_fl_slip_ratio: float
    wheel_fr_slip_ratio: float
    wheel_rl_slip_angle: float
    wheel_rr_slip_angle: float
    wheel_fl_slip_angle: float
    wheel_fr_slip_angle: float
    wheel_rl_lat_force: float
    wheel_rr_lat_force: float
    wheel_fl_lat_force: float
    wheel_fr_lat_force: float
    wheel_rl_long_force: float
    wheel_rr_long_force: float
    wheel_fl_long_force: float
    wheel_fr_long_force: float
    height_of_cog_above_ground: float
    local_velocity_x: float
    local_velocity_y: float
    local_velocity_z: float
    angular_velocity_x: float
    angular_velocity_y: float
    angular_velocity_z: float
    angular_acceleration_x: float
    angular_acceleration_y: float
    angular_acceleration_z: float
    front_wheels_angle: float
    wheel_rl_vert_force: float
    wheel_rr_vert_force: float
    wheel_fl_vert_force: float
    wheel_fr_vert_force: float
    front_aero_height: float
    rear_aero_height: float
    front_roll_angle: float
    rear_roll_angle: float
    chassis_yaw: float
    chassis_pitch: float
    wheel_rl_camber: float
    wheel_rr_camber: float
    wheel_fl_camber: float
    wheel_fr_camber: float
    wheel_rl_camber_gain: float
    wheel_rr_camber_gain: float
    wheel_fl_camber_gain: float
    wheel_fr_camber_gain: float

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = EXTENDEDMOTION_STRUCT.unpack_from(mem, offset)
        return asdict(cls(*values))


## ------------------------- ##
## ------ TIME TRIAL ------- ##
## ------------------------- ##
# Header 14
# 101 bytes
TIMETRIAL_STRUCT = struct.Struct("<" + "BBIIIIBBBBBB" * 3)


@dataclass
class TimeTrial:
    car_idx: int
    team_id: int
    lap_time_in_ms: int
    sector1_time_in_ms: int
    sector2_time_in_ms: int
    sector3_time_in_ms: int
    traction_control: int
    gearbox_assist: int
    anti_lock_brakes: int
    equal_car_performance: int
    custom_setup: int
    valid: int


@dataclass
class TimeTrialPacket:
    player_session_best_data_set: TimeTrial
    personal_best_data_set: TimeTrial
    rival_data_set: TimeTrial

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = TIMETRIAL_STRUCT.unpack_from(mem, offset)
        length_of_data = 12
        number_of_repeats = 3
        setups = [
            TimeTrial(*chunk)
            for chunk in islice(batched(values, length_of_data), number_of_repeats)
        ]

        return asdict(cls(*setups))


## ------------------------------- ##
## ------ POSITION HISTORY ------- ##
## ------------------------------- ##
# Header 15
# 1131 bytes
LAPPOSITION_STRUCT = struct.Struct("<BB" + "B" * 1100)


@dataclass
class LapPositionPacket:
    laps_in_data: int
    lap_where_data_starts: int
    position_for_vehicle_idx: list[list[int]]

    @classmethod
    def decode(cls, packet: bytes, offset: int = 29):
        mem = memoryview(packet)
        values = LAPPOSITION_STRUCT.unpack_from(mem, offset)
        decoded = []
        decoded.append(values[0])
        decoded.append(values[1])
        length_of_data = 50
        number_of_repeats = 22
        cars = [
            ",".join(str(list(chunk)))
            for chunk in islice(batched(values[2:], length_of_data), number_of_repeats)
        ]
        decoded.append(cars)

        return asdict(cls(*decoded))
