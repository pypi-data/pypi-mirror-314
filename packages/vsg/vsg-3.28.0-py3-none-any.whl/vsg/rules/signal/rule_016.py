# -*- coding: utf-8 -*-

from vsg import deprecated_rule


class rule_016(deprecated_rule.Rule):
    """
    This rule was deprecated and replaced with rule:

    * `signal_017 <signal_rules.html#signal-017>`_
    """

    def __init__(self):
        super().__init__()
        self.message.append("Rule " + self.unique_id + " has been replaced with the following rule:")
        self.message.append("  signal_017")
