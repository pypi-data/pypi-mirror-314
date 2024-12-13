"""parsing module"""

from black import FileMode, format_str

from pyab_experiment.codegen.python.python_generator import PythonCodeGen
from pyab_experiment.data_structures.syntax_tree import ExperimentAST
from pyab_experiment.language.grammar import ExperimentParser
from pyab_experiment.language.lexer import ExperimentLexer


def parse_source(text: str) -> ExperimentAST:
    lexer = ExperimentLexer()
    parser = ExperimentParser()
    return parser.parse(lexer.tokenize(text))


def generate_code(text: str, expose_internal_fn: bool = False) -> str:
    """end to end code generation
    high level spec comes in and python
    function comes out"""

    generator = PythonCodeGen(
        parse_source(text), expose_experiment_variant_function=expose_internal_fn
    )
    return format_str(generator.generate(), mode=FileMode())
