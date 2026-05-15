from typing import Protocol


class LLMClientPort(Protocol):

    def generate(self, prompt: str) -> str:
        ...


class InteractionStorePort(Protocol):

    def save(self, anonymized_interaction: str, result: dict, feedback=None):
        ...
