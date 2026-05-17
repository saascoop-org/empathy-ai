# Issue Draft: Prepare controlled public demo with VM, Ollama/Gemma4, and Streamlit

## Context

We want to make EmpathyAI available for testing through a controlled public URL while keeping the current short-term architecture: protected VM + Ollama/Gemma4 + Streamlit, with an ephemeral diary.

This issue covers the next deployment step. The UX package already implemented in the `ux-demo-readiness-streamlit` branch should remain registered separately in `docs/issue_ux_demo_readiness_streamlit.md`.

## Recommended Decision For The Public URL

Publish only as a controlled demo, not as an open demo:

- VM with enough RAM/VRAM for Gemma4.
- Ollama and Streamlit running on the same server or private network.
- HTTPS required.
- Short-lived signed token access for launched sessions.
- Basic Auth kept only as a manual testing fallback.
- Ollama port must not be publicly exposed.
- Ephemeral diary per session, or persistence disabled, to avoid mixing data between testers.
- Concurrency limit/rate limiting.
- Data cleanup routine after tests.

## Controlled Public Demo Scope

- Expose the Streamlit interface through a protected public URL.
- Run the Gemma4 model through Ollama on the demo server.
- Keep the UX experience implemented in the `ux-demo-readiness-streamlit` branch.
- Use ephemeral persistence for the mutual learning diary.
- Close inactive browser sessions after 3 minutes of no human interaction.
- Redirect expired users to a friendly session-expired page with sustainability messaging.
- Launch the VM-backed demo from the GitHub Pages landing page through the Cloud Run launcher.
- Redirect users automatically to the demo URL returned by the launcher API.
- Ensure the demo is suitable for limited testing, not open production use.

## Deployment Pending Items

- [ ] Define a VM provider/size compatible with Gemma4.
- [ ] Validate `gemma4:e2b` with enough memory on the server.
- [ ] Configure Ollama on the server and download the model defined in `GEMMA_MODEL`.
- [ ] Configure Streamlit for public hosting behind proxy/HTTPS.
- [ ] Protect access with signed demo tokens.
- [ ] Ensure the Ollama port is not publicly exposed.
- [ ] Implement an ephemeral diary policy or disable persistence between users.
- [x] Implement frontend inactivity detection for real human interaction.
- [x] Redirect inactive sessions to a Session Expired page.
- [x] Ensure timeout does not depend on Streamlit healthcheck traffic.
- [x] Add landing-page launch flow for the Cloud Run launcher endpoint.
- [x] Add progressive launch messages, spinner, disabled CTA state, and graceful error state.
- [x] Redirect automatically to the launcher-provided demo URL.
- [ ] Configure the Cloud Run launcher CORS response for the GitHub Pages origin.
- [x] Support launcher-provided `auth_url` containing a short-lived signed `demo_token`.
- [x] Remove browser-side support for username/password forwarding.
- [x] Add reusable HMAC demo token generation and validation helpers.
- [x] Add optional Streamlit validation through `DEMO_TOKEN_SECRET`.
- [ ] Confirm that no raw data is persisted.
- [ ] Define automatic cleanup for `data/interactions.sqlite3` or temporary storage.
- [ ] Document demo start/stop operations.
- [ ] Run the validation checklist before releasing the URL.

## Validation Checklist Before Releasing The URL

- [ ] `python -m pytest`
- [ ] `python scripts/smoke_test.py`
- [ ] `python scripts/check_ux_accessibility.py`
- [ ] `python scripts/check_streamlit.py`
- [ ] Manual PT-BR language test.
- [ ] Manual ephemeral diary test.
- [ ] Manual minimal concurrency test.
- [ ] Manual HTTPS access test.
- [ ] Manual Ollama port blocking test.
- [ ] Manual inactivity timeout test in the public VM environment.
- [ ] Manual Cloud Run launcher test.
- [ ] Manual dynamic redirect test with current VM external IP.
- [ ] Confirm `Access-Control-Allow-Origin: https://hackathonbrteam.github.io` is present on `/start-demo`.

## Current Browser Blocker

The Cloud Run launcher currently responds successfully to `/start-demo`, but the browser blocks the GitHub Pages request because the response does not include an `Access-Control-Allow-Origin` header for `https://hackathonbrteam.github.io`.

Required launcher response headers:

```http
Access-Control-Allow-Origin: https://hackathonbrteam.github.io
Vary: Origin
```

The endpoint should keep returning JSON with the current VM URL, for example:

```json
{
  "message": "Demo VM is ready.",
  "status": "running",
  "url": "http://<current-vm-ip>"
}
```

## Token-Based Access Contract

Do not hardcode demo credentials in the GitHub Pages landing page. Do not return username/password from Cloud Run. Do not use `user:password@host` URLs.

The Cloud Run launcher should start the VM, create a short-lived signed token, and return:

```json
{
  "status": "running",
  "url": "https://<current-vm-host>",
  "auth_url": "https://<current-vm-host>/?demo_token=<signed-token>",
  "expires_in": 300
}
```

Token requirements:

- Expires after 5 minutes.
- Includes issued timestamp (`iat`).
- Includes expiration timestamp (`exp`).
- Includes a random nonce.
- Is signed with HMAC-SHA256 using a server-side secret.
- Never exposes the signing secret to the frontend.

The landing page only redirects to `auth_url` or appends a returned `demo_token` to `url`. It does not handle or store Basic Auth credentials.

The Streamlit app can validate tokens directly when `DEMO_TOKEN_SECRET` is configured. Nginx may also validate the token before proxying traffic, using the same token contract. Basic Auth should remain available only for manual operator testing.

## Known Risks

- Streamlit is still not the ideal front-end for public multi-user testing.
- Local SQLite requires isolation or ephemeral behavior for multiple testers.
- Gemma4 may have high latency and queueing under concurrent use.
- The current anonymization is a demo baseline, not a production guarantee.
- Audio requires HTTPS and still does not have automatic transcription in this version.

## How To Create This Issue On GitHub

After re-authenticating the GitHub CLI:

```powershell
gh auth login -h github.com
gh issue create --repo HackathonBrTeam/Empathy-Interactional-Expertise --title "Prepare controlled public demo with VM, Ollama/Gemma4, and Streamlit" --body-file docs/issue_demo_publica_controlada.md
```
