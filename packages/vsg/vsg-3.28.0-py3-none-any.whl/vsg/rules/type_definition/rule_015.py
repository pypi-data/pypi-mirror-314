# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_prefix

lTokens = []
lTokens.append(token.incomplete_type_declaration.identifier)
lTokens.append(token.full_type_declaration.identifier)


class rule_015(token_prefix):
    """
    This rule checks for valid prefixes in user defined type identifiers.
    The default new type prefix is *t_*.

    |configuring_prefix_and_suffix_rules_link|

    **Violation**

    .. code-block:: vhdl

       type my_type is range -5 to 5 ;

    **Fix**

    .. code-block:: vhdl

       type t_my_type is range -5 to 5 ;
    """

    def __init__(self):
        super().__init__(lTokens)
        self.prefixes = ["t_"]
        self.solution = "Type identifiers"
