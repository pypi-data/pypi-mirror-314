# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_case

lTokens = []
lTokens.append(token.entity_specification.entity_class)


class rule_503(token_case):
    """
    This rule checks the *entity_class* has proper case.

    |configuring_uppercase_and_lowercase_rules_link|

    **Violation**

    .. code-block:: vhdl

       attribute coordinate of comp_1 : COMPONENT is (0.0, 17.5);

    **Fix**

    .. code-block:: vhdl

       attribute coordinate of comp_1 : component is (0.0, 17.5);
    """

    def __init__(self):
        super().__init__(lTokens)
        self.groups.append("case::name")
        self.configuration.append("case_exceptions")
