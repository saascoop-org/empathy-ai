# Feature Spec: Safety Boundaries

## Intent

Keep outputs supportive, non-diagnostic, and non-judgmental.

## Prohibited Framing

The system must not:

- diagnose a person
- decide who is right or wrong
- assign blame
- normalize or pathologize behavior
- replace clinical, legal, HR, or specialized educational advice

## Required Framing

The system should:

- describe possible interpretations
- suggest clarification
- support mutual understanding
- identify possible mismatch types
- avoid authority over intent

## Acceptance Criteria

- Safety agent flags pathologizing or blame language.
- Safety agent flags diagnosis, clinical labeling, normalization, harassment or abuse, emotional risk, and out-of-scope advice.
- Response Composer prompt instructs the LLM to avoid diagnosis, blame, and unilateral correction.
- UI displays the advisory notice.

## Policy Source

The active policy is `../safety-policy-v1.md` and runtime rules live in `empathy_engine/safety/policy.py`.
