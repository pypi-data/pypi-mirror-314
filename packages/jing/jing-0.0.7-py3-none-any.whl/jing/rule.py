#!/usr/bin/env python
# -*- encoding: utf8 -*-

import pandas as pd
from abc import ABC, abstractmethod

import warnings
warnings.filterwarnings("ignore")

from jing.trend import Trend
from jing.y import Y

pd.set_option('display.max_columns', None)

class Rule(ABC):
    @abstractmethod
    def run(self):
        pass

class RuleMa50Ma200(Rule):
    def __init__(self, _code, _ref) -> None:
        self.code = _code
        self.ref  = _ref
        self.name = self.__class__.__name__

    def run(self):
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        print(f"{code} {dt} len: {ref.len()}")

        # Rule1: break up ma50
        if ref.close(0) > ref.ma50(0) and ref.close(1) < ref.ma50(1):
            print(f"[{code}][{dt}] break up ma50, nice")
            pass
        else:
            print(f"[{code}][{dt}] not break up ma50, bye")
            #logger.debug(ref.df.head(5))
            return

        # Rule2: ma200 ascending many days!
        trend = Trend()
        per, rate = trend.ascendPercentile(ref.Ma200())
        #logger.debug("[%s] ma200: per: %s, rate: %s", code, per, rate)
        if per >= 98 and rate > 20:
            print(f"[{code}][{dt}] ma200 asceding[{per}, {rate}], nice")
            pass
        else:
            print(f"[{code}][{dt}] ma200 not asceding[{per},{rate}], bye")
            return

        # Rule3: ma50 is always upper than ma200
        per, rate, start = trend.ascendCross(ref.Ma50(), ref.Ma200())
        #logger.debug("[%s] ma50 : per: %s, rate: %s, start: %s", code, per, rate, start)
        if per >= 98 and rate > 25:
            print(f"[{code}][{dt}] ma50 keeps upper[{per}, {rate}], nice")
        else:
            print(f"[{code}][{dt}] ma50 not keeps uppers[{per}, {rate}], bye")
            return

        # Rule4: ma50 is not far away from ma200
        rate = 100 * (ref.ma50(0) / ref.ma200(0) - 1)
        #logger.debug("[%s] near: rate: %s", code, rate)
        # Rate:
        # - NFLX: 5.7%
        # - AMD: 5.7
        if rate > 2 and rate < 15:
            print(f"[{code}][{dt}] ma50 is near to ma200 [{rate}], nice")
        else:
            print(f"[{code}][{dt}] ma50 is not near to ma200 [{rate}], bye")
            return

        # Rule5: close-price once is near to ma200
        n = 50
        minRate = trend.approach(ref.Close(), ref.Ma200(), n)
        if minRate < 10 and minRate > -10:
            print(f"[{code}][{dt}] close is near to ma200 [{minRate}], nice")
        else:
            print(f"[{code}][{dt}] close is not near to ma200[{minRate}], bye")
            return

        print(f"[{code}][{dt}] ruleMa50Ma200 bingo", code, dt)


class RulePriceBreakout(Rule):
    def __init__(self, _code, _ref) -> None:
        self.code = _code
        self.ref  = _ref
        self.name = self.__class__.__name__

    def run(self):
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        print(f"[{code}][{dt}] len: %d", code, dt, ref.len())

        # Rule0: rate & vr
        rate = 100 * (ref.close(0) / ref.close(1) - 1)
        vr   = ref.vol(0) / ref.vma50(0)
        if rate >= 9 and vr >= 4:
            print(f"[{code}][{dt}] rate[{rate}], vr[{vr}], nice")
            pass
        else:
            print(f"[{code}][{dt}] rate[{rate}], vr[{vr}] doesn't match, bye")
            return

        trend = Trend()
        # Rule1: price breakout
        n = 200
        b = trend.breakout(ref.Close(), n)
        if b:
            print(f"[{code}][{dt}] breakout {n} days, nice")
            pass
        else:
            print(f"[{code}][{dt}] not breakout")
            return

        # Rule2: close is near to ma200
        n = 50
        near = trend.approach(ref.Close(), ref.Ma200(), n)
        if near < 20:
            print(f"[{code}][{dt}] approaching[{near}], nice")
        else:
            print(f"[{code}][{dt}] approaching")
            return

        # Rule3: ma200 ascending many days!
        trend = Trend()
        per, rate = trend.ascendPercentile(ref.Ma200())
        #logger.debug("[%s] ma200: per: %s, rate: %s", code, per, rate)
        if per >= 99 and rate > 20:
            print(f"[{code}][{dt}] ma200 asceding[{per}, {rate}], nice")
            pass
        else:
            print(f"[{code}][{dt}] ma200 not asceding[{per}, {rate}], bye")
            return

        # Rule4: ma50 is always upper than ma200
        per, rate, start = trend.ascendCross(ref.Ma50(), ref.Ma200())
        #logger.debug("[%s] ma50 : per: %s, rate: %s, start: %s", code, per, rate, start)
        if per >= 99 and rate > 25:
            print(f"[{code}][{dt}] ma50 keeps upper[{per}, {rate}], nice")
        else:
            print(f"[{code}][{dt}] ma50 not keeps uppers[{per}, {rate}], bye")
            return

        # Rule5: ma50 is not far away from ma200
        rate = 100 * (ref.ma50(0) / ref.ma200(0) - 1)
        if rate > 2 and rate < 20:
            print(f"[{code}][{dt}] ma50 is near to ma200 [{rate}], nice")
        else:
            print(f"[{code}][{dt}] ma50 is not near to ma200 [{rate}], bye")
            return

        print(f"[{code}][{dt}] rulePriceBreakout bingo")


