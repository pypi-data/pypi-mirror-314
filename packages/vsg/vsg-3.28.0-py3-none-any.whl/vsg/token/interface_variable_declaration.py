# -*- coding: utf-8 -*-

from vsg import parser


class variable_keyword(parser.keyword):
    """
    unique_id = interface_variable_declaration : variable_keyword
    """

    def __init__(self, sString):
        super().__init__(sString)


class identifier(parser.identifier):
    """
    unique_id = interface_variable_declaration : identifier
    """

    def __init__(self, sString):
        super().__init__(sString)


class colon(parser.colon):
    """
    unique_id = interface_variable_declaration : colon
    """

    def __init__(self, sString=":"):
        super().__init__()


class assignment(parser.assignment):
    """
    unique_id = interface_variable_declaration : assignment
    """

    def __init__(self, sString):
        super().__init__(sString)
