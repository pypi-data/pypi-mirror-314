# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_case_in_range_bounded_by_tokens_with_prefix_suffix

lTokens = []
lTokens.append(token.subprogram_body.designator)

oStartToken = token.function_specification.function_keyword
oEndToken = token.subprogram_body.semicolon


class rule_506(token_case_in_range_bounded_by_tokens_with_prefix_suffix):
    """
    This rule checks the function designator has proper case on the end function declaration.

    |configuring_uppercase_and_lowercase_rules_link|

    **Violation**

    .. code-block:: vhdl

       end function OVERFLOW;

    **Fix**

    .. code-block:: vhdl

       end function overflow;
    """

    def __init__(self):
        super().__init__(lTokens, oStartToken, oEndToken)
        self.groups.append("case::name")
