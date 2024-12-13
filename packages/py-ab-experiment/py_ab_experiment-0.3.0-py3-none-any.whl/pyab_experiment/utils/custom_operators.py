"""_summary_
tiny module to define custom operators
"""

import operator
from typing import Container


def operator_in(__a: object, __b: Container[object]) -> bool:
    return operator.contains(__b, __a)


def operator_not_in(__a: object, __b: Container[object]) -> bool:
    return not operator.contains(__b, __a)
