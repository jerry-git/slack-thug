import logging

from flask import Flask, request, Response, jsonify

from slack_thug.event import event_handler

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/event", methods=["POST"])
def event_endpoint():
    p = request.get_json()
    if p.get("type") == "url_verification":
        return jsonify({"challenge": p["challenge"]})

    event_handler.delay(p)
    return Response(), 200


if __name__ == "__main__":
    logger.info("Running on DEVELOPMENT mode")
    app.run(debug=True)
