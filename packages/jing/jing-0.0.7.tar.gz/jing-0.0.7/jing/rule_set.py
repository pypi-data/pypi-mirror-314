#!/usr/bin/env python
# -*- encoding: utf8 -*-

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from jing.trend import Trend
from jing.y import Y
from jing.rule import RuleSimple

pd.set_option('display.max_columns', None)

class RuleSet:
    def __init__(self, _code, _ref) -> None:
        self.code = _code
        self.ref = _ref
        self.map = {}

    def add_rule(self, _class):
        self.map[_class.__name__] = _class

    def run(self):
        print('=' * 100)
        for name, a_rule_class in self.map.items():
            print('-' * 100)
            print(f"rule[{name}]")
            rule = a_rule_class(self.code, self.ref)
            rule.run()

if __name__=="__main__":
    # x = X("us", "2023-10-30")
    code = "IONQ"
    date = '2024-09-27'

    y = Y("IONQ", _date=date)
    ref = y.ref

    rs = RuleSet(code, ref)
    rs.add_rule(RuleSimple)
    rs.run()

