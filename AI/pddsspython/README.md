# pddsspython
Python reference implementation of the PDSS + intelligent planner.

This is *not* what Netlify deploys (Netlify Functions use Node.js). The deployed API lives under `pddss/netlify/functions/` as JavaScript.

Use this folder when you want:
- a Python-only local planner
- easy experimentation/debugging of the planning logic

## Run (CLI)
```bash
python pddsspython/cli.py --prompt "Build a web app for scheduling tutors with payments and realtime chat."
```

## Examples
- `examples/sample_prompts.jsonl`

