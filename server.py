from flask import Flask, request
app = Flask(__name__)

@app.route("/webhook", methods=['GET'])
def webhook_get():
    return request.args.get("hub.challenge", "")

def webhook_post():
    # do something
    return "todo"

if __name__ == "__main__":
    app.run()
