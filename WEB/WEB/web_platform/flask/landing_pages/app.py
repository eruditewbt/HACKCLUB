from __future__ import annotations

from flask import Flask


app = Flask(__name__)


@app.get("/")
def index():
    return """
    <h1>WEB Platform</h1>
    <p>Monetizable Python web starter kit.</p>
    <ul>
      <li><a href="/pricing">Pricing</a></li>
      <li><a href="/docs">Docs</a></li>
      <li><a href="/status">Status</a></li>
    </ul>
    """


@app.get("/pricing")
def pricing():
    return """
    <h2>Pricing</h2>
    <p>Free / Pro / Business (wire billing service for real payments).</p>
    """


@app.get("/docs")
def docs():
    return """
    <h2>Docs</h2>
    <p>See OpenAPI: /docs on the FastAPI gateway.</p>
    """


@app.get("/status")
def status():
    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


