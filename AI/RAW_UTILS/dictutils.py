def invert_dict(d):
    out = {}
    for k, v in d.items():
        out.setdefault(v, []).append(k)
    return out


def merge_dicts(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out


def nested_get(d, keys, default=None):
    cur = d
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur


def nested_set(d, keys, value):
    cur = d
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = value
    return d
