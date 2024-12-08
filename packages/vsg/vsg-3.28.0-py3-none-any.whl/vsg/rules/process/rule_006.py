# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_indent

lTokens = []
lTokens.append(token.process_statement.end_keyword)


class rule_006(token_indent):
    """
    This rule checks the indent of the **end process** keywords.

    **Violation**

    .. code-block:: vhdl

       proc_a : process (rd_en, wr_en, data_in, data_out,
                         rd_full, wr_full
                        ) is
       begin

         end process proc_a;

    **Fix**

    .. code-block:: vhdl

       proc_a : process (rd_en, wr_en, data_in, data_out,
                         rd_full, wr_full
                        ) is
       begin

       end process proc_a;
    """

    def __init__(self):
        super().__init__(lTokens)
