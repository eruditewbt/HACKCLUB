from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional


@dataclass(frozen=True)
class CsvReadOptions:
    delimiter: Optional[str] = None
    encoding: str = "utf-8"


def _sniff_delimiter(sample: str) -> str:
    # Safe heuristic: prefer commas, then tabs, then semicolons.
    if "\t" in sample and sample.count("\t") > sample.count(","):
        return "\t"
    if ";" in sample and sample.count(";") > sample.count(","):
        return ";"
    return ","


def iter_csv_rows(path: str, *, options: Optional[CsvReadOptions] = None, max_rows: Optional[int] = None) -> Iterator[Dict[str, str]]:
    options = options or CsvReadOptions()

    with open(path, "r", encoding=options.encoding, newline="") as f:
        if options.delimiter is None:
            head = f.read(4096)
            f.seek(0)
            delimiter = _sniff_delimiter(head)
        else:
            delimiter = options.delimiter

        reader = csv.DictReader(f, delimiter=delimiter)
        n = 0
        for row in reader:
            yield {k: ("" if v is None else str(v)) for k, v in row.items()}
            n += 1
            if max_rows is not None and n >= max_rows:
                return


def read_csv_head(path: str, *, n: int = 20, options: Optional[CsvReadOptions] = None) -> List[Dict[str, str]]:
    return list(iter_csv_rows(path, options=options, max_rows=n))
