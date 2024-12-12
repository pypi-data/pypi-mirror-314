import json


def format_json(data: dict) -> dict:
    _data = json.dumps(data, default=str)
    return json.loads(_data)


def convert_json_to_object(data: dict, class_name):
    _json_formatted = format_json(data)
    return class_name(**_json_formatted, )


def convert_array_json_to_objects(data: list[dict], class_name) -> list:
    return [convert_json_to_object(item, class_name) for item in data]
