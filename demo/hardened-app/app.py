from flask import Flask, request, render_template_string, make_response, redirect, escape
import secrets
import datetime

app = Flask(__name__)

# In-memory storage
users = {"alice": "password123", "bob": "qwerty456"}
sessions = {}  # session_id -> {"username": str, "ip": str, "user_agent": str, "created": datetime}


def get_client_fingerprint():
    """Get client IP and User-Agent for session binding."""
    return {
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "")
    }


def validate_session(session_id):
    """Validate session exists and matches client fingerprint."""
    if not session_id or session_id not in sessions:
        return None
    
    session = sessions[session_id]
    fingerprint = get_client_fingerprint()
    
    # Check IP and User-Agent match
    if session["ip"] != fingerprint["ip"] or session["user_agent"] != fingerprint["user_agent"]:
        # Session hijacking detected - invalidate session
        del sessions[session_id]
        return None
    
    return session["username"]


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # FIXED: Ignore any session_id from URL parameters
        return render_template_string(LOGIN_TEMPLATE)

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username in users and users[username] == password:
        # FIXED: Always generate new session ID on login (prevent fixation)
        session_id = secrets.token_urlsafe(32)
        
        # Store session with fingerprint
        fingerprint = get_client_fingerprint()
        sessions[session_id] = {
            "username": username,
            "ip": fingerprint["ip"],
            "user_agent": fingerprint["user_agent"],
            "created": datetime.datetime.now()
        }

        response = make_response(redirect("/dashboard"))
        # FIXED: Set secure cookie flags
        response.set_cookie(
            "session_id",
            session_id,
            httponly=True,    # Prevent JavaScript access
            secure=True,       # Only send over HTTPS (use False for local HTTP testing)
            samesite="Strict", # Prevent CSRF
            max_age=1800       # 30 minute timeout
        )
        return response

    return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")


@app.route("/dashboard")
def dashboard():
    session_id = request.cookies.get("session_id")
    username = validate_session(session_id)
    
    if not username:
        return redirect("/login")

    # FIXED: Escape display_name to prevent XSS
    display_name = escape(request.args.get("display_name", ""))

    return render_template_string(
        DASHBOARD_TEMPLATE,
        username=username,
        display_name=display_name
    )


@app.route("/search")
def search():
    session_id = request.cookies.get("session_id")
    username = validate_session(session_id)
    
    if not username:
        return redirect("/login")

    # FIXED: Escape query to prevent XSS
    query = escape(request.args.get("q", ""))
    
    return render_template_string(SEARCH_TEMPLATE, query=query)


@app.route("/profile", methods=["POST"])
def profile():
    session_id = request.cookies.get("session_id")
    username = validate_session(session_id)
    
    if not username:
        return redirect("/login")

    # FIXED: Escape and validate display_name
    display_name = escape(request.form.get("display_name", ""))
    
    return redirect(f"/dashboard?display_name={display_name}")


@app.route("/logout")
def logout():
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]

    response = make_response(redirect("/login"))
    response.set_cookie("session_id", "", expires=0)
    return response


# Templates (inline to avoid file management)
LOGIN_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>Login - Hardened App</title>
    </head>
    <body>
        <h1>Login (Hardened)</h1>
        <form method="POST" action="/login">
            <label>Username: <input type="text" name="username" required /></label><br />
            <label>Password: <input type="password" name="password" required /></label><br />
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <p style="color: red">{{ error }}</p>
        {% endif %}
    </body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>Dashboard - Hardened App</title>
    </head>
    <body>
        <h1>Welcome, {{ username }}!</h1>
        <p>Your session is active and secured.</p>

        <h2>Search</h2>
        <form method="GET" action="/search">
            <input type="text" name="q" placeholder="Search..." />
            <button type="submit">Search</button>
        </form>

        <h2>Profile</h2>
        <form method="POST" action="/profile">
            <label>Display Name: <input type="text" name="display_name" /></label><br />
            <button type="submit">Update</button>
        </form>

        {% if display_name %}
        <p>Display name: {{ display_name }}</p>
        {% endif %}

        <br /><a href="/logout">Logout</a>
    </body>
</html>
"""

SEARCH_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>Search Results - Hardened App</title>
    </head>
    <body>
        <h1>Search Results</h1>
        <p>You searched for: {{ query }}</p>
        <p>No results found.</p>
        <br /><a href="/dashboard">Back to Dashboard</a>
    </body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
