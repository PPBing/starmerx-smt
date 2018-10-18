#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import logging.handlers
reload(sys)
sys.setdefaultencoding('utf-8')


LOG_CONFIG = {
    "level": logging.INFO,
    "format": '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
    "datefmt": '%Y-%m-%d %H:%M:%S',
}


class Logger(object):

    def __init__(self,
                 level=LOG_CONFIG['level'],
                 formats=LOG_CONFIG['format'],
                 datefmt=LOG_CONFIG['datefmt']
                 ):
        self.level = level
        self.filename = os.path.dirname(os.getcwd()) + '/Logs/' + 'log'
        self.format = formats
        self.datefmt = datefmt
        # 实例化logger对象
        self._logger = logging.getLogger()
        # 指定日志输出格式
        if not self._logger.handlers:
            self.formatter = logging.Formatter(fmt=self.format, datefmt=self.datefmt)
            # 给logger添加文件日志处理器
            self._logger.addHandler(self.get_file_handler(self.filename))
            # 指定日志的最低输出级别，
            self._logger.setLevel(self.level)

    def get_file_handler(self, log_name):
        # 文件处理器
        # 日志名字
        fh = logging.handlers.TimedRotatingFileHandler(
            log_name, 'midnight', 1, 0)
        fh.suffix = '%Y%m%d'
        # 指定log的输出形式，通过控制台的setFormatter方法来实现
        fh.setFormatter(self.formatter)
        return fh

    @property
    def logger(self):
        return self._logger