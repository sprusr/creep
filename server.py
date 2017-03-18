from flask import Flask, request, json, render_template
from facebook import GraphAPI
import os

FB_APP_ID = os.environ.get("FB_APP_ID")
FB_APP_NAME = os.environ.get("FB_APP_NAME")
FB_APP_SECRET = os.environ.get("FB_APP_SECRET")

app = Flask(__name__)

@app.route("/auth", methods=["GET"])
def auth_post():
    return "HELP ME " + request.args.get("id")

@app.route("/webhook", methods=["GET"])
def webhook_get():
    return request.args.get("hub.challenge")

@app.route("/webhook", methods=["POST"])
def webhook_post():
    data = request.get_json()
    print(json.dumps(data))
    return "todo"

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
