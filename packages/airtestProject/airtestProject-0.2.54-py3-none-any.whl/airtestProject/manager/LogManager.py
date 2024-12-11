import logging
import os
import time
import traceback

import six
from airtestProject.airtest.aircv import aircv
from airtestProject.airtest.core.helper import G
from airtestProject.airtest.utils.logger import get_logger
from airtestProject.airtest.utils.logwraper import AirtestLogger
from loguru import logger
from functools import wraps

# 设置airtest日志等级，debug会输出很多日志
air_logger = logging.getLogger("airtest")
air_logger.setLevel(logging.ERROR)


class LogManager():
    def __init__(self, logfile, log_file="all.txt", project=None):
        self.LOGGER = AirtestLogger(logfile)
        if project is not None:
            self.log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + f"\\log\\{project}"
            self.log_file = os.path.join(self.log_dir, log_file)
            self.setup_logger()
            self.handler = None
        self.save_image = False
        self.project = project

    def setup_logger(self):
        logger.remove()
        self.handler = logger.add(self.log_file, rotation="10 MB", backtrace=True, diagnose=True)

    def close_logger(self):
        if self.handler is not None:
            logger.remove(self.handler)
            self.handler = None

    def log_step(self, message):
        """
        步骤日志，用来标记测试用例中每个步骤的记录日志，日志级别是info级别，便于问题跟踪与定位
        :param message:日志消息内容
        :return:None
        """
        self.log(arg=message, timestamp=time.time(), snapshot=True)
        logger.info(message)

    def log_error(self, message):
        """
        错误日志，用来标记报错时的日志，日志等级是error级别
        :param message: 日志消息内容
        :return:
        """
        self.log(arg=message, timestamp=time.time(), snapshot=False)
        logger.error(message)

    @staticmethod
    def log_assertion(assertion, expected, actual):
        """
        断言日志，用例标记断言过程的日志，日志等级为info级别
        :param assertion:true/flase,表示是否需要断言的标记
        :param expected:期望值
        :param actual:实际值
        :return:无返回
        """
        if assertion:
            logger.info(f"断言通过: 期望值 - {expected}, 实际值 - {actual}")
        else:
            logger.error(f"断言失败: 期望值 - {expected}, 实际值 - {actual}")

    def log_subprocess(self, function_name, *args, **kwargs):
        """
        记录执行子流程的日志，用于跟踪自动化执行过程中的子流程信息。日志等级为DEBUG级别。
        :param function_name: str，子流程的函数名。
        :param args: tuple，传递给子流程函数的位置参数。
        :param kwargs: dict，传递给子流程函数的关键字参数。
        :return: None
        """
        self.log(arg=f"执行子流程: {function_name} 使用参数: {args}, kwargs: {kwargs}", timestamp=time.time())
        logger.debug(f"执行子流程: {function_name} 使用参数: {args}, kwargs: {kwargs}")

    def log(self, arg, timestamp=None, desc="", snapshot=False):
        """
        记录日志
        :param arg: log信息或者异常对象。
        :param snapshot: 是否截图。
        :param desc: int，日志描述、默认是arg.class.__name__。
        :param timestamp: 默认是time.time()，记录时间戳。
        """
        depth = 0
        screen_data = None
        if snapshot:
            # 如果指定了snapshot参数，强制保存一张图片
            self.save_image = True
            try:
                screen_data = self.try_log_screen()
                depth = 2
            except AttributeError:
                # if G.DEVICE is None
                pass
            else:
                depth = 1
            finally:
                self.save_image = False
        if isinstance(arg, Exception):
            if hasattr(arg, "__traceback__"):
                # in PY3, arg.__traceback__ is traceback object
                trace_msg = ''.join(traceback.format_exception(type(arg), arg, arg.__traceback__))
            else:
                trace_msg = arg.message  # PY2
            AirtestLogger.log("info", {
                "name": desc or arg.__class__.__name__,
            }, depth=depth, timestamp=timestamp)
            get_logger("airtest.core.api").error(trace_msg)
        elif isinstance(arg, six.string_types):
            # 普通文本log内容放在"log"里，如果有trace内容放在"traceback"里
            # 在报告中，假如"traceback"有内容，将会被识别为报错，这个步骤会被判定为不通过
            self.LOGGER.log("info", {"name": desc or arg, "traceback": None, "ret": screen_data ,"log": arg}, depth=depth,
                            timestamp=timestamp)
            get_logger("airtest.core.api").info(arg)
        else:
            # arg['ret'] = screen_data

            self.LOGGER.log("info",
                            {"name": desc or repr(arg), "traceback": None, "log": repr(arg), "ret": screen_data},
                            depth=depth,
                            timestamp=timestamp)
            get_logger("airtest.core.api").info(repr(arg))

    def try_log_screen(self, screen=None, quality=None, max_size=None):
        """
        Save screenshot to file

        Args:
            screen: screenshot to be saved
            quality: The image quality, default is ST.SNAPSHOT_QUALITY
            max_size: the maximum size of the picture, e.g 1200

        Returns:
            {"screen": filename, "resolution": aircv.get_resolution(screen)}

        """
        if not self.log_dir or not self.save_image:
            return
        if not quality:
            quality = 10
        if not max_size:
            max_size = 600
        if screen is None:
            screen = G.DEVICE.snapshot(quality=quality)
        filename = "%(time)d.jpg" % {'time': time.time() * 1000}
        filepath = os.path.join(self.log_dir, filename)
        if screen is not None:
            aircv.imwrite(filepath, screen, quality, max_size=max_size)
            print({"screen": filename, "resolution": aircv.get_resolution(screen)})
            return {"screen": filename, "resolution": aircv.get_resolution(screen)}
        return None



def catch_error(func):
    """
    装饰器: 打印报错、通知
    """
    @wraps(func)  # 保持原函数的名称和文档字符串
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:

            logger.error(traceback.format_exc())
    return wrapper
