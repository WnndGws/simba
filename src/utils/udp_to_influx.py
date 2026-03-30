#!/usr/bin/env python
"""#!/usr/bin/env -S uv run --script
## Run this script using uv
## init uv with `uv init && uv venv && source .venv/bin/activate`
## Check `skeletons/tools/py` for a list of currently preferred tools
"""

import atexit  # CHANGED
import os  # CHANGED
from concurrent.futures import ProcessPoolExecutor  # CHANGED
from dataclasses import asdict
from multiprocessing import get_context  # CHANGED

from rich import print

from config import cached_values
from models import udp_collected, udp_protocol

### ------------------------ ###
### --- Helper Functions --- ###
### ------------------------ ###
collected_player_cars = {
    idx: asdict(udp_collected.PlayerCollectedCar()) for idx in range(2)
}
collected_ai_cars = {
    idx: asdict(udp_collected.AllCarsCollectedCar()) for idx in range(22)
}
collected_session = asdict(udp_collected.CollectedSession())


def map_dataclass_to_collectedclass(fromclass, tocollected, prefix: str) -> None:
    for name, value in fromclass.items():
        dest = f"{prefix}_{name}"
        if dest in tocollected:
            tocollected[dest] = value


# worker function run in child processes to prepare per-car updates
def _prepare_item(idx, item, prefix, player1_idx, player2_idx):
    """Prepare a dict of fields to update for a single car.
    This is executed in a child process so it returns only serializable data.
    """
    result = {}
    for name, value in item.items():
        dest = f"{prefix}_{name}"
        result[dest] = value

    # set aaa_car_idx similar to previous logic
    if idx == player1_idx:
        result["aaa_car_idx"] = player1_idx
    elif idx == player2_idx:
        result["aaa_car_idx"] = player2_idx
    else:
        result["aaa_car_idx"] = idx

    return idx, result


# CHANGED: persistent process pool (lazy init) to avoid creating a pool on every call
_pool = None  # CHANGED
_pool_ctx = get_context("spawn")  # CHANGED


def _init_pool(max_workers: int = None):
    global _pool
    if _pool is not None:
        return _pool
    cpu = os.cpu_count() or 1
    # default: use half the CPUs but at least 1
    suggested = max(1, int(cpu / 2))
    max_workers = max_workers or suggested
    # Use ProcessPoolExecutor via the spawn context for compatibility
    _pool = ProcessPoolExecutor(
        max_workers=max_workers, mp_context=_pool_ctx
    )  # CHANGED
    atexit.register(_shutdown_pool)  # CHANGED
    return _pool


def _shutdown_pool():
    global _pool
    if _pool is not None:
        try:
            _pool.shutdown(wait=True)
        except Exception:
            pass
        _pool = None


update_count = 0


# CHANGED: use the persistent pool instead of creating one per call
def update_cars_data(itterable, prefix: str):
    """Parallelize per-car mapping/processing in worker processes and then
    merge the updates back into the global collected_* dictionaries.
    """
    args = [
        (
            idx,
            item,
            prefix,
            cached_values.player1_car_index,
            cached_values.player2_car_index,
        )
        for idx, item in enumerate(itterable)
    ]

    if not args:
        return

    pool = _init_pool()

    # Use map-style execution on the existing pool
    # Note: ProcessPoolExecutor.map preserves order; starmap equivalent via generator
    futures = []
    for a in args:
        futures.append(pool.submit(_prepare_item, *a))

    results = [f.result() for f in futures]

    # merge results back into global dictionaries (only update keys that exist)
    for idx, upd in results:
        if idx == cached_values.player1_car_index:
            dict_item = collected_player_cars[0]
        elif idx == cached_values.player2_car_index:
            dict_item = collected_player_cars[1]
        else:
            # if AI range possibly out-of-bounds fallback to existing dicts guard
            dict_item = collected_ai_cars.get(idx, {})

        # update only keys that exist in target dict (preserve original behavior)
        for k, v in upd.items():
            if k in dict_item:
                dict_item[k] = v

        # maintain original print for player 1 (as was in original code)
        if idx == cached_values.player1_car_index:
            global update_count
            update_count += 1
            print(f"updated {update_count} times")


### ------------ ###
### --- Data --- ###
### ------------ ###


def handle_header(packet: bytes):
    header = udp_protocol.Header.decode(packet)
    map_dataclass_to_collectedclass(header, collected_session, "header")
    cached_values.player1_car_index = header["player_car_index"]
    cached_values.player2_car_index = header["player2_car_index"]


def handle_motion(packet: bytes):
    prefix = "motion"
    motion = udp_protocol.MotionPacket.decode(packet)
    update_cars_data(motion["cars"], prefix)


