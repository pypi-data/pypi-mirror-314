"""
日志工具
"""
import random
import subprocess

import loguru
from typing import Callable

import functools
import time
import sys
import os

import logging

from airtestProject.commons.Listen.listen import tag_listener
from airtestProject.commons.utils.tools import log_error

# 设置airtest日志等级，debug会输出很多日志
air_logger = logging.getLogger("airtest")
air_logger.setLevel(logging.ERROR)


class Logger:
    """
    通过单例模式，只实例化一个日志对象
    直接调用log实例对象进行日志调用
    """

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, '_instance'):
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        添加日志记录器，写入文件
        日志分类型存储，一份完整日志，一份错误日志
        通过读取配置文件中的 IS_WRITE 判断是否需要写入文件，便于调试
        """

        self.logger = loguru.logger
        date = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(time.time()))
        self.adb_log = None

        # if OUTPUT:
        #     all_log_path = os.path.join(REPORT_DIR, "all.log")
        #     self.logger.add(
        #         all_log_path,  # 日志存放位置
        #         retention=7,  # 清理周期
        #         level="DEBUG",  # 日志级别
        #         enqueue=True,  # 具有使日志记录调用非阻塞的优点
        #         encoding="utf-8",
        #         format=LOG_FORMAT
        #     )
        #     error_log_path = os.path.join(REPORT_DIR, "error.log")
        #     self.logger.add(
        #         error_log_path,
        #         retention=7,
        #         level="ERROR",
        #         enqueue=True,
        #         encoding="utf-8",
        #         format=LOG_FORMAT
        #     )

    def get_logger(self):
        return self.logger

    def random_emoji(self):
        emoji = '🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍑🍒🍓🥝🍅🥥🥑🍆🥔🥕🌽🥒🥬🥦🧄🧅🍄🎃🎄🎆🎇🧨✨🎈🎉🎊🎋🎍🎎🎏🍖🍗🥩🥓🍔🍟🍕'
        return random.choice(emoji)

    def step(self, msg):
        self.logger.info(f'{" ".join(self.random_emoji() * 2)} ：{msg}')

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warn(self, msg):
        self.logger.warning(f'{" ".join(self.random_emoji() * 2)} ：{msg}')

    def error(self, msg):
        self.logger.error(f'😈 😈 ：{msg}')

    def test(self, msg):
        from airtestProject.airtest.core import api as air
        self.logger.info(f'{" ".join(self.random_emoji() * 2)} ：{msg}')
        air.log(f'{" ".join(self.random_emoji() * 2)} ：{msg}')

    def wrap(self, msg: str = None) -> Callable:
        from airtestProject.airtest.core import api as air
        """
        函数日志装饰器
        :param msg: 消息内容
        :return:
        """

        def wrapper(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                start_time = time.time()
                try:
                    res = func(*args, **kwargs)
                    end_time = time.time()
                    duration = round(end_time - start_time, 2)
                    self.step(f"{msg} - func: {func.__name__} - duration: {duration} s")
                    if self.adb_log is not None and ("Unity" or "CRASH" in self.adb_log):
                        log_error(self.adb_log,
                                       desc=f":😈 😈 {msg} - func: {func.__name__}",
                                       snapshot=True, start_time=start_time, end_time=end_time)
                    elif tag_listener.tag == -1:
                        log_error("疑似资源缺失，检查上面步骤中的画面",
                                       desc=f":😈 😈 {msg} - func: {func.__name__}",
                                       snapshot=True, start_time=start_time, end_time=end_time)
                    else:
                        air.log(f"{' '.join(self.random_emoji() * 2)}: {msg} - func: {func.__name__}", snapshot=True)
                    self.adb_log = None
                    return res
                except Exception as e:
                    air.log(e, desc=f"😈 😈  : {msg} - func: {func.__name__}", snapshot=True)
                    return func

            return inner

        return wrapper

    def log_adb_out(self, adb_log):
        self.adb_log = adb_log

    def tag(self, msg: str = None) -> Callable:
        """
        函数日志装饰器
        :param msg: 消息内容
        :return:
        """

        def tag_wrapper(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                start_time = time.time()
                res = func(*args, **kwargs)
                end_time = time.time()
                duration = round(end_time - start_time, 2)
                self.step(f"{msg} - func: {func.__name__} - duration: {duration} s")
                return res

            return inner

        return tag_wrapper

    def case(self, func: Callable[[str], str]) -> Callable:
        """
        测试用例日志装饰器
        :param func: 用例函数对象
        :return:
        """

        @functools.wraps(func)
        def inner(*args, **kwargs):
            self.step(f"Start running testcase: {func.__name__}")
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.step(f"End running testcase : {func.__name__} [ Case duration: {duration} s ]")
            self.step(f"{'- ' * 16} 分割线 {' -' * 16}")
            return res

        return inner


log = Logger()

if __name__ == '__main__':
    log.info('aaaa')
    log.error('aaaa')
    log.warn('aaaa')
    log.step('aaaa')


    @log.case
    def test():
        log.debug(111)


    test()
