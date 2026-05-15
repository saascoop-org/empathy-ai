from empathy_engine.i18n.language import localize_workflow_result


class ResultPresenter:

    def present(self, workflow_result: dict, output_language: str) -> dict:
        return localize_workflow_result(workflow_result, output_language)