def handle_session(packet: bytes):
    session = udp_protocol.SessionPacket.decode(packet)
    map_dataclass_to_collectedclass(session, collected_session, "session")


def handle_lapdata(packet: bytes):
    prefix = "lapdata"
    lapdata = udp_protocol.LapdataPacket.decode(packet)
    update_cars_data(lapdata["cars"], prefix)
    cached_values.player1_position = collected_player_cars[0]["lapdata_car_position"]
    if cached_values.player2_car_index != 255:
        cached_values.player2_position = collected_player_cars[1][
            "lapdata_car_position"
        ]


def handle_event(packet: bytes):
    event = udp_protocol.EventPacket.decode(packet)
    map_dataclass_to_collectedclass(event, collected_session, "event")


def handle_participants(packet: bytes):
    participants = udp_protocol.ParticipantsPacket.decode(packet)
    prefix = "participants"
    update_cars_data(participants["cars"], prefix)


def handle_setups(packet: bytes):
    setups = udp_protocol.SetupPacket.decode(packet)
    prefix = "setup"
    update_cars_data(setups["setups"], prefix)


def handle_telemetry(packet: bytes):
    telemetry = udp_protocol.TelemetryPacket.decode(packet)
    prefix = "telemetry"
    update_cars_data(telemetry["statuses"], prefix)


def handle_status(packet: bytes):
    status = udp_protocol.StatusPacket.decode(packet)
    prefix = "status"
    update_cars_data(status["statuses"], prefix)


def handle_classification(packet: bytes):
    classification = udp_protocol.ClassificationPacket.decode(packet)
    prefix = "classification"
    update_cars_data(classification["classification"], prefix)


def handle_lobby(packet: bytes):
    lobby = udp_protocol.LobbyPacket.decode(packet)
    prefix = "lobby"
    update_cars_data(lobby["statuses"], prefix)


def handle_damage(packet: bytes):
    damage = udp_protocol.DamagePacket.decode(packet)
    prefix = "damage"
    update_cars_data(damage["statuses"], prefix)


def handle_positionhistory(packet: bytes):
    history = udp_protocol.LapPositionPacket.decode(packet)
    prefix = "positionhistory"
    # update_cars_data(history["position_for_vehicle_idx"], prefix)


def handle_exmotion(packet: bytes):
    exmotion = udp_protocol.ExMotionPacket.decode(packet)
    map_dataclass_to_collectedclass(exmotion, collected_player_cars[0], "extmotion_")


def handle_sessionhistory(packet: bytes):
    # NB. different to others
    history = udp_protocol.SessionHistoryPacket.decode(packet)
    if history["relevant_car_id"] == cached_values.player1_car_index:
        dict_item = collected_player_cars[0]
    elif history["relevant_car_id"] == cached_values.player2_car_index:
        dict_item = collected_player_cars[1]
    else:
        dict_item = collected_ai_cars[history["relevant_car_id"]]

    # zero indexed
    map_dataclass_to_collectedclass(
        history["lap_history_data"][history["number_of_laps_in_data"] - 1],
        dict_item,
        "laphistory_last_lap_",
    )
    map_dataclass_to_collectedclass(
        history["lap_history_data"][history["best_s1_lap_number"] - 1],
        dict_item,
        "laphistory_fastest_s1lap_",
    )
    map_dataclass_to_collectedclass(
        history["lap_history_data"][history["best_s2_lap_number"] - 1],
        dict_item,
        "laphistory_fastest_s2lap_",
    )
    map_dataclass_to_collectedclass(
        history["lap_history_data"][history["best_s3_lap_number"] - 1],
        dict_item,
        "laphistory_fastest_s3lap_",
    )
    map_dataclass_to_collectedclass(
        history["lap_history_data"][history["best_lap_number"] - 1],
        dict_item,
        "laphistory_fastest_lap_",
    )


