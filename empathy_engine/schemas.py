from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class InteractionRequest(BaseModel):
    interaction: str = Field(min_length=1)
    output_language: str = "en"


class LanguageMetadata(BaseModel):
    user_language: str
    processing_language: str = "en"
    output_language: str = "en"


class ContextResult(BaseModel):
    literal_language: bool
    ambiguity_level: str


class DoubleEmpathyAnalysis(BaseModel):
    gap_type: str
    possible_misinterpretation: str


class PerspectiveTranslation(BaseModel):
    translation_for_user: str
    translation_for_other_person: str


class SensoryLoadResult(BaseModel):
    possible_factors: list[str] = Field(default_factory=list)


class SafetyResult(BaseModel):
    safe: bool
    removed_terms: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    guidance: str


class SafetyReviewInput(BaseModel):
    context: ContextResult
    analysis: DoubleEmpathyAnalysis
    translation: PerspectiveTranslation
    sensory_load: SensoryLoadResult


class ResponseResult(BaseModel):
    bridge_message: str
    llm_status: str | None = None


class ResponseComposerInput(BaseModel):
    analysis: DoubleEmpathyAnalysis
    translation: PerspectiveTranslation
    sensory_load: SensoryLoadResult
    safety: SafetyResult
    user_language: str
    processing_language: str = "en"
    output_language: str = "en"


class LearningResult(BaseModel):
    reflection_question: str


class WorkflowStepMetric(BaseModel):
    name: str
    duration_ms: float


class WorkflowExecutionMetadata(BaseModel):
    total_duration_ms: float
    steps: list[WorkflowStepMetric] = Field(default_factory=list)


class LearningCoachInput(BaseModel):
    context: ContextResult
    analysis: DoubleEmpathyAnalysis
    translation: PerspectiveTranslation
    response: ResponseResult


class WorkflowResult(BaseModel):
    interaction: str
    language: LanguageMetadata
    context: ContextResult
    analysis: DoubleEmpathyAnalysis
    translation: PerspectiveTranslation
    sensory_load: SensoryLoadResult
    safety: SafetyResult
    response: ResponseResult
    learning: LearningResult
    execution: WorkflowExecutionMetadata


class StoredInteractionRecord(BaseModel):
    id: int | None = None
    created_at: str | None = None
    consent_version: str = "local-demo-v1"
    anonymized_interaction: str
    result_json: dict[str, Any]
    feedback: str | None = None
    db_path: Path | None = None


class StoredInteractionSummary(BaseModel):
    id: int
    created_at: str
    consent_version: str
    anonymized_interaction: str
    feedback: str | None = None


class FeedbackValue:
    USEFUL_SAFE = "useful_safe"
    PARTIALLY_USEFUL = "partially_useful"
    NOT_USEFUL = "not_useful"


FEEDBACK_LABELS = {
    "Useful and safe": FeedbackValue.USEFUL_SAFE,
    "Útil e segura": FeedbackValue.USEFUL_SAFE,
    "Útil y segura": FeedbackValue.USEFUL_SAFE,
    "Partially useful": FeedbackValue.PARTIALLY_USEFUL,
    "Parcialmente útil": FeedbackValue.PARTIALLY_USEFUL,
    "No útil": FeedbackValue.NOT_USEFUL,
    "Not useful": FeedbackValue.NOT_USEFUL,
    "Não útil": FeedbackValue.NOT_USEFUL,
}


def normalize_feedback(feedback: str | None) -> str | None:
    if feedback is None:
        return None
    return FEEDBACK_LABELS.get(feedback, feedback)


def to_plain_data(value):
    if isinstance(value, BaseModel):
        return value.model_dump()
    if isinstance(value, dict):
        return {key: to_plain_data(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_plain_data(item) for item in value]
    return value
