# Acceptance Matrix

These scenarios connect product behavior to tests and smoke checks.

| Scenario | Spec Area | Automated Check |
| --- | --- | --- |
| Direct communication perceived as rude | `features/interaction-analysis.md` | `tests/test_acceptance.py` |
| Misunderstanding under noise or time pressure | `features/interaction-analysis.md` | `tests/test_acceptance.py` |
| Sensitive data is anonymized | `features/privacy-consent-storage.md` | `tests/test_acceptance.py`, `tests/test_privacy.py` |
| PT-BR input is detected and can produce PT-BR output | `features/multilingual-output.md` | `tests/test_i18n.py`, `tests/test_acceptance.py` |
| Spanish input is detected and can produce Spanish output | `features/multilingual-output.md` | `tests/test_i18n.py`, `tests/test_acceptance.py` |
| LLM unavailable or timeout falls back safely | `features/local-llm-runtime.md` | `tests/test_llm_runtime.py` |
| Wrong-language LLM output falls back safely | `features/multilingual-output.md` | `tests/test_llm_runtime.py` |
| Consented storage writes local anonymized record | `features/privacy-consent-storage.md` | `tests/test_storage.py`, `tests/test_use_cases.py` |
| No-consent analysis does not create a local database | `features/privacy-consent-storage.md` | `tests/test_use_cases.py` |
| Streamlit UI responds locally | operational readiness | `python scripts/check_streamlit.py` |

## Required Local Validation

```bash
python -m pytest
python scripts/smoke_test.py
python scripts/check_streamlit.py
```
