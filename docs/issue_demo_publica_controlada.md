# Issue Draft: Prepare controlled public demo with VM, Ollama/Gemma4, and Streamlit

## Context

We want to make EmpathyAI available for testing through a controlled public URL while keeping the current short-term architecture: protected VM + Ollama/Gemma4 + Streamlit, with an ephemeral diary.

This issue covers the next deployment step. The UX package already implemented in the `ux-demo-readiness-streamlit` branch should remain registered separately in `docs/issue_ux_demo_readiness_streamlit.md`.

## Recommended Decision For The Public URL

Publish only as a controlled demo, not as an open demo:

- VM with enough RAM/VRAM for Gemma4.
- Ollama and Streamlit running on the same server or private network.
- HTTPS required.
- Simple authentication or protected link.
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
- Ensure the demo is suitable for limited testing, not open production use.

## Deployment Pending Items

- [ ] Define a VM provider/size compatible with Gemma4.
- [ ] Validate `gemma4:e2b` with enough memory on the server.
- [ ] Configure Ollama on the server and download the model defined in `GEMMA_MODEL`.
- [ ] Configure Streamlit for public hosting behind proxy/HTTPS.
- [ ] Protect access with authentication or password.
- [ ] Ensure the Ollama port is not publicly exposed.
- [ ] Implement an ephemeral diary policy or disable persistence between users.
- [x] Implement frontend inactivity detection for real human interaction.
- [x] Redirect inactive sessions to a Session Expired page.
- [x] Ensure timeout does not depend on Streamlit healthcheck traffic.
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
