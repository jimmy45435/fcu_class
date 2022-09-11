from asyncio.log import logger
import logging


USERNAME = 'D0848579'
PASSWORD = 'jAsOn0222'
CLASSCODE = ["3106","3124"]

LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s | %(levelname)-7s | %(filename)s  [line:%(lineno)d] - %(message)s'
#LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y%m%d %H:%M:%S'
LOG_FILENAME = "log.log"