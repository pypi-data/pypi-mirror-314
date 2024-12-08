# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_prefix as Rule

lTokens = []
lTokens.append(token.alias_declaration.alias_designator)


class rule_600(Rule):
    """
    This rule checks for valid prefixes on alias designators.

    Default prefix is *a_*.

    |configuring_prefix_and_suffix_rules_link|

    **Violation**

    .. code-block:: vhdl

       alias header is name;
       alias footer is name;

    **Fix**

    .. code-block:: vhdl

       alias a_header is name;
       alias a_footer is name;
    """

    def __init__(self):
        super().__init__(lTokens)
        self.prefixes = ["a_"]
        self.solution = "Alias designators"
