import logging
import json

with open('Setting.json','r') as f:
    u = json.load(f)
    CLASSCODE = u['CLASSCODE']
#     USERNAME = u['USERNAME']
#     PASSWORD = u['PASSWORD']

USERNAME = 'D0848081'
PASSWORD = 'JIMMYx134679x'
# CLASSCODE = ["3165","3166"]

LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s | %(levelname)-7s | %(filename)s  [line:%(lineno)d] - %(message)s'
#LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y%m%d %H:%M:%S'
LOG_FILENAME = "log.log"