class RuleVolumeBreakout(Rule):
    def __init__(self, _code, _ref) -> None:
        self.code = _code
        self.ref  = _ref
        self.name = self.__class__.__name__

    def run(self):
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        print(f"[{code}][{dt}] len: {ref.len()}")

        # Rule1: rate & vr
        rate = 100 * (ref.close(0) / ref.close(1) - 1)
        vr   = ref.vol(0) / ref.vma50(0)
        if rate >= 30 and vr >= 6:
            print(f"[{code}][{dt}] rate[{rate}], vr[{vr}], nice")
            pass
        else:
            print(f"[{code}][{dt}] rate[{rate}], vr[{vr}] doesn't match, bye")
            return

        trend = Trend()
        # Rule2: price breakout
        n = 50
        b = trend.breakout(ref.Close(), n)
        if b:
            print(f"[{code}][{dt}] breakout {n} days, nice")
            pass
        else:
            print(f"[{code}][{dt}] not breakout")
            return

        # Rule3: close was near to ma200
        n = 50
        near = trend.approach(ref.Close(), ref.Ma200(), n)
        if near < 20:
            print(f"[{code}][{dt}] approaching[{near}], nice")
        else:
            print(f"[{code}][{dt}] approaching")
            return

        # Rule3: ma200 ascending many days!
        trend = Trend()
        per, rate = trend.ascendPercentile(ref.Ma200(), 50)
        #logger.debug("[%s] ma200: per: %s, rate: %s", code, per, rate)
        if per >= 90 and rate > 5:
            print(f"[{code}][{dt}] ma200 asceding[{per}, {rate}], nice")
            pass
        else:
            print(f"[{code}][{dt}] ma200 not asceding[{per}, {rate}], bye")
            return

        # Rule4: ma50 is always upper than ma200
        per, rate, start = trend.ascendCross(ref.Ma50(), ref.Ma200(), 100, 50)
        #logger.debug("[%s] ma50 : per: %s, rate: %s, start: %s", code, per, rate, start)
        if per >= 99 and rate > 5:
            print(f"[{code}][{dt}] ma50 keeps upper[{per}, {rate}], nice")
        else:
            print(f"[{code}][{dt}] ma50 not keeps uppers[{per}, {rate}], bye")
            return

        # Rule5: ma50 is not far away from ma200
        rate = 100 * (ref.ma50(0) / ref.ma200(0) - 1)
        if rate > 2 and rate < 20:
            print(f"[{code}][{dt}] ma50 is near to ma200 [{rate}], nice")
        else:
            print(f"[{code}][{dt}] ma50 is not near to ma200 [{rate}], bye")
            return

        print(f"[{code}][{dt}] ruleVolumeBreakout bingo")

class RuleSimple(Rule):
    def __init__(self, _code, _ref) -> None:
        self.code = _code
        self.ref  = _ref
        self.name = self.__class__.__name__

    def run(self):
        code = self.code
        ref = self.ref
        dt = ref.date(0)

        print(f"[{code}][{dt}] len: {ref.len()}")

        # Rule1: rate & vr
        rate = 100 * (ref.close(0) / ref.close(1) - 1)
        vr   = ref.vol(0) / ref.vma50(0)
        if rate >= 20 and vr >= 8:
            print(f"[{code}][{dt}] rate[{rate}], vr[{vr}], nice")
            pass
        else:
            print(f"[{code}][{dt}] rate[{rate}], vr[{vr}] doesn't match, bye")
            return

        print(f"[{code}][{dt}] RuleSimple bingo")


if __name__=="__main__":
    code = "IONQ"
    date = '2024-09-27'

    y = Y("IONQ", _date=date)
    ref = y.ref

    rule = RuleSimple(code, ref)
    rule.run()

