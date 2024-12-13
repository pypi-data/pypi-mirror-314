import hashlib
from functools import partial  # noqa: F401

from pyab_experiment.binning.binning import deterministic_choice  # noqa: F401
from pyab_experiment.codegen.python.custom_exceptions import (  # noqa: F401
    ExperimentConditionalFailedError,
)
from pyab_experiment.codegen.python.python_generator import PythonCodeGen
from pyab_experiment.utils.wraper_functions import parse_source

# Note the noqa 401's ignoring the imported, not used
# we are loading dynamic code that needs this libraries. so they are used
# but flake can't know about it by looking at the static files


class ExperimentEvaluator:
    """Experiment evaluator class. What we do here is to take the experiment source,
    compile it, and generate the python functions.
    These functions are then set inside the class to expose them to the outside world

    The advantage is that we can easily load new source code at runtime, while keeping
    tabs of it's checksum to avoid re-compiling the same source file multiple times.
    Also since the class manages the source code & compilation it avoids calls to exec
    from unknown sources, since the code is self generated from the source file that
    follows a strict grammar takes a source code file, generates the python functions
    and plugs them into the class
    """

    _checksum: str = ""

    def __init__(self, source_code: str) -> None:
        self.recompile(source_code)

    def recompile(self, source_code: str) -> None:
        """Recompiles the source code.

        This method takes a string of source code and recompiles it.

        Args:
            source_code (str): The source code to recompile.

        Returns:
            None: This method does not return a value, but it recompiles the
                  source code.

        Raises:
            YaccError: If the source code is not valid (parsing error,
            or invalid characters)
        """
        new_checksum = hashlib.md5(source_code.encode("utf-8")).hexdigest()

        # only trigger a recompile on code that has changed
        if self._checksum != new_checksum:
            code_holder = {}
            self._checksum = new_checksum

            ast = parse_source(source_code)
            fn_name = ast.id
            exec(
                compile(
                    PythonCodeGen(
                        ast, expose_experiment_variant_function=False
                    ).generate(),
                    "<string>",
                    "exec",
                ),
                None,
                code_holder,
            )
            setattr(
                self, "run_experiment", code_holder[fn_name]
            )  # initialize the function

    def run_experiment(self, **kwargs):
        raise RuntimeError("Code was not loaded")

    def __call__(self, **kwargs):
        return self.run_experiment(**kwargs)
