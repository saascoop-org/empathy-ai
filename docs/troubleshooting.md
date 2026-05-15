# Troubleshooting

## Streamlit port is already in use

Run Streamlit on another port:

```bash
streamlit run app/streamlit_app.py --server.port 8502
```

## Ollama is not running

Start Ollama, then confirm it responds:

```bash
ollama list
```

If `ollama list` fails, check whether the Ollama desktop app or service is running.

## Configured model is missing

Check the configured model in `.env`:

```bash
GEMMA_MODEL=gemma3:1b
```

Then download it:

```bash
ollama pull gemma3:1b
```

For the higher-memory Gemma 4 target, use:

```bash
GEMMA_MODEL=gemma4:e2b
ollama pull gemma4:e2b
```

## Model is installed but cannot run

If Ollama reports a memory error, use a machine with more available RAM or configure a smaller local model in `.env`, such as `gemma3:1b`.

The app remains usable for demo purposes because the response composer falls back to a deterministic safe bridge when the LLM is unavailable.

## Dependency is missing

Install project dependencies:

```bash
pip install -r requirements.txt
```

Then validate:

```bash
python -m pytest
```

## Local SQLite data needs to be removed

Delete the local demo database:

```powershell
Remove-Item data/interactions.sqlite3
```

Only anonymized consented records should be present in this database.

You can also delete local records from the app sidebar under `Local data`.
