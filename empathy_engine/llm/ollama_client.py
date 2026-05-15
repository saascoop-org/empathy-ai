import os


class OllamaClient:

    def __init__(self, model=None):
        import ollama
        from dotenv import load_dotenv

        load_dotenv()
        self.model = model or os.getenv("GEMMA_MODEL", "gemma3:1b")
        base_url = os.getenv("OLLAMA_BASE_URL")
        self.client = ollama.Client(host=base_url) if base_url else ollama.Client()

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
