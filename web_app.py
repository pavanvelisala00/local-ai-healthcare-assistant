"""Flask web interface for the local healthcare assistant."""

from flask import Flask, jsonify, render_template, request

from guardrails import check_input, check_output
from model_loader import generate_response

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = payload.get("message", "")

    allowed, warning = check_input(question)
    if not allowed:
        return jsonify({"answer": warning, "blocked": True}), 400

    try:
        answer = generate_response(question)
    except (RuntimeError, OSError, ValueError) as exc:
        app.logger.exception("Model inference failed")
        return jsonify({"answer": str(exc), "blocked": True}), 503

    safe, output_warning = check_output(answer)
    if not safe:
        return jsonify({"answer": output_warning, "blocked": True}), 200

    return jsonify({"answer": answer, "blocked": False})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
