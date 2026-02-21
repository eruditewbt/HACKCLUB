def drop_nulls(rows, keys=None):
    """Drop rows that have None or empty values for given keys."""
    out = []
    for row in rows:
        if keys is None:
            ok = all(v is not None and v != "" for v in row.values())
        else:
            ok = all(row.get(k) is not None and row.get(k) != "" for k in keys)
        if ok:
            out.append(row)
    return out


def fill_nulls(rows, value=0, keys=None):
    """Fill None or empty values with a default value."""
    out = []
    for row in rows:
        new_row = dict(row)
        if keys is None:
            for k, v in new_row.items():
                if v is None or v == "":
                    new_row[k] = value
        else:
            for k in keys:
                if new_row.get(k) is None or new_row.get(k) == "":
                    new_row[k] = value
        out.append(new_row)
    return out


def strip_strings(rows, keys=None):
    """Strip whitespace from string fields."""
    out = []
    for row in rows:
        new_row = dict(row)
        if keys is None:
            for k, v in new_row.items():
                if isinstance(v, str):
                    new_row[k] = v.strip()
        else:
            for k in keys:
                v = new_row.get(k)
                if isinstance(v, str):
                    new_row[k] = v.strip()
        out.append(new_row)
    return out


def cast_types(rows, schema):
    """Cast row fields to given types. schema is dict of key -> callable."""
    out = []
    for row in rows:
        new_row = dict(row)
        for k, caster in schema.items():
            if k in new_row and new_row[k] is not None and new_row[k] != "":
                new_row[k] = caster(new_row[k])
        out.append(new_row)
    return out
