from . import dataset_utils as utils_csv
from . import io_utils as utils_io


def load_list_from_csv(file: str) -> list[dict]:
    return utils_csv.file_csv_to_json(file)


def save_list_to_csv(file: str, data: list[dict]):
    utils_csv.json_to_file_csv(file, data)


def load_list_from_json(file: str) -> list[dict]:
    return utils_io.read_json(file)


def save_list_to_json(file: str, data: list[dict]):
    utils_io.write_json(file, data)
