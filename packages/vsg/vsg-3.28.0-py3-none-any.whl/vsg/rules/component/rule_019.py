# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import remove_comments_from_end_of_lines_bounded_by_tokens

oStart = token.component_declaration.component_keyword

oEnd = token.component_declaration.semicolon


class rule_019(remove_comments_from_end_of_lines_bounded_by_tokens):
    """
    This rule checks for comments at the end of the port and generic clauses in component declarations.
    These comments represent additional maintenance.
    They will be out of sync with the entity at some point.
    Refer to the entity for port types, port directions and purpose.

    **Violation**

    .. code-block:: vhdl

       wr_en : in    std_logic;  -- Enables write to RAM
       rd_en : out   std_logic; -- Enable reads from RAM

    **Fix**

    .. code-block:: vhdl

       wr_en : in    std_logic;
       rd_en : out   std_logic;
    """

    def __init__(self):
        super().__init__(oStart, oEnd)
        self.solution = "Remove comment."
