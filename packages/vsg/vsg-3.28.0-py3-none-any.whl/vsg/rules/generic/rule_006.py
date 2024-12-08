# -*- coding: utf-8 -*-

from vsg import parser, token
from vsg.rules.whitespace_between_token_pairs_bounded_by_tokens import Rule

lTokens = []
lTokens.append([token.interface_constant_declaration.assignment, parser.todo])
lTokens.append([token.interface_signal_declaration.assignment, parser.todo])
lTokens.append([token.interface_variable_declaration.assignment, parser.todo])
lTokens.append([token.interface_unknown_declaration.assignment, parser.todo])

oStart = token.generic_clause.open_parenthesis
oEnd = token.generic_clause.close_parenthesis


class rule_006(Rule):
    """
    This rule checks for a single space after the default assignment.

    |configuring_whitespace_rules_link|

    **Violation**

    .. code-block:: vhdl

       g_width : integer :=32;
       g_depth : integer :=     512;

    **Fix**

    .. code-block:: vhdl

       g_width : integer := 32;
       g_depth : integer := 512;
    """

    def __init__(self):
        super().__init__(lTokens, oStart, oEnd)
