def normalize_newlines(obj):
    if isinstance(obj, str):
        return obj.replace('\r\n', '\n').replace('\r', '\n')
    elif isinstance(obj, dict):
        return {key: normalize_newlines(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [normalize_newlines(element) for element in obj]
    else:
        return obj
