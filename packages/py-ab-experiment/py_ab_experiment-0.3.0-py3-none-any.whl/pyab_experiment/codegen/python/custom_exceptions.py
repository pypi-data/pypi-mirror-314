__all__ = [
    "ExperimentConditionalFailedError",
]


class ExperimentConditionalFailedError(Exception):
    """Raised whenever the experiment conditional evaluation
    fails. This can occurs whenever defaults are not properly
    defined on an experiment conditional
    """

    def __init__(self, message="Experiment conditional evaluation failed"):
        super().__init__(message)
