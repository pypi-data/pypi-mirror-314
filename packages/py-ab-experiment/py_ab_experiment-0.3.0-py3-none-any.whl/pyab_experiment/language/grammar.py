"""Grammar definition for our AP experiment language"""

# flake8: noqa
from pyab_experiment.data_structures.syntax_tree import (
    BooleanOperatorEnum,
    ConditionalType,
    ExperimentAST,
    ExperimentConditional,
    ExperimentGroup,
    Identifier,
    LogicalOperatorEnum,
    RecursivePredicate,
    TerminalPredicate,
)
from pyab_experiment.language.lexer import ExperimentLexer
from pyab_experiment.sly import Parser


class ExperimentParser(Parser):
    """Defines the grammar for an AB testing configuration language.

    This class defines a set of rules (grammar) for parsing and validating AB testing
    configuration files. The grammar defines the structure and syntax of the
    configuration language, which is used to specify AB tests and their
    associated settings.
    """

    # Uncomment to print updated grammar
    # debugfile = 'parser.out'
    tokens = ExperimentLexer.tokens

    precedence = (
        ("left", KW_OR),
        ("left", KW_AND),
        ("left", KW_NOT),
    )

    @_("header_id LBRACE opt_header_salt opt_splitter conditional RBRACE")
    def header(self, p):
        return ExperimentAST(
            id=p.header_id,
            splitting_fields=p.opt_splitter,
            salt=p.opt_header_salt,
            conditions=p.conditional,
        )

    # *********** HEADER FIELDS *****************
    @_("")
    def empty(self, p):
        pass

    @_("KW_DEF ID")
    def header_id(self, p):
        return p.ID

    @_("empty")
    def opt_header_salt(self, p):
        return None

    @_("KW_SALT COLON STRING_LITERAL")
    def opt_header_salt(self, p):
        return p.STRING_LITERAL

    @_("empty")
    def opt_splitter(self, p):
        return None

    @_("KW_SPLITTERS COLON fields")
    def opt_splitter(self, p):
        return p.fields

    @_("ID COMMA fields")
    def fields(self, p):
        return [p.ID] + p.fields

    @_("ID")
    def fields(self, p):
        return [p.ID]

    # *************** Conditional rules *******************************
    @_("KW_IF predicate LBRACE conditional RBRACE subconditional ")
    def conditional(self, p):
        return ExperimentConditional(
            conditional_type=ConditionalType.IF,
            predicate=p.predicate,
            true_branch=p.conditional,
            false_branch=p.subconditional,
        )

    @_("return_expr")
    def conditional(self, p):
        # "unconditioned" conditional. serves as a stop recursion rule
        return p.return_expr

    @_("KW_ELIF predicate LBRACE conditional RBRACE subconditional")
    def subconditional(self, p):
        return ExperimentConditional(
            conditional_type=ConditionalType.ELIF,
            predicate=p.predicate,
            true_branch=p.conditional,
            false_branch=p.subconditional,
        )

    @_("KW_ELSE LBRACE conditional RBRACE")
    def subconditional(self, p):
        return ExperimentConditional(
            conditional_type=ConditionalType.ELSE,
            predicate=None,
            true_branch=p.conditional,
            false_branch=None,
        )

    @_("empty")
    def subconditional(self, p):
        return None

    # ************** predicates ****************
    @_("term logical_op term")
    def predicate(self, p):
        return TerminalPredicate(
            left_term=p.term0, logical_operator=p.logical_op, right_term=p.term1
        )

    @_("LPAREN predicate RPAREN")
    def predicate(self, p):
        return p.predicate

    @_("predicate KW_AND predicate")
    def predicate(self, p):
        return RecursivePredicate(
            left_predicate=p.predicate0,
            boolean_operator=BooleanOperatorEnum.AND,
            right_predicate=p.predicate1,
        )

    @_("predicate KW_OR predicate")
    def predicate(self, p):
        return RecursivePredicate(
            left_predicate=p.predicate0,
            boolean_operator=BooleanOperatorEnum.OR,
            right_predicate=p.predicate1,
        )

    @_("KW_NOT predicate")
    def predicate(self, p):
        return RecursivePredicate(
            left_predicate=p.predicate,
            boolean_operator=BooleanOperatorEnum.NOT,
            right_predicate=None,
        )

    @_("literal")
    def term(self, p):
        return p.literal

    @_("ID")
    def term(self, p):
        return Identifier(name=p.ID)

    @_("tuple")
    def term(self, p):
        return p.tuple

    @_("LPAREN term op_term")
    def tuple(self, p):
        return [p.term] + p.op_term

    @_("COMMA term op_term")
    def op_term(self, p):
        return [p.term] + p.op_term

    @_("RPAREN")
    def op_term(self, p):
        return []

    # ********** Boolean ops*********************

    @_("KW_LT")
    def logical_op(self, p):
        return LogicalOperatorEnum.LT

    @_("KW_GT")
    def logical_op(self, p):
        return LogicalOperatorEnum.GT

    @_("KW_GE")
    def logical_op(self, p):
        return LogicalOperatorEnum.GE

    @_("KW_LE")
    def logical_op(self, p):
        return LogicalOperatorEnum.LE

    @_("KW_IN")
    def logical_op(self, p):
        return LogicalOperatorEnum.IN

    @_("KW_NE")
    def logical_op(self, p):
        return LogicalOperatorEnum.NE

    @_("KW_EQ")
    def logical_op(self, p):
        return LogicalOperatorEnum.EQ

    @_("KW_NOT_IN")
    def logical_op(self, p):
        return LogicalOperatorEnum.NOT_IN

    # *********** RETURN STATEMENTS *****************
    @_("KW_RETURN return_statement")
    def return_expr(self, p):
        return p.return_statement

    @_("literal KW_WEIGHTED weight")
    def return_statement(self, p):
        return [ExperimentGroup(group_definition=p.literal, group_weight=p.weight)]

    @_("literal KW_WEIGHTED weight COMMA return_statement")
    def return_statement(self, p):
        return [
            ExperimentGroup(group_definition=p.literal, group_weight=p.weight)
        ] + p.return_statement

    # weights
    @_("NON_NEG_INTEGER")
    def weight(self, p):
        return p.NON_NEG_INTEGER

    @_("NON_NEG_FLOAT")
    def weight(self, p):
        return p.NON_NEG_FLOAT

    # ***************** literals ************************
    @_("MINUS NON_NEG_INTEGER")
    def literal(self, p):
        return -p.NON_NEG_INTEGER

    @_("MINUS NON_NEG_FLOAT")
    def literal(self, p):
        return -p.NON_NEG_FLOAT

    @_("NON_NEG_INTEGER")
    def literal(self, p):
        return p.NON_NEG_INTEGER

    @_("NON_NEG_FLOAT")
    def literal(self, p):
        return p.NON_NEG_FLOAT

    @_("STRING_LITERAL")
    def literal(self, p):
        return p.STRING_LITERAL
