# RAW_UTILS

General-purpose pure-Python utility helpers.

## Modules
- `iterutils.py`: Chunking, flattening, sliding windows, unique order.
- `dictutils.py`: Invert, merge, nested get/set.
- `textfile.py`: Read/write text and line files.

## Quick start
```python
from RAW_UTILS import chunked, nested_get

print(chunked([1, 2, 3, 4, 5], 2))
print(nested_get({"a": {"b": 1}}, ["a", "b"]))
```
