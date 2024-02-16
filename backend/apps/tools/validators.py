async def validate_json(json: dict, keys_types: dict[str,tuple[type]]) -> bool:
    for key, value in json.items():
        if key not in keys_types.keys():
            return False
        key_type = keys_types.get(key)
        
        if not isinstance(value, key_type):
            return False

    return True
