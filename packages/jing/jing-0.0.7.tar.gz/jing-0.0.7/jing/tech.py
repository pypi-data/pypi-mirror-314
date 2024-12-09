#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
from jing.data_center import DataCenter

class Tech:
    def __init__(self, _df) -> None:
        self.df = _df

        self.df.set_index("Date", inplace=True)
        self.df = self.df.sort_index(ascending=True)


    def calc(self):
        price = self.df['Close']

        # sma
        self.df['ma20']  = calc_sma(price, 20)
        self.df['ma50']  = calc_sma(price, 50)
        self.df['ma200'] = calc_sma(price, 200)

        # vma
        vol = self.df['Volume']
        self.df['vma50'] = calc_sma(vol, 50)

        # macd
        diff, dea, macd = calc_macd(price)
        self.df['macd'] = macd
        self.df['diff'] = diff
        self.df['dea'] = dea

        return self.df.dropna()

def calc_sma(_sc, _n):
    return _sc.rolling(_n).mean()

def calc_macd(_sc):
    # Get the 26-day EMA of the closing price
    k = _sc.ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = _sc.ewm(span=26, adjust=False, min_periods=26).mean()

    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d

    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()

    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = 2 * (macd - macd_s)

    return macd, macd_s, macd_h # diff, dea, macd

if __name__ == "__main__":
    data_center = DataCenter()
    df = data_center.one("IONQ")
    pd.set_option('display.max_columns', None)
    df = Tech(df).calc()
    print(df)
