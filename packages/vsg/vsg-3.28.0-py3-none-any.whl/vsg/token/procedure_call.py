# -*- coding: utf-8 -*-

from vsg import parser


class procedure_name(parser.item):
    """
    unique_id = procedure_call : procedure_name
    """

    def __init__(self, sString):
        super().__init__(sString)


class open_parenthesis(parser.open_parenthesis):
    """
    unique_id = procedure_call : open_parenthesis
    """

    def __init__(self, sString="("):
        super().__init__()


class close_parenthesis(parser.close_parenthesis):
    """
    unique_id = procedure_call : close_parenthesis
    """

    def __init__(self, sString=")"):
        super().__init__()
