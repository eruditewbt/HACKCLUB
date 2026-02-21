# RAW_DATA

Pure-Python data parsing and cleaning utilities.

## Modules
- `parsing.py`: Read CSV/TSV/JSON and parse key-value lines.
- `cleaning.py`: Drop/fill nulls, strip strings, cast types.
- `validation.py`: Basic validators for email, URL, int/float, date.
- `dataset.py`: Lightweight dataset wrapper around list-of-dicts.

## Quick start
```python
from RAW_DATA import read_csv, strip_strings, cast_types

rows = read_csv("data.csv")
rows = strip_strings(rows)
rows = cast_types(rows, {"age": int})
```

## Notes
- CSV reader returns list-of-dicts if `has_header=True`.
- Validators are regex-based and intentionally simple.
