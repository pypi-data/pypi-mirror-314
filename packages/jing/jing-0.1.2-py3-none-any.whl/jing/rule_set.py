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
        self.result = []

    def add_rule(self, _class):
        self.map[_class.__name__] = _class

    def get_result(self):
        return self.result

    def run(self):
        print('=' * 100)
        for rule_name, a_rule_class in self.map.items():
            print(f"rule[{rule_name}]")
            rule = a_rule_class(self.code, self.ref)
            good = rule.run()
            if good:
                self.result.append({'rule':rule_name, 'code':self.code})
            print('-' * 100)

if __name__=="__main__":
    # x = X("us", "2023-10-30")
    code = "IONQ"
    date = '2024-09-27'

    y = Y("IONQ", _date=date)
    ref = y.ref

    rs = RuleSet(code, ref)
    rs.add_rule(RuleSimple)
    rs.run()

    good = rs.get_result()
    print(good)

