import base64
import json
import os
import sys

# Ensure project root is on path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pdss_prob import ProjectDSS
from intel_planner import REQUIRED_KEYS, prompt_to_pdss_input, advanced_project_plan


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(body),
    }


def handler(event, context):
    method = event.get("httpMethod", "GET")

    if method == "OPTIONS":
        return _response(200, {"ok": True})

    if method == "GET":
        return _response(200, {
            "ok": True,
            "message": "POST JSON with prompt or project_characteristics to get an advanced plan.",
            "required_keys": REQUIRED_KEYS,
            "example": {
                "prompt": "Build a web app for scheduling tutors with payments, admin analytics, and realtime chat."
            }
        })

    if method != "POST":
        return _response(405, {"ok": False, "error": "Method not allowed"})

    body = event.get("body")
    if not body:
        return _response(400, {"ok": False, "error": "Missing request body"})

    if event.get("isBase64Encoded"):
        try:
            body = base64.b64decode(body).decode("utf-8")
        except Exception:
            return _response(400, {"ok": False, "error": "Invalid base64 body"})

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return _response(400, {"ok": False, "error": "Body must be valid JSON"})

    prompt = payload.get("prompt", "")
    characteristics = payload.get("project_characteristics")
    if characteristics is None:
        characteristics = prompt_to_pdss_input(prompt)
    elif not isinstance(characteristics, dict):
        return _response(400, {"ok": False, "error": "project_characteristics must be an object"})

    missing = [k for k in REQUIRED_KEYS if k not in characteristics]
    if missing:
        if prompt:
            inferred = prompt_to_pdss_input(prompt)
            for k in missing:
                characteristics[k] = inferred.get(k)
            missing = [k for k in REQUIRED_KEYS if k not in characteristics]
    if missing:
        return _response(400, {"ok": False, "error": "Missing required keys", "missing": missing})

    dss = ProjectDSS()
    dss.project_characteristics = characteristics
    dss.analyze_and_recommend()
    plan = advanced_project_plan(prompt, dss.project_characteristics, dss.recommendations)

    return _response(200, {
        "ok": True,
        "prompt": prompt,
        "project_characteristics": dss.project_characteristics,
        "recommendations": dss.recommendations,
        "narrative": plan.get("narrative"),
        "plan": plan.get("plan"),
        "architecture_components": plan.get("architecture_components"),
        "architecture_patterns": plan.get("architecture_patterns"),
        "tech_stack_suggestions": plan.get("tech_stack_suggestions"),
        "quality_strategy": plan.get("quality_strategy"),
        "data_strategy": plan.get("data_strategy"),
        "risk_register": plan.get("risk_register"),
        "success_metrics": plan.get("success_metrics"),
        "project_category_overview": plan.get("project_category_overview"),
        "similar_project_examples": plan.get("similar_project_examples"),
        "market_analogs": plan.get("market_analogs"),
        "industry_context": plan.get("industry_context"),
        "dependency_map": plan.get("dependency_map"),
        "critical_path": plan.get("critical_path"),
        "release_train": plan.get("release_train"),
        "stakeholder_communications": plan.get("stakeholder_communications"),
        "acceptance_criteria": plan.get("acceptance_criteria"),
        "deliverables": plan.get("deliverables"),
        "real_world_considerations": plan.get("real_world_considerations"),
    })
