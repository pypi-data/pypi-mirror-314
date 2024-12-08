# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_indent

lTokens = []
lTokens.append(token.case_generate_statement.generate_label)
lTokens.append(token.for_generate_statement.generate_label)
lTokens.append(token.if_generate_statement.generate_label)


class rule_001(token_indent):
    """
    This rule checks the indent of the generate declaration.

    **Violation**

    .. code-block:: vhdl

       architecture rtl of fifo is
       begin

       ram_array : for i in 0 to 7 generate

             ram_array : for i in 0 to 7 generate

    **Fix**

    .. code-block:: vhdl

       architecture rtl of fifo is
       begin

         ram_array : for i in 0 to 7 generate

         ram_array : for i in 0 to 7 generate
    """

    def __init__(self):
        super().__init__(lTokens)
