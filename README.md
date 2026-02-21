# HACKCLUB

Practical AI, Python, and web experimentation workspace with course content, runnable snippets, and prototype systems.

## What This Repository Contains

- `COURSE/`: Structured learning content.
- `AI/`: AI algorithms, math/ML/text/data utility libraries, and automation experiments.
- `WEB/`: Web-focused agent/service experiments and course snippets.
- `python_snippets/`: Fundamentals and quick practice scripts.
- `translate/`: Dart-based translation CLI/package experiments.
- `workspace/`: Miscellaneous standalone code/docs scratch area.

## High-Level Directory Overview

- `COURSE/python_ai_modular/`
  - Browser-based modular curriculum (`index.html`) with module pages in `modules/`.
- `COURSE/stanford/`
  - Stanford AI PDF references (Courses 1-4).
- `AI/course_snippets/`
  - Small runnable AI examples (RAG demo, prompt schema usage, tiny NN baseline).
- `WEB/course_snippets/`
  - Production-oriented snippets (FastAPI inference pattern, request validation, config/logging).
- `AI/RAW_*`
  - Reference mini-libraries for math, ML, text processing, data handling, algorithms, and utils.

## Course Roadmap (Recommended Sequence)

Use this sequence for a complete path from fundamentals to production:

1. `COURSE/python_ai_modular/modules/01_python_foundations.html`
2. `COURSE/python_ai_modular/modules/02_python_for_ai.html`
3. `COURSE/python_ai_modular/modules/03_math_stats.html`
4. `COURSE/python_ai_modular/modules/04_ml_core.html`
5. `COURSE/python_ai_modular/modules/05_deep_learning.html`
6. `COURSE/python_ai_modular/modules/06_classical_ai.html`
7. `COURSE/python_ai_modular/modules/07_llm_engineering.html`
8. `COURSE/python_ai_modular/modules/08_production_python.html`
9. `COURSE/python_ai_modular/modules/09_mlops_eval_safety.html`
10. `COURSE/python_ai_modular/modules/10_capstones.html`
11. `COURSE/python_ai_modular/modules/11_snippet_catalog.html`
12. `COURSE/python_ai_modular/modules/12_project_showcase.html`
13. Stanford reference reinforcement:
   - `COURSE/stanford/Stanford_AI__COURSE 1.pdf`
   - `COURSE/stanford/Stanford_AI__COURSE 2 (search 2 - Gaming 2).pdf`
   - `COURSE/stanford/Stanford_AI__COURSE 3 (Factor graph I -  II).pdf`
   - `COURSE/stanford/Stanford_AI__COURSE 4 (Bayesian Network 1-2-3).pdf`

## Referenced Files To Use During the Course

- Python fundamentals:
  - `python_snippets/course_basics/variables_and_flow.py`
  - `python_snippets/course_basics/functions_and_oop.py`
  - `python_snippets/course_basics/errors_and_files.py`
- AI practice snippets:
  - `AI/course_snippets/basic_rag_demo.py`
  - `AI/course_snippets/llm_prompt_with_schema.py`
  - `AI/course_snippets/model_eval_template.py`
  - `AI/course_snippets/tiny_nn_binary_classifier.py`
- Web production snippets:
  - `WEB/course_snippets/fastapi_inference_service.py`
  - `WEB/course_snippets/request_validation_example.py`
  - `WEB/course_snippets/config_and_logging.py`
- Supporting reference libraries:
  - `AI/RAW_MATH/README.md`
  - `AI/RAW_ML/README.md`
  - `AI/RAW_TEXT/README.md`
  - `AI/RAW_DATA/README.md`
  - `AI/RAW_ALGOS/README.md`
  - `AI/RAW_UTILS/README.md`

## Learning Outcomes Matrix

By completing the roadmap, learners should be able to:

1. Build Python-first data and preprocessing workflows for AI tasks.
2. Implement baseline ML models and evaluate them with defensible metrics.
3. Apply classical AI methods (search/planning/value iteration) to decision problems.
4. Build LLM workflows with schema-driven prompting and basic RAG structure.
5. Ship API-ready inference patterns with validation, logging, and reproducibility.
6. Design capstone projects with testing, documentation, and safety constraints.

## Course Review and Perfection Notes

Current status from repository review:

1. Module `01` now has authored content and learning objectives.
2. Module `11` (Snippet Catalog and Run Guide) now exists and matches index links.
3. Module files `01` through `11` are now present and sequenced coherently.

Recommended perfection order:

1. Add a short completion checklist at the end of every module file (`02`-`10`) for consistency.
2. Add a lightweight test/run command block to each module page.
3. Add a single progress tracker page (module completion + capstone milestones).
4. Add an optional answer key/rubric appendix for assessments.

## Progress and Completion Standard

Use this standard to confirm course completion quality:

1. Every module run guide command is executed at least once.
2. Each module includes one implementation extension beyond the base example.
3. At least one capstone is delivered with tests and a reproducible run script.
4. Final capstone README documents architecture, metrics, and failure modes.

## Additional Improvement Tracks

Optional but recommended enhancements:

1. Add a `COURSE/python_ai_modular/modules/13_assessment_rubrics.html` page for module quizzes and rubric-backed grading.
2. Add a repo-level `Makefile` or `task runner` for common setup/run/test commands.
3. Add lightweight CI checks for snippet syntax and basic import validation.
4. Add module-level quizzes and solution rubric files under `COURSE/python_ai_modular/modules/`.

## Quick Start

From repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pytest fastapi uvicorn pydantic numpy pandas scikit-learn matplotlib
```

Then open:

- `COURSE/python_ai_modular/index.html`

## Notes

- This repo contains large and many files; this README intentionally focuses on high-value overview and course navigation.
- `llm.db` and dataset files are present for local experiments and should be handled as local/dev assets unless formalized.
