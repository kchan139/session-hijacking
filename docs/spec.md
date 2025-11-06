# Assignment Specification — Session Hijacking in Web Environments

**Course:** Cryptography and Network Security  
**Assignment Title:** Research and Analysis on Session Hijacking Attacks  
**Team size:** 4 students  
**Duration:** 4 weeks  
**Total points:** 100

## 1. Objective

This assignment gives student teams practical and analytical exposure to session hijacking in web environments. Teams will research how session hijacking works, how attackers perform it, how to detect and mitigate it, and—if feasible—produce a safe, controlled demonstration or simulation that illustrates attack and defense techniques.

By the end of the project students should be able to:

- Explain session concepts (cookies, session identifiers, tokens) and why sessions are vulnerable.
- Describe session hijacking techniques and attacker goals (impersonation, privilege escalation, data theft).
- Evaluate detection and prevention strategies for web applications and network layers.
- Build a safe lab demonstration or simulation in an isolated environment (optional but encouraged).
- Demonstrate ethical and legal conduct while researching vulnerabilities.

## 2. Required Project Components

Each group must complete the following parts and submit the final package at the end of week 4.

### Part A — Background & Overview (Weeks 1–2)

- Define a web session and common session management mechanisms:
  - Cookies (secure, HttpOnly, SameSite)
  - Session identifiers and tokens (JWT, opaque tokens)
  - Session lifecycle (creation, renewal, expiration, logout)
- Define session hijacking and classify attack types:
  - Session fixation
  - Cookie theft (XSS, network sniffing on HTTP)
  - Session replay and token theft (man-in-the-middle)
  - CSRF that leads to session misuse
  - Exploiting poor session management (predictable IDs, long-lived sessions)
- Discuss attacker goals and likely impacts (account takeover, data leakage, financial loss).

**Deliverable:** 2–3 page literature-backed overview with references (IEEE or APA).

### Part B — Attack Methodologies (Week 2)

- Give technical, step-by-step descriptions of how common session hijacking attacks are performed:
  - How XSS steals cookies (document.cookie, exfiltration techniques)
  - How insecure transport (HTTP) enables sniffing and replay of session tokens
  - Session fixation attack flow (forcing a victim to use attacker-chosen session id)
  - Token theft via local storage misuse and cross-site leaks
- Describe attacker tools and measures used for proof-of-concept (e.g., Burp Suite, Wireshark, browser dev tools) — for documentation and lab use only.
- Explain prerequisites and limitations (HTTPS vs. HTTP, SameSite/Secure flags, modern browsers).

**Deliverable:** 3–4 page technical write-up with diagrams/sequence charts.

### Part C — Detection & Prevention (Week 2–3)

- Review detection techniques:
  - Anomaly detection on session usage (IP/UA changes, geo changes)
  - Monitoring for multiple concurrent uses of the same session id
  - Logging and alerting on suspicious session activity
- Review prevention & hardening techniques:
  - Always use HTTPS/TLS; set Secure and HttpOnly cookie flags
  - Use short session lifetimes and rotate session identifiers on privilege change or re-authentication
  - Implement token-binding or use signed tokens with server-side validation (avoid storing sensitive data solely in client tokens)
  - Use SameSite cookie attribute and CSRF tokens; avoid localStorage for sensitive tokens
  - Employ multi-factor authentication (MFA) and risk-based authentication checks
  - Backend measures: server-side session invalidation, IP/UA binding, rate-limiting, device fingerprinting
- Produce a recommended defense checklist for web developers and network administrators.

**Deliverable:** 3–4 page section with diagrams, configuration examples, and a prioritized action plan.

### Part D — Practical Demonstration (Optional but strongly encouraged) (Week 3–4)

- Build a controlled, isolated lab demo showing one or more of the following in a safe environment (VMs, private network, or localhost):
  - A harmless session fixation proof-of-concept between two local VMs.
  - Demonstration of cookie theft via a simple XSS payload on a lab app you control (only in isolated lab).
  - Detection demonstration: server logs trigger when the same session id is used from two different IPs; or an IDS signature that flags session-reuse.
- Provide full documentation: lab topology, VM images or scripts, code snippets, screenshots, and a mitigation demonstration showing how a fix prevents the hijack.
- Produce a short video (5–7 minutes) showing the demo and safety measures used.

**Safety requirement:** Do NOT target live systems, public websites, campus production networks, or third-party services. Include a clear attestation describing the isolated environment and safeguards taken.

**Deliverable:** Demo package (ZIP) + video + README with reproduction steps.

## 3. Final Deliverables (Due at end of Week 4)

Submit one consolidated package per group containing:

| Deliverable | Description | Weight |
|-------------|-------------|--------|
| Final Report | Complete report (8–10 pages recommended) covering Parts A–C and optional Part D. Include references, diagrams, and conclusions. | 60% |
| Presentation Slides | 10–12 slides summarizing the project for a 10–15 minute in-class presentation. | 20% |
| Demo / Simulation | Working demo or simulation and video (optional, up to 10 bonus points). | 0–10 bonus |
| Team Contribution Sheet | Roles and contributions for each team member; time logs if available. | 10% |

**Submission method:** Upload via [LMS name / email] by [Exact due date — 4 weeks from assignment release]. Late penalties: 10% per day up to 3 days; submissions after 3 days will not be accepted except for documented exceptional reasons.

## 4. Grading Rubric

- Research quality & technical accuracy — 30 points
- Depth of attack analysis (correctness and clarity) — 20 points
- Detection & mitigation proposals (practicality, detail) — 20 points
- Practical demo & reproducibility (if submitted) — 10 points (+10 bonus)
- Clarity, organization, writing quality — 10 points
- Team contribution and adherence to ethics — 10 points

**Total:** 100 points (plus up to 10 bonus for demo)

## 5. Schedule & Milestones

- **Week 0** (assignment release): Form groups and share contact details.
- **End Week 1:** Submit a one-page project outline and literature list.
- **End Week 2:** Submit drafts for Parts A & B (background + attack methods).
- **End Week 3:** Submit draft for Part C (detection & prevention) and demo plan.
- **End Week 4:** Final report, slides, demo (if any), and team contribution sheet.

## 6. Safety, Legal & Ethical Rules (MANDATORY)

- All experiments must be performed only in isolated lab environments fully controlled by the students (local VMs, private VLANs, or sandboxed containers).
- Do not target or interact with any real, public, or third-party systems — including campus production systems, cloud services you do not own, or other students' devices without explicit written permission.
- Document exactly what isolation measures were taken (snapshots, network isolation, firewall rules).
- Tools and scripts used must be clearly documented; do not include or distribute harmful payloads.
- Violations of these rules will result in project failure and potential academic disciplinary action.

## 7. Recommended References & Resources

- Course textbook chapters on web security and authentication (William Stallings).
- OWASP resources (Session Management Cheat Sheet, Top Ten).
- Browser documentation for cookie attributes (Secure, HttpOnly, SameSite).
- Tools and frameworks for safe lab work: Docker, VirtualBox, local test web apps (DVWA, WebGoat) — use only in isolated labs.
- Academic papers and security blogs for case studies and detection strategies.

## 8. Submission Guidelines

- Submit all materials via LMS by **December 7, 2025, at 23:59:59**.
- Late submissions will incur a penalty of 10% per day (up to 3 days).
- Use the following naming convention for files: `CC0X_GroupX_SessionHijacking_Assignment.zip`
