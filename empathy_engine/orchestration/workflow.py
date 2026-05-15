from empathy_engine.agents.context_decoder import ContextDecoderAgent
from empathy_engine.agents.double_empathy_analyzer import DoubleEmpathyAnalyzerAgent
from empathy_engine.agents.bias_safety_agent import BiasSafetyAgent
from empathy_engine.agents.learning_coach import LearningCoachAgent
from empathy_engine.agents.perspective_translator import PerspectiveTranslatorAgent
from empathy_engine.agents.response_composer import ResponseComposerAgent
from empathy_engine.agents.sensory_load_agent import SensoryLoadAgent
from empathy_engine.config import load_settings
from empathy_engine.i18n.language import (
    detect_user_language,
    normalize_language,
)
from empathy_engine.llm.ollama_client import OllamaClient
from empathy_engine.observability import WorkflowTimer, get_logger, log_event
from empathy_engine.safety.anonymizer import Anonymizer
from empathy_engine.schemas import (
    LanguageMetadata,
    LearningCoachInput,
    ResponseComposerInput,
    SafetyReviewInput,
    WorkflowExecutionMetadata,
    WorkflowResult,
)


class EmpathyWorkflow:

    def __init__(self, use_llm=False):
        self.settings = load_settings()
        llm_client = OllamaClient(settings=self.settings) if use_llm else None
        self.anonymizer = Anonymizer()
        self.context_agent = ContextDecoderAgent()
        self.double_empathy_agent = DoubleEmpathyAnalyzerAgent()
        self.translator_agent = PerspectiveTranslatorAgent()
        self.sensory_load_agent = SensoryLoadAgent()
        self.bias_safety_agent = BiasSafetyAgent()
        self.response_composer_agent = ResponseComposerAgent(llm_client)
        self.learning_coach_agent = LearningCoachAgent()

    def run(self, interaction: str, output_language="en"):
        timer = WorkflowTimer()
        logger = get_logger()

        user_language = timer.measure(
            "detect_language",
            lambda: detect_user_language(interaction),
        )
        processing_language = self.settings.processing_language
        output_language = normalize_language(output_language)
        anonymized_interaction = timer.measure(
            "anonymize",
            lambda: self.anonymizer.anonymize(interaction),
        )

        context = timer.measure(
            "context_decoder",
            lambda: self.context_agent.run(anonymized_interaction),
        )

        analysis = timer.measure(
            "double_empathy_analyzer",
            lambda: self.double_empathy_agent.run(context),
        )

        translation = timer.measure(
            "perspective_translator",
            lambda: self.translator_agent.run(analysis),
        )

        sensory_load = timer.measure(
            "sensory_load",
            lambda: self.sensory_load_agent.run(anonymized_interaction),
        )

        safety = timer.measure(
            "bias_safety",
            lambda: self.bias_safety_agent.run(
                SafetyReviewInput(
                    context=context,
                    analysis=analysis,
                    translation=translation,
                    sensory_load=sensory_load,
                )
            )
        )

        response = timer.measure(
            "response_composer",
            lambda: self.response_composer_agent.run(
                ResponseComposerInput(
                    analysis=analysis,
                    translation=translation,
                    sensory_load=sensory_load,
                    safety=safety,
                    user_language=user_language,
                    processing_language=processing_language,
                    output_language=output_language,
                )
            )
        )

        if response.llm_status not in (None, "ok"):
            log_event(
                logger,
                "llm_fallback",
                llm_status=response.llm_status,
                output_language=output_language,
            )

        learning = timer.measure(
            "learning_coach",
            lambda: self.learning_coach_agent.run(
                LearningCoachInput(
                    context=context,
                    analysis=analysis,
                    translation=translation,
                    response=response,
                )
            )
        )

        execution = WorkflowExecutionMetadata(
            total_duration_ms=timer.total_duration_ms(),
            steps=timer.steps,
        )

        log_event(
            logger,
            "workflow_completed",
            output_language=output_language,
            processing_language=processing_language,
            step_count=len(execution.steps),
            total_duration_ms=execution.total_duration_ms,
            llm_status=response.llm_status,
        )

        result = WorkflowResult(
            interaction=anonymized_interaction,
            language=LanguageMetadata(
                user_language=user_language,
                processing_language=processing_language,
                output_language=output_language,
            ),
            context=context,
            analysis=analysis,
            translation=translation,
            sensory_load=sensory_load,
            safety=safety,
            response=response,
            learning=learning,
            execution=execution,
        )

        return result.model_dump()
