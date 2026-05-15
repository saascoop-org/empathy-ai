class EmpathyEngineError(Exception):
    """Base application error for recoverable engine failures."""


class WorkflowExecutionError(EmpathyEngineError):
    """Raised when the analysis workflow cannot complete."""


class PersistenceError(EmpathyEngineError):
    """Raised when consented local persistence fails."""
