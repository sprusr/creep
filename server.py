from flask import Flask, request, json, render_template
from facebook import GraphAPI
from esendexer import Esendex
from threading import Thread
import os, random, datetime, time

# These need to be set as env vars
FB_APP_ID = os.environ.get("FB_APP_ID")
FB_APP_NAME = os.environ.get("FB_APP_NAME")
FB_APP_SECRET = os.environ.get("FB_APP_SECRET")

app = Flask(__name__)
esendex = Esendex(os.environ.get("ESENDEX_USERNAME"), os.environ.get("ESENDEX_PASSWORD"), os.environ.get("ESENDEX_ACCOUNT_REF"))
esendex.from_string("Creep")

def invite_pressure(token, mobile):
    graph = GraphAPI(token)
    events = graph.get_object("me/events?fields=rsvp_status,name,attending,start_time")
    random.shuffle(events["data"])
    for event in events["data"]:
        if event["rsvp_status"] == "attending" and datetime.datetime.strptime(event["start_time"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None) > datetime.datetime.now():
            found = False
            while not found:
                friend = random.choice(graph.get_object("me/taggable_friends")["data"])
                if not any(friend["name"] in person["name"] for person in event["attending"]["data"]):
                    found = True
                    esendex.to(mobile).message("Nice that you're going to " + event["name"] + ", but why haven't you invited " + friend["name"] + "? Have you fallen out?").send()
            break

def devices(token, mobile):
    graph = GraphAPI(token)
    devices = graph.get_object("me?fields=devices")["devices"]
    for device in devices:
        print(device["hardware"])
        if device["hardware"]:
            esendex.to(mobile).message("Pretty cool that you own a " + device["hardware"] + ". Do you still use it much?").send()
            break

functions = [invite_pressure, devices]

class UpdateThread(Thread):
    def __init__(self, token, mobile):
        self.stopped = False
        self.token = token
        self.mobile = mobile
        Thread.__init__(self)
    def run(self):
        while not self.stopped:
            time.sleep(30)
            random.choice(functions)(self.token, self.mobile)

@app.route("/auth", methods=["POST"])
def auth_post():
    graph = GraphAPI(request.form.get("token"))
    profile = graph.get_object("me")
    esendex.to(request.form.get("mobile")).message("Hello, " + profile["name"] + ". I know a lot about you...").send()
    thread = UpdateThread(request.form.get("token"), request.form.get("mobile"))
    thread.start()
    return "HELP ME " + request.form.get("mobile") + " " + request.form.get("token")

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
    return render_template("index.html", app_id=FB_APP_ID)

if __name__ == "__main__":
    app.run(debug=True)


