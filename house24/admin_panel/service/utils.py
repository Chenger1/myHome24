def prepare_error_message(errors):
    result = {}
    if isinstance(errors, list):
        for item in errors:
            for key, value in item.items():
                result[key] = value
    elif isinstance(errors, dict):
        result.update(errors)
    return result
