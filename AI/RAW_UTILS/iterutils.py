def chunked(iterable, size):
    if size <= 0:
        return []
    return [list(iterable[i : i + size]) for i in range(0, len(iterable), size)]


def flatten(list_of_lists):
    return [item for sub in list_of_lists for item in sub]


def sliding_window(seq, size):
    if size <= 0:
        return []
    return [seq[i : i + size] for i in range(len(seq) - size + 1)]


def unique_everseen(seq):
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out
