#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from jing.data_center import DataCenter
from jing.reference import Reference

class Trend:
    def __init__(self) -> None:
        self.step = 20
        pass

    def ascendPercentile(self, _ma200, _limit=120):
        up = 0
        down = 0
        length = len(_ma200)
        n = 0
        for i, v in _ma200.items():
            # recent X days
            if n >= _limit:
                break

            # incase overflow
            k = n + self.step
            if k >= length:
                break

            if v >= _ma200.iloc[k]:
                up += 1
            else:
                down += 1

            n += 1 

        n = up + down
        percentile = 100.00 * (up / n)
        rate = 100.00 * (_ma200.iloc[0] / _ma200.iloc[n-1] - 1)
        return percentile, rate

    # cross:
    # - ma50, short
    # - ma200, long
    def ascendCross(self, _ma50, _ma200, _cross=200, _upLimit=100):
        up = 0
        down = 0
        length = len(_ma200)
        n = 0
        shortUp = 0
        start = ""
        for i, v in _ma200.items():

            # recent X days
            if n >= _cross:
                break

            if _ma50[i] < _ma200.loc[i]:
                start = i
                break

            if _ma50.loc[i] > _ma200.loc[i]:
                shortUp += 1

            n += 1

        if shortUp < _upLimit:
            print("shortUp", shortUp)
            return 0, 0, '2024-01-01'

        percentile = 100.00 * (shortUp / n)
        rate = 100.00 * (_ma50.iloc[0] / _ma50.iloc[n-1] - 1)
        return percentile, rate, start

    # price breakout recent n days
    def breakout(self, _close, _n):
        this = _close.iloc[0]
        prev  = _close.iloc[1]
        maxPrice = _close[1:_n].max()
        # print("price: ", this)
        # print("prev: ", prev)
        # print("max: ", maxPrice)
        v = this > maxPrice and prev < maxPrice
        return v

    def approach(self, _close, _ma200, _n):
        close = _close[:_n]
        ma200 = _ma200[:_n]
        rate = 100 * (close / ma200 - 1)
        minRate = rate.min()
        # print("min rate: %s", minRate)
        return minRate

if __name__ == "__main__":
    data_center = DataCenter()
    df = data_center.csv("SMCI", '2024-01-19')
    print(df)
    ref = Reference(df)
    ma50 = ref.Ma50()
    ma200 = ref.Ma200()
    close = ref.Close()
    trend = Trend()
    per, rate = trend.ascendPercentile(ma200)
    print("trend", per, rate)
    # model = trend.linear(ma200)
    # print(model.summary())

    per, rate, start = trend.ascendCross(ma50, ma200)
    print("cross", per, rate, start)

    trend.breakout(close, 200)
    trend.approach(close, ma200, 50)
