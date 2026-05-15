import logging

from empathy_engine.safety.anonymizer import Anonymizer


class RedactingFormatter(logging.Formatter):

    def __init__(self, fmt=None):
        super().__init__(fmt or "%(levelname)s:%(name)s:%(message)s")
        self.anonymizer = Anonymizer()

    def format(self, record):
        record.msg = self.anonymizer.anonymize_for_persistence(str(record.msg))
        if record.args:
            record.args = tuple(
                self.anonymizer.anonymize_for_persistence(str(arg))
                for arg in record.args
            )
        return super().format(record)


def configure_safe_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter())

    logger = logging.getLogger("empathy_engine")
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False

    return logger
