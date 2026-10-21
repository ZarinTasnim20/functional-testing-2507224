"""Flask frontend + JSON API that runs the target.py functions."""

import ast
import inspect
import os

from flask import Flask, jsonify, render_template, request

import target

app = Flask(__name__)

COMMIT_SHA = os.environ.get("RENDER_GIT_COMMIT") or os.environ.get("COMMIT_SHA", "local")

FUNCTIONS = {
    name: fn
    for name, fn in inspect.getmembers(target, inspect.isfunction)
    if fn.__module__ == "target"
}


def parse_arg(raw):
    """Turn a text box value into a Python value: 18, 2.5, None, [1, 2], {1, 2}, 'text'."""
    raw = raw.strip()
    if raw == "":
        return ""
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return raw  # treat as a plain string


def signature_of(fn):
    return [p.name for p in inspect.signature(fn).parameters.values()]


@app.get("/")
def index():
    funcs = [
        {"name": n, "params": signature_of(f), "doc": (inspect.getcomments(f) or "").strip("# \n")}
        for n, f in FUNCTIONS.items()
    ]
    return render_template("index.html", funcs=funcs, sha=COMMIT_SHA)


@app.get("/health")
def health():
    return jsonify(status="ok", sha=COMMIT_SHA)


@app.post("/api/run/<name>")
def run(name):
    fn = FUNCTIONS.get(name)
    if fn is None:
        return jsonify(ok=False, error="UnknownFunction", message=name), 404
    raw_args = (request.get_json(silent=True) or {}).get("args", [])
    args = [parse_arg(a) if isinstance(a, str) else a for a in raw_args]
    try:
        result = fn(*args)
    except Exception as exc:  # noqa: BLE001 - show any error to the user
        return jsonify(ok=False, error=type(exc).__name__, message=str(exc))
    if isinstance(result, set):
        shown = repr(result) if result else "set()"
    else:
        shown = repr(result)
    return jsonify(ok=True, result=shown, type=type(result).__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
