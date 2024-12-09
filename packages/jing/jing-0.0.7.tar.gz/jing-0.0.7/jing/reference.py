#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from jing.data_center import DataCenter
from jing.tech import Tech

class Reference:
    def __init__(self, _df) -> None:
        self.df = Tech(_df).calc()
        self.df = self.df.sort_index(ascending=False).dropna()

    def close(self, _i):
        try:
            v = self.df['Close'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def vol(self, _i):
        try:
            v = self.df['Volume'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def len(self):
        return len(self.df)

    def date(self, _i):
        try:
            v = self.df.index[_i]
            return v
        except Exception as e:
            print(e)
            return e

    def ma20(self, _i):
        try:
            v = self.df['ma20'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def ma50(self, _i):
        try:
            v = self.df['ma50'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def ma200(self, _i):
        try:
            v = self.df['ma200'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def Ma200(self):
        return self.df['ma200'].dropna()

    def Ma50(self):
        return self.df['ma50'].dropna()

    def Close(self):
        return self.df['Close'].dropna()

    def vma50(self, _i):
        try:
            v = self.df['vma50'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def macd(self, _i):
        try:
            v = self.df['macd'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def diff(self, _i):
        try:
            v = self.df['diff'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

    def dea(self, _i):
        try:
            v = self.df['dea'].iloc[_i]
            return float(v)
        except Exception as e:
            print(e)
            return e

if __name__ == "__main__":
    dc = DataCenter()
    df = dc.one("IONQ", _date='2024-09-27')
    ref = Reference(df)
    price = ref.close(0)
    vol = ref.vol(0)
    print(price, vol, ref.date(0), ref.ma20(0), ref.ma50(0), ref.ma200(0), ref.vma50(0), ref.macd(0), ref.diff(0), ref.dea(0))
