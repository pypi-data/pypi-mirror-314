
#!/usr/bin/env python
# -*- encoding: utf8 -*-

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from jing.x import X
from jing.rule_set import RuleSet
from jing.rule import RuleSimple
from jing.rule import RulePriceBreakout
from jing.rule import RuleVolumeBreakout
from jing.rule import RuleMa50Ma200

pd.set_option('display.max_columns', None)


class Regression:
    def __init__(self) -> None:
        pass

    def breakoutList(self):
        rule = RulePriceBreakout
        l = [
            ["2024-01-19", "SMCI", rule],
            ["2023-10-27", "DECK", rule],
            ["2023-11-30", "CRM", rule],
        ]
        return l

    def ma50Ma200List(self):
        rule = RuleMa50Ma200
        l = [
            [ "2023-10-30", "NFLX", rule],
            [ "2023-11-07", "CRM", rule ],
            [ "2024-01-10", "MDB", rule ],
            [ "2023-11-01", "AMD", rule ],
            [ "2023-11-02", "UBER", rule ],
        ]
        return l

    def volumeBreakoutList(self):
        rule = RuleVolumeBreakout
        l = [
            ["2023-05-24", "ANF", rule],
            ["2024-01-19", "SMCI", rule],
        ]
        return l

    def runOne(self, _list):
        for one in _list:
            dt   = one[0]
            code = one[1]
            rule = one[2]
            print(dt, code, rule)
            x = X("us", dt, code)
            x.add_rule(rule)
            x.run()

    def run(self):
        l = self.breakoutList()
        self.runOne(l)

        l = self.ma50Ma200List()
        self.runOne(l)

        l = self.volumeBreakoutList()
        self.runOne(l)

if __name__=="__main__":
    r = Regression()
    r.run()
