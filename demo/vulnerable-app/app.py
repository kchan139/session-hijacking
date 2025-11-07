from flask import Flask, request, render_template, make_response, redirect
import secrets
import datetime

app = Flask(__name__)

# in-memory storage
users = {"alice": "password123", "bob": "qwerty456"}

sessions = {}  # session_id -> username


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # NOTE - VULNERABLE: Session fixation - accept session_id from URL
        fixed_session = request.args.get("session_id")
        response = make_response(render_template("login.html"))
        if fixed_session:
            response.set_cookie("session_id", fixed_session)
        return response

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username in users and users[username] == password:
        # NOTE - VULNERABLE: Reuse existing session_id instead of regenerating
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = secrets.token_hex(8)

        sessions[session_id] = username

        response = make_response(redirect("/dashboard"))
        # NOTE - VULNERABLE: No Secure, HttpOnly, or SameSite flags
        response.set_cookie("session_id", session_id)
        return response

    return render_template("login.html", error="Invalid credentials")


@app.route("/dashboard")
def dashboard():
    session_id = request.cookies.get("session_id")

    if not session_id or session_id not in sessions:
        return redirect("/login")

    username = sessions[session_id]
    display_name = request.args.get("display_name", "")

    return render_template(
        "dashboard.html", username=username, display_name=display_name
    )


@app.route("/search")
def search():
    session_id = request.cookies.get("session_id")

    if not session_id or session_id not in sessions:
        return redirect("/login")

    # NOTE - VULNERABLE: XSS via search query
    query = request.args.get("q", "")
    return render_template("search.html", query=query)


@app.route("/profile", methods=["POST"])
def profile():
    session_id = request.cookies.get("session_id")

    if not session_id or session_id not in sessions:
        return redirect("/login")

    # NOTE - VULNERABLE: XSS via display name
    display_name = request.form.get("display_name", "")
    return redirect(f"/dashboard?display_name={display_name}")


@app.route("/logout")
def logout():
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]

    response = make_response(redirect("/login"))
    response.set_cookie("session_id", "", expires=0)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
