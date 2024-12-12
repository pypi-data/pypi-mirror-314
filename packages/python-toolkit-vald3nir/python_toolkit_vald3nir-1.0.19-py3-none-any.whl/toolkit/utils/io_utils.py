import json
import os
import shutil


def list_all_sub_folders(directory) -> list[str]:
    _files = []
    for root, dirs, _ in os.walk(directory):
        return dirs
    return _files


def list_all_files(directory) -> list[str]:
    _files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            _files.append(os.path.join(root, file))
    return _files


def list_files_for_extension(directory, extension) -> list[str]:
    _files = []
    for file in list_all_files(directory):
        if file.endswith(extension):
            _files.append(file)
    return _files


def read_json(file):
    with open(file, encoding="utf8") as f:
        return json.load(f)


def write_json(file, data):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_lines(file_path: str, lines: list[str]):
    try:
        create_folder(os.path.dirname(file_path))
        f = open(file_path, "w")
        for line in lines:
            f.write(line)
        f.close()
    except Exception as e:
        print("Error to write file:", file_path)
        print(str(e))


def rename_file(file_name: str, new_file_name: str):
    try:
        print('-------------------------------------------------------')
        print(" * ", file_name)
        print("-> ", new_file_name)
        if not exist_file(new_file_name):
            os.rename(file_name, new_file_name)
    except Exception as e:
        print("Error when renaming files", file_name, new_file_name)
        print(str(e))


def delete_file(file: str):
    try:
        if os.path.exists(file):
            os.remove(file)
    except Exception as e:
        print(str(e))


def delete_folder(folder: str):
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    except Exception as e:
        print(str(e))


def exist_file(file):
    return os.path.exists(file)


def create_folder(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
