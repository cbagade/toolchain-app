"""
IBM OnePipeline DevSecOps V11 — Production Flask Microservice
Exposes a root route and a dedicated /health probe endpoint required by
IBM Continuous Delivery automated gating checks.
"""

import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Root route — confirms the service is reachable."""
    return (
        jsonify(
            {
                "status": "ok",
                "message": "IBM OnePipeline microservice is running",
            }
        ),
        200,
    )


@app.route("/health", methods=["GET"])
def health():
    """
    Health-check endpoint consumed by IBM Continuous Delivery automated
    gating probes. Must return HTTP 200 to allow pipeline stage promotion.
    """
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
