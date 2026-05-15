from pydantic import BaseModel, Field

from empathy_engine.errors import PersistenceError, WorkflowExecutionError
from empathy_engine.orchestration.workflow import EmpathyWorkflow
from empathy_engine.presentation.result_presenter import ResultPresenter
from empathy_engine.storage.interaction_store import InteractionStore


class AnalyzeInteractionCommand(BaseModel):
    interaction: str = Field(min_length=1)
    output_language: str = "en"
    store_consent: bool = False
    feedback: str | None = None
    use_llm: bool = True


class AnalyzeInteractionResult(BaseModel):
    workflow_result: dict
    display_result: dict
    stored_record_id: int | None = None


class AnalyzeInteractionUseCase:

    def __init__(self, workflow=None, presenter=None, store=None):
        self.workflow = workflow
        self.presenter = presenter or ResultPresenter()
        self.store = store or InteractionStore()

    def execute(self, command: AnalyzeInteractionCommand) -> AnalyzeInteractionResult:
        workflow = self.workflow or EmpathyWorkflow(use_llm=command.use_llm)

        try:
            workflow_result = workflow.run(
                command.interaction,
                output_language=command.output_language,
            )
        except Exception as error:
            raise WorkflowExecutionError(str(error)) from error

        display_result = self.presenter.present(
            workflow_result,
            command.output_language,
        )

        stored_record_id = None
        if command.store_consent:
            try:
                stored_record_id = self.store.save(
                    workflow_result["interaction"],
                    workflow_result,
                    command.feedback,
                )
            except Exception as error:
                raise PersistenceError(str(error)) from error

        return AnalyzeInteractionResult(
            workflow_result=workflow_result,
            display_result=display_result,
            stored_record_id=stored_record_id,
        )
