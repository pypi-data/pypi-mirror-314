#!/usr/bin/env python
# -*- encoding: utf8 -*-

import os
import json

class Config:
    def __init__(self) -> None:
        self.config = self.load()

    def get(self, _section, _key):
        if _section in self.config:
            if _key in self.config[_section]:
                val = self.config[_section][_key]
                return val
            else:
                pass
        else:
            pass

        return ""

    def load(self):
        path = "%s/.local/sai.json" % os.getenv('HOME')
        if os.path.isfile(path):
            fd = open(path)
            return json.load(fd)
        else:
            raise NameError('error: path')

config = Config()

def GetMysqlHost():
    return config.get("mysql", "host")

if __name__=="__main__":
    print(GetMysqlHost())
