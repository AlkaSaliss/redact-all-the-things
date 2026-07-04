import json
import os


def _headers(event):
    origin = (event.get("headers") or {}).get("origin")
    allowed = {
        value.strip()
        for value in os.environ.get("FRONTEND_ALLOWED_ORIGINS", "").split(",")
        if value.strip()
    }
    headers = {"content-type": "application/json"}
    if origin in allowed:
        headers.update(
            {
                "access-control-allow-origin": origin,
                "access-control-allow-methods": "GET,OPTIONS,POST,PUT",
                "access-control-allow-headers": "authorization,content-type",
                "access-control-expose-headers": "etag",
                "access-control-max-age": "300",
                "vary": "origin",
            }
        )
    return headers


def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    path = event.get("rawPath")
    if method == "OPTIONS":
        return {"statusCode": 204, "headers": _headers(event), "body": ""}
    if method == "GET" and path == "/jobs":
        return {
            "statusCode": 200,
            "headers": _headers(event),
            "body": json.dumps([]),
        }
    return {
        "statusCode": 200,
        "headers": _headers(event),
        "body": json.dumps({"status": "ok", "service": "control-plane-stub"}),
    }
