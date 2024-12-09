#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import glob
import pandas as pd
from datetime import datetime

from jing.file_set import FileSet

class DataCenter:
    def __init__(self, market='us') -> None:
        self.market = market
        self.date = '2024-11-30'
        self.data_dir = "%s/data" % (os.getenv('PHOME'))
        self.fs = FileSet(self.data_dir)

    def one(self, _id, _date=""):
        today = datetime.today()
        self.date = today.strftime("%Y-%m-%d")
        if self.market == 'us':
            pass
        elif self.market == 'hk':
            pass
        else:
            pass

        if len(_date) > 0:
            self.date = _date

        df = self.fs.fetch(_id, self.date, self.market)
        return df

    def list(self, market="cn"):
        return self.listD(market)

    def listD(self, market="cn"):
        return self.fs.list(market)

    def csv(self, _id, _date=""):
        path = "/Users/allen/project/data/yf/%s.csv" % (_id)
        df = pd.read_csv(path)
        # print(df.dtypes)
        # print(df["Date"])
        # print(df["Date"].dtype)
        if len(_date) > 0:
            return df.loc[df['Date'] <= _date]
        return df
    
if __name__ == "__main__":
    dc = DataCenter('us')
    df = dc.one("IONQ")
    print(df)
    df = dc.list()
    print(df['code'])