def handle_tyresets(packet: bytes):
    # NB. different to others
    tyres = udp_protocol.TyreSetsPacket.decode(packet)
    if tyres["car_idx"] == cached_values.player1_car_index:
        dict_item = collected_player_cars[0]
    elif tyres["car_idx"] == cached_values.player2_car_index:
        dict_item = collected_player_cars[1]
    else:
        dict_item = collected_ai_cars[tyres["car_idx"]]

    softs = [
        tyre for tyre in tyres["tyre_set_data"] if tyre["visual_tyre_compound"] == 16
    ]
    mediums = [
        tyre for tyre in tyres["tyre_set_data"] if tyre["visual_tyre_compound"] == 17
    ]
    hards = [
        tyre for tyre in tyres["tyre_set_data"] if tyre["visual_tyre_compound"] == 18
    ]
    inters = [
        tyre for tyre in tyres["tyre_set_data"] if tyre["visual_tyre_compound"] == 7
    ]

    dict_item["tyresets_softs_number_of_new_available"] = len(
        [tyre for tyre in softs if tyre["available"] == 1]
    )
    dict_item["tyresets_softs_number_of_used_available"] = (
        len(softs) - dict_item["tyresets_softs_number_of_new_available"]
    )
    dict_item["tyresets_softs_best_actual_compound"] = softs[0]["actual_tyre_compound"]
    dict_item["tyresets_softs_best_wear"] = min([tyre["wear"] for tyre in softs])
    tyresets_softs_best_available = next(
        tyre for tyre in softs if tyre["wear"] == dict_item["tyresets_softs_best_wear"]
    )
    dict_item["tyresets_softs_best_recommended_session"] = (
        tyresets_softs_best_available["recommended_session"]
    )
    dict_item["tyresets_softs_best_life_span"] = tyresets_softs_best_available[
        "life_span"
    ]
    dict_item["tyresets_softs_best_usable_life"] = tyresets_softs_best_available[
        "usable_life"
    ]
    dict_item["tyresets_softs_best_lap_delta_time"] = tyresets_softs_best_available[
        "lap_delta_time"
    ]

    dict_item["tyresets_mediums_number_of_new_available"] = len(
        [tyre for tyre in mediums if tyre["available"] == 1]
    )
    dict_item["tyresets_mediums_number_of_used_available"] = (
        len(mediums) - dict_item["tyresets_mediums_number_of_new_available"]
    )
    dict_item["tyresets_mediums_best_actual_compound"] = mediums[0][
        "actual_tyre_compound"
    ]
    dict_item["tyresets_mediums_best_wear"] = min([tyre["wear"] for tyre in mediums])
    tyresets_mediums_best_available = next(
        tyre
        for tyre in mediums
        if tyre["wear"] == dict_item["tyresets_mediums_best_wear"]
    )
    dict_item["tyresets_mediums_best_recommended_session"] = (
        tyresets_mediums_best_available["recommended_session"]
    )
    dict_item["tyresets_mediums_best_life_span"] = tyresets_mediums_best_available[
        "life_span"
    ]
    dict_item["tyresets_mediums_best_usable_life"] = tyresets_mediums_best_available[
        "usable_life"
    ]
    dict_item["tyresets_mediums_best_lap_delta_time"] = tyresets_mediums_best_available[
        "lap_delta_time"
    ]

    dict_item["tyresets_hards_number_of_new_available"] = len(
        [tyre for tyre in hards if tyre["available"] == 1]
    )
    dict_item["tyresets_hards_number_of_used_available"] = (
        len(hards) - dict_item["tyresets_hards_number_of_new_available"]
    )
    dict_item["tyresets_hards_best_actual_compound"] = hards[0]["actual_tyre_compound"]
    dict_item["tyresets_hards_best_wear"] = min([tyre["wear"] for tyre in hards])
    tyresets_hards_best_available = next(
        tyre for tyre in hards if tyre["wear"] == dict_item["tyresets_hards_best_wear"]
    )
    dict_item["tyresets_hards_best_recommended_session"] = (
        tyresets_hards_best_available["recommended_session"]
    )
    dict_item["tyresets_hards_best_life_span"] = tyresets_hards_best_available[
        "life_span"
    ]
    dict_item["tyresets_hards_best_usable_life"] = tyresets_hards_best_available[
        "usable_life"
    ]
    dict_item["tyresets_hards_best_lap_delta_time"] = tyresets_hards_best_available[
        "lap_delta_time"
    ]

    dict_item["tyresets_inters_number_of_new_available"] = len(
        [tyre for tyre in inters if tyre["available"] == 1]
    )
    dict_item["tyresets_inters_number_of_used_available"] = (
        len(inters) - dict_item["tyresets_inters_number_of_new_available"]
    )
    dict_item["tyresets_inters_best_actual_compound"] = inters[0][
        "actual_tyre_compound"
    ]
    dict_item["tyresets_inters_best_wear"] = min([tyre["wear"] for tyre in inters])
    tyresets_inters_best_available = next(
        tyre
        for tyre in inters
        if tyre["wear"] == dict_item["tyresets_inters_best_wear"]
    )
    dict_item["tyresets_inters_best_recommended_session"] = (
        tyresets_inters_best_available["recommended_session"]
    )
    dict_item["tyresets_inters_best_life_span"] = tyresets_inters_best_available[
        "life_span"
    ]
    dict_item["tyresets_inters_best_usable_life"] = tyresets_inters_best_available[
        "usable_life"
    ]
    dict_item["tyresets_inters_best_lap_delta_time"] = tyresets_inters_best_available[
        "lap_delta_time"
    ]
