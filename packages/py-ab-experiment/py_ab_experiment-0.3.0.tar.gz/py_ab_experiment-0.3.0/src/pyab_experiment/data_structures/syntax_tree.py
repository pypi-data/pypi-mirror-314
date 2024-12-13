"""
Module that houses the abstract syntax tree (AST) representation of an experiment
It's a collection of pydantic classes that represent a tree with several
specialized nodes each representing a specific data structure of the experiment
"""

from enum import Enum, auto
from typing import Union

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class LogicalOperatorEnum(Enum):
    """
    Enum representing the logical operators that can be used in a terminal predicate.
    """

    EQ = auto()
    GT = auto()
    LT = auto()
    GE = auto()
    LE = auto()
    NE = auto()
    IN = auto()
    NOT_IN = auto()


class BooleanOperatorEnum(Enum):
    """
    Enum representing the boolean operators that can be used in a
    recursive predicate, effectively chaining complex predicates.
    e.g. (predicate1 OR predicate2) AND NOT predicate3
    """

    AND = auto()
    OR = auto()
    NOT = auto()


class ConditionalType(Enum):
    """
    Enum representing the types of conditionals that can be used in an experiment.
    These are the classical if then else keywoods found in
    traditional programming languages
    """

    IF = auto()
    ELIF = auto()
    ELSE = auto()


class ExperimentGroup(BaseModel):
    """
    A group definition for an experiment. A group in an experiment
    (or element of a group) is a string associated with a weight
    The weight represents the likelyhood of choosing the element.

    For example with 2 groups A,B with weights 1,2 respectively.
    B is twice as likely to be chosen compared to A. Effectively
    the probability of choosing A becomes 1/3, while P(choosing B)
    becomes 2/3

    Attributes:
        group_definition (str): The definition of the group.
        group_weight (Union[NonNegativeFloat, NonNegativeInt]): The weight of the group.
    """

    group_definition: Union[int, float, str]
    group_weight: Union[NonNegativeFloat, NonNegativeInt]

    class Config:
        smart_union = True


class Identifier(BaseModel):
    """
    A model representing an identifier. (i.e a variable or function name)

    Attributes:
        name (str): The name of the identifier.
    """

    name: str


class TerminalPredicate(BaseModel):
    """
    A model representing a terminal predicate. A terminal predicate
    typically consists of 2 terms (either literals, or identifiers)
    and a boolean operand between them.

    for example in the predicate my_int_variable >= 2, we have
    my_variable: - the left term
    ">=" the operand
    "2" - the right term (int literal with value 2)

    Attributes:
        left_term (Union[float, int, str, tuple, Identifier]):
            The left term of the predicate.
        logical_operator (LogicalOperatorEnum):
            The logical operator used in the predicate.
        right_term (Union[float, int, str, tuple, Identifier]):
            The right term of the predicate.
    """

    left_term: Union[float, int, str, tuple, Identifier]
    logical_operator: LogicalOperatorEnum
    right_term: Union[float, int, str, tuple, Identifier]


class RecursivePredicate(BaseModel):
    """
    A model representing a recursive predicate.
    Similar to terminal predicates, but chains recursive definitions with logical
    operators.

    e.g. in predicate1 AND predicate2
    predicate1 is the left term
    AND is the logical operator
    predicate2 is the right term

    Attributes:
        left_predicate (Union[TerminalPredicate, "RecursivePredicate"]):
            The left predicate of the recursive predicate.
        boolean_operator (BooleanOperatorEnum):
            The boolean operator used in the recursive predicate.
        right_predicate (Union[TerminalPredicate, "RecursivePredicate", None]):
            The right predicate of the recursive predicate.
    """

    left_predicate: Union[TerminalPredicate, "RecursivePredicate"]
    boolean_operator: BooleanOperatorEnum
    right_predicate: Union[TerminalPredicate, "RecursivePredicate", None]


class ExperimentConditional(BaseModel):
    """
    A model representing a conditional  (if then else) in an experiment.

    Attributes:
        conditional_type (ConditionalType):
            The type of conditional - either IF, ELSE IF, or ELSE)
        predicate (Union[TerminalPredicate, RecursivePredicate, None]):
            The (possibly recursive) predicate used in the conditional.
        true_branch (Union[list[ExperimentGroup], "ExperimentConditional"]):
            The true branch of the conditional. could be a group (terminal) or
            nested conditional. For example IF p1{ IF (p2){...}}. Semantically
            represents the branch to explore if the predicate evaluates to TRUE

        false_branch (Union[list[ExperimentGroup], "ExperimentConditional", None]):
            The false branch of the conditional (if any) same as above, but
            semantically representing the branch to explore if the predicate is FALSE.
            Note that it may be None, for ex on a clause "IF p1{ branch1 }" if
            the predicate p1 is false there is no branch to explore
    """

    conditional_type: ConditionalType
    predicate: Union[TerminalPredicate, RecursivePredicate, None]
    true_branch: Union[list[ExperimentGroup], "ExperimentConditional"]
    false_branch: Union[list[ExperimentGroup], "ExperimentConditional", None]


class ExperimentAST(BaseModel):
    """
    A model representing the abstract syntax tree (AST) of an experiment.

    Attributes:
        id (str): The ID of the experiment.
        splitting_fields (List[str] | None):
            The fields used for splitting groups.
        salt (str | None):
            The salt used change hashing. Useful in case multiple experiments with the
            same splitting fields are used.

        conditions (Union[ExperimentConditional, List[ExperimentGroup]]):
            The conditions used in the experiment.
    """

    id: str
    splitting_fields: list[str] | None
    salt: str | None
    conditions: Union[ExperimentConditional, list[ExperimentGroup]]
