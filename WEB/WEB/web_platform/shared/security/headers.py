from __future__ import annotations


def security_headers() -> dict[str, str]:
    # Minimal sane defaults. Tune per app and CSP needs.
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }


