from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.debug(level = logging.DEBUG)

@app.route("/", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }

    req = request.json
    if req["session"]["new"]:
        response["session"]["text"] = "Здарова, заебал!"
    else:
        if response["request"]["original_utterance"].lower() in ["привет"]:
            response["session"]["text"] = "Привет-привет!"
        elif response["request"]["original_utterance"].lower() in ["пока"]:
            response["session"]["text"] = "Пока!"
    
    return json.dumps(response)
