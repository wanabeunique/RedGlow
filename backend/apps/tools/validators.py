from typing import Iterable


async def validate_json(json: dict, keys: Iterable) -> bool:
    for key in json.keys():
        if key not in keys:
            return False

    return True
