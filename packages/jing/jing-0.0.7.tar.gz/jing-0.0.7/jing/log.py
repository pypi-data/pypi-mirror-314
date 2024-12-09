#!/usr/bin/python
# -*- encoding: utf8 -*-

import logging
import logging.handlers
import os
import sys

sai_dft_log = "sai.log"
sai_dft_fmt = "%(asctime)s - %(filename)s:%(lineno)s - %(message)s"
sai_dft_tm  = "%m-%d %H:%M:%S"
sai_dft_path= os.environ['LOG'] + '/'
#fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

g_logger = logging.getLogger(sai_dft_path+"sai.log")

def getLogger():
    return g_logger

def initLogger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not name:
        name = sai_dft_log

    # new
    fm=logging.Formatter(sai_dft_fmt, sai_dft_tm)
    rh=logging.handlers.TimedRotatingFileHandler(sai_dft_path+name, 'D')
    rh.setFormatter(fm)
    logger.addHandler(rh)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    global g_logger
    g_logger = logger
    return logger

def loggerStdout():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


if __name__ == "__main__":
    initLogger("x.log")
    logger = getLogger()

    # loggerStdout()
    logger.debug("hello debug 2")
    logger.info("hello info 2")
