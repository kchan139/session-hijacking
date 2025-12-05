# Cryptography and Network Security

Session Fixation and Cross-Site Scripting (XSS) Demo

## Prerequisites
- Docker & Docker compose
- Web browser

## Setup

```bash
cd demo
cp .env.example .env
docker compose up -d
```

Access:
- Vulnerable app: [http://localhost:5001](http://localhost:5001)
- Hardened app: [http://localhost:5002](http://localhost:5002)
- Attacker page: [http://localhost:8080](http://localhost:8080)

## Use Real Hostnames (Optional)

For a more *realistic* experience (lol), add this line to your hosts file:
```
127.0.0.1 vuln-app hard-app attacker-app
```

- **Linux/Mac** (`/etc/hosts`):
- **Windows** (`C:\Windows\System32\drivers\etc\hosts`):

Then update `demo/.env`:
```
VULN_APP_URL=http://vuln-app:5001
HARDENED_APP_URL=http://hard-app:5002
ATTACKER_APP_URL=http://attacker-app:8080
```

Access:
- Vulnerable app: [http://vuln-app:5001](http://vuln-app:5001)
- Hardened app: [http://hard-app:5002](http://hard-app:5002)
- Attacker page: [http://attacker-app:8080](http://attacker-app:8080)

## Attacks Demonstrated
See [docs/walkthrough.md](docs/walkthrough.md) for detailed steps.

### 1. Session Fixation
Visit attacker page and click the altered login link.

This forces a known session ID before login.

### 2. XSS Cookie Theft
1. Log in to vulnerable app (alice/password123)
2. Visit attacker page
3. Click the login link with malicious payload
4. Check attacker logs: `docker logs attacker-app`

## Vulnerabilities

**vulnerable-app:**
- Accepts session_id from URL (fixation)
- No HttpOnly/Secure cookie flags
- XSS in display_name and search
- No session regeneration on login

**hardened-app:**
- Ignores session_id from URL
- Secure cookie flags (HttpOnly, Secure, SameSite)
- XSS protection via input escaping
- Session regeneration on login
- Session fingerprinting (IP + User-Agent)
- 30-minute session timeout

## Test Accounts

| Username | Password |
| :--- | :--- |
| **alice** | `password123` |
| **bob** | `qwerty456` |

## Cleanup

```bash
docker compose down -v
```

## Safety

All containers run isolated on local bridge network. No external targets.
