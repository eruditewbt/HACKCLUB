import json


PROMPT = """
You are a strict JSON assistant.
Return exactly this schema:
{
  "summary": "string",
  "action_items": ["string"]
}
""".strip()


def parse_model_output(raw_text):
    data = json.loads(raw_text)
    if not isinstance(data, dict):
        raise ValueError("Output must be JSON object")
    if "summary" not in data or "action_items" not in data:
        raise ValueError("Missing required fields")
    if not isinstance(data["summary"], str):
        raise ValueError("summary must be string")
    if not isinstance(data["action_items"], list):
        raise ValueError("action_items must be list")
    return data


def main():
    mock_output = '{"summary":"Team meeting moved to Friday","action_items":["Update calendar","Notify participants"]}'
    parsed = parse_model_output(mock_output)
    print("parsed=", parsed)


if __name__ == "__main__":
    main()
