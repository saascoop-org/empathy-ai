from empathy_engine.config import AppSettings, load_settings


class OllamaClient:

    def __init__(self, model=None, settings: AppSettings | None = None):
        import ollama

        self.settings = settings or load_settings()
        self.model = model or self.settings.gemma_model
        self.client = ollama.Client(host=self.settings.ollama_base_url)

    def generate(self, prompt: str):

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
