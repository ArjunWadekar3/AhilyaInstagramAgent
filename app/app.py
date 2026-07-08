from flask import Flask, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


# ----------------------------------------
# Health Check
# ----------------------------------------
@app.route("/", methods=["GET"])
def home():
    return {
        "status": "running",
        "service": "Instagram Customer Agent"
    }


# ----------------------------------------
# Meta Webhook Verification
# ----------------------------------------
@app.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook Verified")
        return challenge, 200

    return "Verification failed", 403


# ----------------------------------------
# Receive Instagram Messages
# ----------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    print("\nReceived Event:\n")
    print(data)

    try:

        requests.post(
            N8N_WEBHOOK_URL,
            json=data,
            timeout=10
        )

        return "EVENT_RECEIVED", 200

    except Exception as e:

        print(e)

        return "Forwarding Failed", 500


# ----------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )