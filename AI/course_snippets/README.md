# course_snippets
Small, stdlib-only “teaching scripts” and mini labs.

## Existing scripts
- `basic_rag_demo.py`
- `llm_prompt_with_schema.py`
- `model_eval_template.py`
- `tiny_nn_binary_classifier.py`

## Labs
Runnable, slightly more structured exercises under `course_snippets/labs/`:
- `rag_lab`: chunking + lexical retrieval + a tiny demo QA loop.
- `schema_prompt_lab`: parse/validate strict JSON outputs with helpful errors.
- `eval_lab`: metrics + error analysis helpers.
- `nn_lab`: tiny logistic regression training demo (no numpy).

## Run
```bash
python -m course_snippets.labs.rag_lab.demo
python -m course_snippets.labs.schema_prompt_lab.demo
python -m course_snippets.labs.eval_lab.demo
python -m course_snippets.labs.nn_lab.demo
```

