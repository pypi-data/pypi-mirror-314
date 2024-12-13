
The PyAB experiment language is a domain-specific language for defining A/B tests. It follows
a C-style syntax while maintaining Python-like simplicity.
Referenced by the :py:mod:`Language pyab_experiment.language` module

.. _grammar:

Basic Structure
--------------

Each experiment is defined using this basic structure:

.. code-block:: python

    def experiment_name {
        [salt: "optional_salt"]
        [splitters: field1, field2, ...]
        conditional_logic
    }

Language Components
------------------

Return Statements
~~~~~~~~~~~~~~~~

Return statements define groups with weighted probabilities:

.. code-block:: python

    return "control" weighted 1,
           "variant_a" weighted 2,
           "variant_b" weighted 1

This means:
- variant_a has 2x the probability of being selected compared to control or variant_b
- Total weights: 4 (1+2+1), so probabilities are:
    - control: 25%
    - variant_a: 50%
    - variant_b: 25%

Conditional Logic
~~~~~~~~~~~~~~~

The language supports nested if/else if/else statements:

.. code-block:: python

    if user_id in (1,2,3) {
        return "group1" weighted 1
    } else if country == "US" and age >= 18 {
        return "group2" weighted 1
    } else {
        return "default" weighted 1
    }

Supported Operators
~~~~~~~~~~~~~~~~

- Comparison: ``==``, ``!=``, ``>``, ``<``, ``>=``, ``<=``, ``in``, ``not in``
- Logical: ``and``, ``or``, ``not``
- Values can be:
    - Strings: ``"value"``
    - Numbers: ``42``, ``3.14``, ``-1``
    - Tuples: ``(1,2,3)``

Comments
~~~~~~~~

Supports both C-style comments:

.. code-block:: python

    // Single line comment
    /* Multi-line
       comment block */

Complete Example
--------------

Here's a real-world example with annotations:

.. code-block:: python

    def complex_experiment {
        // Salt ensures consistent group assignment
        salt: "user_exp_v1"

        // Fields used for splitting traffic
        splitters: user_id, country

        // Target specific user segments
        if age >= 21 and country in ("US", "CA") {
            // High-value markets get 3 variants
            return "control" weighted 1,
                   "variant_a" weighted 2,
                   "variant_b" weighted 2
        } else if country not in ("US", "CA") {
            // International markets get 2 variants
            return "int_control" weighted 1,
                   "int_variant" weighted 1
        } else {
            // Everyone else gets default experience
            return "default" weighted 1
        }
    }

Formal Grammar
-------------

The full grammar rules as defined in the language:

.. code-block:: python

    <S> ::= <header>

    <header> ::= <header_id> "{" <opt_header_salt> <opt_splitter> <conditional> "}"

    <empty> ::=

    <header_id> ::= KW_DEF <ID>

    <opt_header_salt> ::= KW_SALT ":" <STRING_LITERAL>
                        | <empty>

    <opt_splitter> ::= KW_SPLITTERS ":" <fields>
                     | <empty>

    <fields> ::= <ID>
               | <ID> "," <fields>

    <conditional> ::= <return_expr>
                    | KW_IF <predicate> "{" <conditional> "}" <subconditional>

    <subconditional> ::=
                   | KW_ELSE "{" <conditional> "}"
                   | KW_ELIF <predicate> "{" <conditional> "}" <subconditional>

    <predicate> ::= KW_NOT <predicate>
                  | <predicate> KW_OR <predicate>
                  | <predicate> KW_AND <predicate>
                  | "(" <predicate> ")"
                  | <term> <logical_op> <term>

Terminal Tokens
--------------

Special Symbols
~~~~~~~~~~~~~~

.. code-block:: text

    LPAREN      : \(
    RPAREN      : \)
    MINUS       : -
    COMMA       : ,
    COLON       : :
    LBRACE      : {
    RBRACE      : }

Logical Operators
~~~~~~~~~~~~~~~

.. code-block:: text

    KW_EQ       : ==
    KW_GT       : >
    KW_LT       : <
    KW_GE       : >=
    KW_LE       : <=
    KW_NE       : !=
    KW_IN       : in
    KW_NOT_IN   : not\s+in
    KW_NOT      : not

Reserved Keywords
~~~~~~~~~~~~~~~

.. code-block:: text

    KW_DEF          : def
    KW_SALT         : salt
    KW_SPLITTERS    : splitters
    KW_IF           : if
    KW_ELIF         : else\s*if
    KW_ELSE         : else
    KW_WEIGHTED     : weighted
    KW_RETURN       : return
    KW_AND          : and
    KW_OR           : or

Notes
-----

1. All numeric literals must be non-negative (minus sign handled separately)
2. String literals support both single and double quotes
3. Keywords are case-sensitive
4. Block comments support nesting through state management
5. Whitespace is significant for some operators (e.g., 'not in')
