"""
Package sourced from https://github.com/dabeaz/sly

SLY (Sly Lex Yacc)
source documentation not included in docs to improve readability. For detailed
information refer to either the GH repo 👉 https://github.com/dabeaz/sly
or to the documentation page 👉 https://sly.readthedocs.io/en/latest/sly.html

"""

# flake8: noqa
from .lex import *
from .yacc import *

__all__ = [*lex.__all__, *yacc.__all__]
