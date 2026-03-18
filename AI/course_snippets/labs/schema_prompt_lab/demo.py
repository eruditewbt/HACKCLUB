from __future__ import annotations

import json

from .schema import Field, validate_object


def main():
    fields = [
        Field("title", str, required=True),
        Field("summary", str, required=True),
        Field("risks", list, required=False),
    ]

    print("Schema prompt lab. Paste JSON; it will be validated.\n")
    while True:
        raw = input("JSON (empty to quit): ").strip()
        if not raw:
            break
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}\n")
            continue
        ok, errors = validate_object(obj, fields)
        if ok:
            print("OK\n")
        else:
            print("Errors:")
            for err in errors:
                print(f"- {err}")
            print()


if __name__ == "__main__":
    main()

