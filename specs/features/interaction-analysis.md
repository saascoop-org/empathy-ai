# Feature Spec: Interaction Analysis

## Intent

Help a user transform a described communication mismatch into a possible empathy bridge.

## Input

- Free-text interaction description.
- Selected output language from the UI.
- Optional consent and feedback from the UI.

## Output

The workflow returns:

- anonymized interaction
- detected user language
- processing language
- output language
- context analysis
- double empathy analysis
- perspective translation
- sensory load factors
- safety result
- bridge message
- learning reflection question

## Behavior

1. Detect likely user input language.
2. Keep processing language set to English.
3. Anonymize interaction text.
4. Run the agent pipeline.
5. Generate or fall back to a bridge message.
6. Return structured output.

## Acceptance Criteria

- The result contains all required workflow keys.
- The response includes a bridge message.
- The result includes a learning reflection question.
- Tests cover the full workflow contract.
