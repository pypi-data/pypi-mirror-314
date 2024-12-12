import logging
from copy import deepcopy
from halerium_utilities.board.schemas import Node

def migrate_board(board_dict):

    # 1. check version before starting migration
    if board_dict.get("version", None) != "2.0":
        raise Exception("Input board has wrong version.")

    migrated_board = deepcopy(board_dict)
    migrated_board["version"] = "2.1"

    # 1. Change store_uuids of setup_args from array to dictionary
    for node in [node for node in migrated_board["nodes"]
                 if node["type"] == "setup" and
                    node["type_specific"]["setup_args"].get("store_uuids", None)]:
        new_store_uuids = {}
        store_uuids =node["type_specific"]["setup_args"]["store_uuids"]

        for uuid in store_uuids:
            new_store_uuids[uuid] = ["read", "write"]

        node["type_specific"]["setup_args"]["store_uuids"] = new_store_uuids

    return migrated_board
