# -*- coding: utf-8 -*-

from vsg import parser


class use_keyword(parser.keyword):
    """
    unique_id = binding_indication : use_keyword
    """

    def __init__(self, sString):
        super().__init__(sString)
