from empathy_engine.agents.context_decoder import ContextDecoderAgent
from empathy_engine.agents.double_empathy_analyzer import DoubleEmpathyAnalyzerAgent
from empathy_engine.agents.bias_safety_agent import BiasSafetyAgent
from empathy_engine.agents.learning_coach import LearningCoachAgent
from empathy_engine.agents.perspective_translator import PerspectiveTranslatorAgent
from empathy_engine.agents.response_composer import ResponseComposerAgent
from empathy_engine.agents.sensory_load_agent import SensoryLoadAgent
from empathy_engine.llm.ollama_client import OllamaClient
from empathy_engine.safety.anonymizer import Anonymizer


class EmpathyWorkflow:

    def __init__(self, use_llm=False):
        llm_client = OllamaClient() if use_llm else None
        self.anonymizer = Anonymizer()
        self.context_agent = ContextDecoderAgent()
        self.double_empathy_agent = DoubleEmpathyAnalyzerAgent()
        self.translator_agent = PerspectiveTranslatorAgent()
        self.sensory_load_agent = SensoryLoadAgent()
        self.bias_safety_agent = BiasSafetyAgent()
        self.response_composer_agent = ResponseComposerAgent(llm_client)
        self.learning_coach_agent = LearningCoachAgent()

    def run(self, interaction: str):
        anonymized_interaction = self.anonymizer.anonymize(interaction)

        context = self.context_agent.run(anonymized_interaction)

        analysis = self.double_empathy_agent.run(context)

        translation = self.translator_agent.run(analysis)

        sensory_load = self.sensory_load_agent.run(anonymized_interaction)

        safety = self.bias_safety_agent.run({
            "context": context,
            "analysis": analysis,
            "translation": translation,
            "sensory_load": sensory_load
        })

        response = self.response_composer_agent.run({
            "analysis": analysis,
            "translation": translation,
            "sensory_load": sensory_load,
            "safety": safety
        })

        learning = self.learning_coach_agent.run({
            "context": context,
            "analysis": analysis,
            "translation": translation,
            "response": response
        })

        return {
            "interaction": anonymized_interaction,
            "context": context,
            "analysis": analysis,
            "translation": translation,
            "sensory_load": sensory_load,
            "safety": safety,
            "response": response,
            "learning": learning
        }
