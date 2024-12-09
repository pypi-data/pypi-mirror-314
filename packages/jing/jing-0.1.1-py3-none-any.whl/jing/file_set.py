#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import glob
import pandas
import os
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

dirMap = {'cn':'ak',
            'bn':'bn',
            'BN':'bn',
            'us':'yf'}

class FileSet:
    def __init__(self, _market='us') -> None:
        self.dir_path = "%s/data" % (os.getenv('PHOME')) ## TODO: get from config
        self.market = _market

        if os.path.isdir(self.dir_path):
            pass
        else:
            raise IsADirectoryError

    def fetch(self, _id, _date="", _market="us"):
        if len(_market) > 0:
            self.market = _market

        sub = dirMap.get(self.market, 'no')
        if sub == 'no':
            return None

        file_path = f"{self.dir_path}/{sub}/{_id}.csv"
        df = pd.read_csv(file_path)
        if len(_date) > 0:
            df = df[df['Date'] <= _date]
        return df
    def list(self, _market="us"):
        if len(_market) > 0:
            self.market = _market

        sub = dirMap.get(self.market, 'no')
        if sub == 'no':
            return None

        bsDir = "%s/%s" % (self.dir_path, sub)
        os.chdir(bsDir)

        pattern = "*.csv"
        fileList = glob.glob(pattern)

        df = pd.DataFrame(fileList, columns=["FileName"])
        df["code"] = df["FileName"].str[:-4]
        return df
        

if __name__ == "__main__":
    fs = FileSet()
    df = fs.fetch('IONQ', '2024-11-20', 'us')
    print(df)
    print(fs.list())

