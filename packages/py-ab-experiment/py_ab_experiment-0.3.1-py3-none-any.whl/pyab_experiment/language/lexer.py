"""Lexical Analysis for Experiment Language Definition

This module defines the lexer for the experiment language definition.
It includes common constructs such as operators, identifiers, and literals
(floats, integers). The module also defines reserved keywords used by the grammar.

The lexical analysis is performed using YACC (via the SLY implementation)
for finite state automaton processing.
"""

# flake8: noqa
from pyab_experiment.sly import Lexer


class ExperimentLexer(Lexer):
    """Lexical analyzer for an AB testing configuration language.

    This class provides a method for tokenizing an AB testing configuration
    file into a list of tokens, to be used for parsing and validation, in conjunction
    with the grammar defined in a companion class.
    The lexer uses regular expressions to match terminal patterns in the configuration
    file and generate corresponding tokens.
    """

    # define token list to be used by the grammar
    tokens = {
        ID,
        NON_NEG_INTEGER,
        NON_NEG_FLOAT,
        STRING_LITERAL,
        LPAREN,
        RPAREN,
        MINUS,
        COMMA,
        COLON,
        LBRACE,
        RBRACE,
        KW_EQ,
        KW_GT,
        KW_LT,
        KW_GE,
        KW_LE,
        KW_NE,
        KW_IN,
        KW_NOT,
        KW_NOT_IN,
        KW_DEF,
        KW_SALT,
        KW_SPLITTERS,
        KW_IF,
        KW_ELIF,
        KW_ELSE,
        KW_WEIGHTED,
        KW_RETURN,
        KW_AND,
        KW_OR,
    }

    # Special symbols
    LPAREN = r"\("
    RPAREN = r"\)"
    MINUS = r"-"
    COMMA = r","
    COLON = r":"
    LBRACE = r"{"
    RBRACE = r"}"

    # logical operators
    KW_EQ = r"=="
    KW_GT = r">"
    KW_LT = r"<"
    KW_GE = r">="
    KW_LE = r"<="
    KW_NE = r"!="
    KW_IN = r"in"
    KW_NOT_IN = r"not\s+in"
    KW_NOT = r"not"

    # reserved kw
    KW_DEF = r"def"
    KW_SALT = r"salt"
    KW_SPLITTERS = r"splitters"
    KW_IF = r"if"
    KW_ELIF = r"else\s*if"
    KW_ELSE = r"else"
    KW_WEIGHTED = r"weighted"
    KW_RETURN = r"return"
    KW_AND = r"and"
    KW_OR = r"or"

    # identifiers
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # literals
    @_(r"\d+\.\d+")
    def NON_NEG_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r"\d+")
    def NON_NEG_INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r"\".*?\"|\'.*?\'")
    def STRING_LITERAL(self, t):
        t.value = t.value[1:-1]
        return t

    # block comment
    @_(r"/\*")
    def BLOCK_COMMENT_START(self, t):
        self.push_state(BlockComment)

    # regular comments
    ignore_inline_comment = r"//.*"

    # Ignored pattern
    ignore_newline = r"\n+"
    ignore_ws = r"\s+"

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class BlockComment(Lexer):
    """Helper state that deals with C style opening
    and closing block comments"""

    tokens = {BLOCK_COMMENT_END}

    @_(r".*\*/")
    def BLOCK_COMMENT_END(self, t):
        self.pop_state()

    @_(r".+")
    def t_block_comment_content(self, t):
        pass

    ignore_newline = r"\n+"

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")
