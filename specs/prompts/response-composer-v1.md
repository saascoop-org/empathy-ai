# Prompt Spec: Response Composer v1

## Owner

`empathy_engine/agents/response_composer.py`

## Purpose

Compose a concise empathy bridge from structured workflow analysis.

## Processing Language

English.

## Presentation Language

The final bridge must be written in the selected output language:

- English
- Brazilian Portuguese
- Spanish

## Inputs

- double empathy analysis
- perspective translation
- sensory load factors
- safety result
- detected user language
- configured processing language
- selected output language

## Safety Constraints

The model must not:

- diagnose a person
- decide who is right or wrong
- assign blame
- tell one person to change as if they are the only problem
- normalize or pathologize behavior

## Output Contract

Return one practical bridge message in plain language.

## Current Prompt Shape

```text
Compose a concise, non-diagnostic empathy bridge from this analysis.
Do not decide who is right or wrong.
Do not tell one person to change their communication style as if it is the only problem.
Return a neutral, practical bridge that supports mutual clarification in plain language.
Process the analysis in English because the configured processing language is {processing_language}.
Translate only the final bridge for presentation, and write that final bridge in {output_language_name}.

Analysis:
{payload}
```

## Acceptance Criteria

- The bridge is practical and concise.
- The bridge is not diagnostic.
- The bridge does not assign blame.
- The final bridge is in the selected output language.
- If LLM generation fails, the deterministic fallback is used.
