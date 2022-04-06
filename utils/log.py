'''
記錄日誌的模塊
'''

import sys
#Python的標準日誌模塊：logging
import logging

from settings import LOG_LEVEL,LOG_FMT ,LOG_DATEFMT,LOG_FILENAME 

class Logger(object):

    def __init__(self):
        #獲取一個logger對象
        self._logger = logging.getLogger()
        #設置format對象
        self.formatter = logging.Formatter(fmt=LOG_FMT,datefmt=LOG_DATEFMT)
        #設置日誌輸出——文件日誌模式
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        #設置日誌輸出——終端日誌模式
        self._logger.addHandler(self._get_console_handler())
        # 4. 設置日誌等級
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        '''
        返回一個文件日誌handler
        '''
        # 獲取一個輸出爲文件日誌的handler
        filehandler = logging.FileHandler(filename=filename,encoding="utf-8")
        # 設置日誌格式
        filehandler.setFormatter(self.formatter)
        # 返回
        return filehandler

    def _get_console_handler(self):
        '''
        返回一個輸出到終端日誌handler
        '''
        #獲取一個輸出到終端的日誌handler
        console_handler = logging.StreamHandler(sys.stdout)
        #設置日誌格式
        console_handler.setFormatter(self.formatter)
        # 返回handler
        return console_handler

    #屬性裝飾器，返回一個logger對象
    @property
    def logger(self):
        return self._logger

# 初始化並配一個logger對象，達到單例
# 使用時，直接導入logger就可以使用
logger = Logger().logger

# if __name__ == '__main__':
#     print(logger)
#     logger.debug("調試信息")
#     logger.info("狀態信息")
#     logger.warning("警告信息")
#     logger.error("錯誤信息")
#     logger.critical("嚴重錯誤信息")