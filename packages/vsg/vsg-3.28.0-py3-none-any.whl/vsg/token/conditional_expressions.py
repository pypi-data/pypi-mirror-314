# -*- coding: utf-8 -*-

from vsg import parser


class when_keyword(parser.keyword):
    """
    unique_id = conditional_expressions : when_keyword
    """

    def __init__(self, sString):
        super().__init__(sString)


class else_keyword(parser.keyword):
    """
    unique_id = conditional_expressions : else_keyword
    """

    def __init__(self, sString):
        super().__init__(sString)
