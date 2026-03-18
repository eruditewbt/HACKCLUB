from __future__ import annotations

import html
from typing import Any, Dict

from dataanalysis_platform.viz.narrative import analyze_artifact


def _h(s: str) -> str:
    return html.escape(s or "")


def render_report(artifact: Dict[str, Any]) -> str:
    title = artifact.get("title") or "DATAANALYSIS Report"
    profile = artifact.get("profile") or {}
    validation = artifact.get("validation") or {}

    cols = profile.get("columns") or []
    narrative = analyze_artifact(artifact)

    score = validation.get("quality_score") if validation else None
    score_pct = None
    if isinstance(score, (int, float)):
        score_pct = max(0.0, min(100.0, float(score) * 100.0))

    score_display = _h(f"{score_pct:.1f}" if score_pct is not None else "-")

    col_rows = []
    for c in cols:
        col_rows.append(
            "<tr>"
            f"<td>{_h(str(c.get('name')))}</td>"
            f"<td>{_h(str(c.get('type')))}</td>"
            f"<td>{_h(str(c.get('count')))}</td>"
            f"<td>{_h(str(c.get('missing')))}</td>"
            f"<td>{_h(str(c.get('missing_rate')))}</td>"
            f"<td>{_h(str(c.get('distinct_count')))}</td>"
            f"<td>{_h(str(c.get('min')))}</td>"
            f"<td>{_h(str(c.get('max')))}</td>"
            f"<td>{_h(str(c.get('mean')))}</td>"
            "</tr>"
        )

    failures = (validation or {}).get("failures") or []
    fail_rows = []
    for f in failures[:200]:
        fail_rows.append(
            "<tr>"
            f"<td>{_h(str(f.get('row')))}</td>"
            f"<td>{_h(str(f.get('rule')))}</td>"
            f"<td>{_h(str(f.get('message')))}</td>"
            "</tr>"
        )

    ok = (validation or {}).get("failed_checks", 0) == 0 if validation else True
    status = "OK" if ok else "ISSUES"
    status_class = "pill-ok" if ok else "pill-bad"

    generated_at = _h(str(artifact.get("generated_at") or ""))
    source = _h(str((artifact.get("source") or {}).get("path") or ""))
    org_id = _h(str(artifact.get("org_id") or ""))
    dataset_name = _h(str(artifact.get("dataset_name") or ""))

    def bullets(items):
        if not items:
            return "<p class=\"muted\">None</p>"
        return "<ul>" + "".join([f"<li>{_h(i)}</li>" for i in items]) + "</ul>"

    css = """
    :root { --bg:#0b1020; --card:#111a33; --text:#e8ecff; --muted:#a8b3e6; --accent:#7dd3fc; --bad:#fb7185; --ok:#86efac; }
    body { margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; background: radial-gradient(1200px 700px at 20% 10%, #1d2a5f, var(--bg)); color:var(--text); }
    .wrap { max-width: 1100px; margin: 32px auto; padding: 0 18px; }
    h1 { margin: 0 0 10px 0; letter-spacing: .2px; }
    h2 { margin: 0 0 10px 0; }
    .meta { color: var(--muted); margin-bottom: 18px; }
    .grid { display:grid; grid-template-columns: 1fr; gap: 14px; }
    .card { background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)); border: 1px solid rgba(255,255,255,0.10); border-radius: 14px; padding: 14px; }
    .kpis { display:flex; gap: 10px; flex-wrap: wrap; align-items: stretch; }
    .kpi { background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.10); border-radius: 12px; padding: 10px 12px; min-width: 160px; }
    .kpi b { display:block; font-size: 14px; }
    .kpi span { color: var(--muted); }
    .score { font-size: 34px; line-height: 1; color: var(--accent); font-weight: 700; margin-top: 6px; }
    table { width:100%; border-collapse: collapse; overflow:hidden; border-radius: 12px; }
    th, td { padding: 10px 10px; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 13px; }
    th { text-align:left; color: var(--muted); font-weight: 600; }
    .pill-ok { color: var(--ok); }
    .pill-bad { color: var(--bad); }
    code { color: var(--accent); }
    ul { margin: 8px 0 0 18px; }
    li { margin: 6px 0; color: var(--text); }
    .muted { color: var(--muted); }
    """

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_h(title)}</title>
  <style>{css}</style>
</head>
<body>
  <div class="wrap">
    <h1>{_h(title)}</h1>
    <div class="meta">
      Generated: <code>{generated_at}</code>
      | Source: <code>{source}</code>
      | Org: <code>{org_id}</code>
      | Dataset: <code>{dataset_name}</code>
    </div>

    <div class="grid">
      <div class="card">
        <div class="kpis">
          <div class="kpi"><b>Rows</b><span>{_h(str(profile.get('row_count')))}</span></div>
          <div class="kpi"><b>Columns</b><span>{_h(str(len(cols)))}</span></div>
          <div class="kpi"><b>Status</b><span class="{status_class}">{_h(status)}</span></div>
          <div class="kpi"><b>Quality Score</b><div class="score">{score_display}</div><span class="muted">out of 100</span></div>
        </div>
      </div>

      <div class="card">
        <h2>Executive Summary</h2>
        <p>{_h(str(narrative.get('executive_summary') or ''))}</p>
      </div>

      <div class="card">
        <h2>Key Issues</h2>
        {bullets(narrative.get('key_issues') or [])}
      </div>

      <div class="card">
        <h2>Recommendations</h2>
        {bullets(narrative.get('recommendations') or [])}
      </div>

      <div class="card">
        <h2>Profile</h2>
        <table>
          <thead>
            <tr>
              <th>Column</th><th>Type</th><th>Count</th><th>Missing</th><th>Missing Rate</th><th>Distinct</th><th>Min</th><th>Max</th><th>Mean</th>
            </tr>
          </thead>
          <tbody>
            {''.join(col_rows)}
          </tbody>
        </table>
      </div>

      <div class="card">
        <h2>Validation Failures (first 200)</h2>
        <table>
          <thead><tr><th>Row</th><th>Rule</th><th>Message</th></tr></thead>
          <tbody>
            {''.join(fail_rows) if fail_rows else '<tr><td colspan="3" class="pill-ok">No failures</td></tr>'}
          </tbody>
        </table>
      </div>

      <div class="card">
        <h2>Notes</h2>
        {bullets(narrative.get('notes') or [])}
      </div>
    </div>
  </div>
</body>
</html>"""
