#!/usr/bin/env python
# -*- encoding: utf8 -*-

from jing.data_center import DataCenter
from jing.reference import Reference

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

class Y:
    def __init__(self, code, _date="", _market="us") -> None:
        self.market = _market
        self.date = _date
        self.code = code

        self.data_center = DataCenter(self.market)
        self.df = self.data_center.one(self.code, self.date) 
        self.ref = Reference(self.df)

if __name__=="__main__":
    y = Y("IONQ", _date="2024-09-27")
    ref = y.ref
    print(ref.date(0), ref.ma20(0), ref.ma50(0), ref.ma200(0), ref.vma50(0), ref.macd(0), ref.diff(0), ref.dea(0))
