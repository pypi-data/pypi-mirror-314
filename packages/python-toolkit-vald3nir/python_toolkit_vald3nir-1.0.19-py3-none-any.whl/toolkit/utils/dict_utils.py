def dict_size(d: dict) -> int:
    size = 0
    for i in d.values():
        size += len(i)
    return size
