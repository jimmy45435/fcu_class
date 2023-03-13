import logging
import json

USERNAME = 'D0000000'
PASSWORD = ''
CLASSCODE = ["2222"]  # ['1111','3333',....]

token = '' #line 權杖 功能:通知搶課

LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s | %(levelname)-7s | %(filename)s  [line:%(lineno)d] - %(message)s'
#LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y%m%d %H:%M:%S'
LOG_FILENAME = "log.log"