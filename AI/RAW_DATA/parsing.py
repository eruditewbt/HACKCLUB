import csv
import json


def read_csv(path, delimiter=",", has_header=True):
    """Read CSV file. Returns list of dicts if header exists, else list of lists."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)
    if not rows:
        return []
    if has_header:
        header = rows[0]
        return [dict(zip(header, row)) for row in rows[1:]]
    return rows


def read_tsv(path, has_header=True):
    return read_csv(path, delimiter="	", has_header=has_header)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_kv_lines(text, sep="=", comment="#"):
    """Parse key-value pairs from lines of text."""
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(comment):
            continue
        if sep in line:
            k, v = line.split(sep, 1)
            out[k.strip()] = v.strip()
    return out
