# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_case as Rule

lTokens = []
lTokens.append(token.for_generate_statement.generate_keyword)


class rule_501(Rule):
    """
    This rule checks the *generate* keyword has proper case.

    |configuring_uppercase_and_lowercase_rules_link|

    **Violation**

    .. code-block:: vhdl

       for x in range (3 downto 0) GENERATE

    **Fix**

    .. code-block:: vhdl

       for x in range (3 downto 0) generate
    """

    def __init__(self):
        super().__init__(lTokens)
        self.groups.append("case::keyword")
