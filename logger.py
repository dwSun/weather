#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers


class Singleton(type):
    '''
    Dark Magic
    Class meta as Singleton will have only one instance forever.
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger():
    __metaclass__ = Singleton
    def __init__(self):
        '''
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        '''
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

        # 创建一个logger
        self.logger = logging.getLogger('weather')
        self.logger.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

    def trace(self, label=""):
        def handle_func(func):
            def handle_args(*args, **kwargs):
                self.logger.debug('{1} {0} start...'.format(func.__name__,label))

                res = func(*args, **kwargs)

                self.logger.debug('{1} {0} end...'.format(func.__name__,label))
                return res
            return handle_args
        return handle_func


if __name__ == '__main__':
    logger = Logger(logpath='log.log').getlog()
    logger.error('cc')
