# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_case_with_prefix_suffix

lTokens = []
lTokens.append(token.process_statement.process_label)


class rule_017(token_case_with_prefix_suffix):
    """
    This rule checks the process label has proper case.

    |configuring_uppercase_and_lowercase_rules_link|

    **Violation**

    .. code-block:: vhdl

       PROC_A : process (rd_en, wr_en, data_in, data_out,
                         rd_full, wr_full
                        ) is
       begin

    **Fix**

    .. code-block:: vhdl

       proc_a : process (rd_en, wr_en, data_in, data_out,
                         rd_full, wr_full
                        ) is
       begin
    """

    def __init__(self):
        super().__init__(lTokens)
        self.groups.append("case::label")
