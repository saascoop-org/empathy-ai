# Feature Spec: Multilingual Interface And Output

## Intent

Allow users to operate the interface in English, Brazilian Portuguese, or Spanish while preserving English as the processing language.

## Supported Languages

- `en`
- `pt-BR`
- `es`

## Rules

- UI labels must be localized to the selected language.
- UI translations must live in per-language locale files.
- Locale files must maintain coverage with English keys.
- Missing locale keys must fall back to English.
- Processing language must remain `en`.
- The workflow must detect likely user input language.
- If detection fails, user language must default to `en`.
- User-facing output must be presented in the selected UI language.
- LLM prompts must instruct the model to process in English and output the final bridge in the selected language.
- LLM output must be checked against the selected output language before display.
- If LLM output appears to be in the wrong language, the localized deterministic fallback must be used.

## Acceptance Criteria

- PT-BR input is detected as `pt-BR`.
- Spanish input is detected as `es`.
- English input is detected as `en`.
- Unknown input defaults to `en`.
- Workflow result keeps `processing_language` as `en`.
- Workflow result records selected `output_language`.
- Display output is localized for deterministic fields.
- Translation coverage validation returns no missing keys.
- Wrong-language LLM output falls back to localized deterministic output.

## Implementation

- Locale files: `empathy_engine/i18n/locales/`.
- Translation orchestration: `empathy_engine/i18n/language.py`.
- Display localization: `empathy_engine/presentation/result_presenter.py`.
- LLM output language validation: `ResponseComposerAgent`.
