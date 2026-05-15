# Demo Go/No-Go

## Responsible Operator

- Name: Demo presenter / local machine operator.
- Role: Start the local app, confirm Ollama status, run smoke tests, and stop the app after use.

## Acceptance Criteria For Demo

- Streamlit opens locally.
- The interface calls `EmpathyWorkflow`.
- User input is anonymized before processing and persistence.
- No interaction is stored unless the consent checkbox is selected.
- If consent is selected, only anonymized content is stored in SQLite.
- The response is framed as possible interpretation, not diagnosis or blame.
- The app remains usable when Ollama cannot run the configured model.
- `python -m pytest` passes before the demo.
- `python scripts/smoke_test.py` passes before the demo.

## Smoke Test Scenarios

1. Direct communication perceived as rude.
2. Misunderstanding caused by time pressure or sensory load.
3. Input containing fake e-mail, phone, CPF-like identifier, and address.

## Rollback Plan

1. Stop the Streamlit process.
2. Delete local demo data if needed:

```powershell
Remove-Item data/interactions.sqlite3
```

3. Restore `.env` from `.env.example` if configuration was changed.
4. Restart Streamlit only after tests pass again.

## Current No-Go Conditions

- `gemma4:e2b` remains No-Go on the current machine because available memory is below the model requirement.
- The local demo is Go with `gemma3:1b`, which has been downloaded and validated through Ollama.
- Production use is No-Go until anonymization, consent retention, audit logging, and broader safety validation are expanded.
