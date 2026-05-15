from empathy_engine.agents.bias_safety_agent import BiasSafetyAgent
from empathy_engine.agents.context_decoder import ContextDecoderAgent
from empathy_engine.agents.double_empathy_analyzer import DoubleEmpathyAnalyzerAgent
from empathy_engine.agents.perspective_translator import PerspectiveTranslatorAgent
from empathy_engine.agents.sensory_load_agent import SensoryLoadAgent
from empathy_engine.schemas import ResponseComposerInput


def build_response_input(output_language="en"):
    context = ContextDecoderAgent().run("A direct message was misunderstood.")
    analysis = DoubleEmpathyAnalyzerAgent().run(context)
    translation = PerspectiveTranslatorAgent().run(analysis)
    sensory_load = SensoryLoadAgent().run("A noisy meeting felt rushed.")
    safety = BiasSafetyAgent().run({
        "context": context,
        "analysis": analysis,
        "translation": translation,
        "sensory_load": sensory_load,
    })

    return ResponseComposerInput(
        analysis=analysis,
        translation=translation,
        sensory_load=sensory_load,
        safety=safety,
        user_language="en",
        processing_language="en",
        output_language=output_language,
    )
