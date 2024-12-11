import asyncio
import inspect
import random
import queue
import sys
import threading
import traceback
import time
from functools import wraps

import airtestProject.airtest.core.android
from airtestProject.airtest.core.android import Android
from airtestProject.airtest.core.android.recorder import Recorder
from airtestProject.airtest.core.settings import Settings as ST
from airtestProject.commons.Listen.fps_listen import globalApmSubject, ApmListen
from airtestProject.commons.stateMachine.task import Task
from airtestProject.commons.stateMachine.task_state import TaskEnd, StartTest, TaskException, TaskNormal, TestPreparation
from airtestProject.airtest.core import api as air
from airtestProject.commons.utils.gotCommon import TestGot
from airtestProject.commons.utils.tools import log_normal, log_error
from airtestProject.manager.DeviceManager import DeviceManager
from airtestProject.commons.utils.logger import log

thread_local = threading.local()  # 确保exception_queue是每个线程独一份


class TaskMachine:
    def __init__(self, state_classes, adb, test_cases, apk_name, file_path, profile_on):
        self.state = None
        self.states = {state_class.__name__: state_class(self) for state_class in state_classes}
        self.adb = adb
        self.recorder = Recorder(self.adb) if self.adb is not None else None
        self.error_num = 0
        self.last_error_queue_num = 0
        self.error_queue_num = 0
        self.sub_method_exception_thrown = False
        self.test_cases = test_cases
        self.log_dir = ST.LOG_DIR
        self.apk_name = apk_name
        self.file_path = file_path
        self.apm = None
        self.executor = None   # 线程池 solox用
        self.loop = None
        self.profile_report = []
        self.apm_listen = ApmListen(callback=lambda msg, apm_type: log_error(
            f"{apm_type if apm_type else 'Fps'}异常,数据为{msg}", desc="apm数据异常", snapshot=True))
        self.profile_on = profile_on

    def run(self, error_num_out):
        globalApmSubject.add_listen(self.apm_listen)
        while not self.test_cases.empty():
            self.state = self.states['TestPreparation']  # 将状态设置为StartTest
            test_case = self.test_cases.get()
            if self.sub_method_exception_thrown:
                self.test_cases.queue.clear()
                break
            while self.state is not None:
                if self.error_num >= error_num_out or self.error_queue_num >= error_num_out:
                    self.test_cases.queue.clear()
                    break
                try:
                    self.state.run(test_case)
                    if not thread_local.exception_queue.empty():
                        self.state = self.states['TaskException']
                        self.state.set_exception_queue(thread_local.exception_queue)
                        self.state.run(test_case)
                    self.state = self.state.next_state()
                except Exception as e:
                    self.state = self.states['TaskException']
                    self.state.set_exception(e)
                    if not thread_local.exception_queue.empty():
                        self.state.set_exception_queue(thread_local.exception_queue)
                    self.state.run(test_case)
                    self.state.set_exception(None)
                    self.state.set_exception_queue(None)
                    self.state = self.state.next_state()
            if test_case.stop_Machine:
                self.test_cases.queue.clear()
        if self.apm is not None:
            log.info("采集任务强制结束")
            self.profile_report.append(asyncio.run(self.apm.collectAll(False)))
            self.apm = None
            self.executor = None
        globalApmSubject.remove_listen(self.apm_listen)


def put_task(func_out=None, adb_log_leve="ERROR", task_name=None,
             end_view=None, is_recording=False, is_profile=None, run_again_num=0, error_run_again_num=0,
             is_uwa_profile=False):
    """
    流程装饰器，提供更多的可选参数，如果想要状态更加丰富，报告生成更加易于理解，推荐使用。
    :param func_out: 这个千万不要传，这个是自动的，占位参数。
                也就是说后续的参数请用adb_log_leve=xx，这种形式进行传参
    :param adb_log_leve: 日志等级
        "INFO"
        "DEBUG"
        "WARNING"
        "ERROR"
    :param task_name: 任务名字
    :param end_view: 当前任务的结束点，也是下一个任务要成功运行的必要元素
    :param is_recording: 启用录屏
    :param is_profile: 如果为True,则在当前任务启用性能采集，如果为False则在当前任务关闭性能采集。可多次开启或关闭，会生成多份性能报告
    :param run_again_num: 当前方法任务重复次数默认不重复
    :param error_run_again_num: 当前方法报错后重复执行，感觉报错了之后重复多少有点多余了哈哈哈哈,未实现
    :param is_uwa_profile: 未实现
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self):
            func.only_run_this = False
            func.start_tag = False
            self.task_queue.put(Task(func, self, adb_log_leve, task_name,
                                     end_view, is_recording, is_profile,
                                     run_again_num,
                                     error_run_again_num=error_run_again_num, is_uwa_profile=is_uwa_profile))

        return wrapper

    if callable(func_out):
        return decorator(func_out)
    else:
        return decorator


def stop_machine_f(func):
    """
    流程装饰器，任务停止控制器, 执行完这个任务后停止
    """

    @wraps(func)
    def wrapper(self):
        func.only_run_this = False
        func.start_tag = False
        self.task_queue.put(Task(func, self, "ERROR", stop_Machine=True))

    return wrapper


def start_tag(func_out=None, adb_log_leve="ERROR", task_name=None,
              end_view=None, is_recording=False, is_profile=None, run_again_num=0):
    """
        从当前任务开始运行，可以给当前任务设定状态。
        :param func_out: 这个千万不要传，这个是自动的，占位参数。
                    也就是说后续的参数请用adb_log_leve=xx，这种形式进行传参
        :param adb_log_leve: 日志等级
            "INFO"
            "DEBUG"
            "WARNING"
            "ERROR"
        :param task_name: 任务名字
        :param end_view: 当前任务的结束点，也是下一个任务要成功运行的必要元素
        :param is_recording: 启用录屏
        :param is_profile: 启用性能采集
        :param run_again_num: 当前方法任务重复次数默认不重复
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self):
            func.only_run_this = False
            func.start_tag = True
            self.task_queue.queue.clear()
            self.task_queue.put(Task(func, self, adb_log_leve, task_name,
                                     end_view, is_recording, is_profile, run_again_num=run_again_num))

        return wrapper

    if callable(func_out):
        return decorator(func_out)
    else:
        return decorator


def only_run_this(func_out=None, adb_log_leve="ERROR", task_name=None,
                  end_view=None, is_recording=False, is_profile=None, run_again_num=0):
    """
        只运行当前任务，可以给当前任务设定状态。切记使用了这个装饰器后其他流程装饰器均不生效
        :param func_out: 这个千万不要传，这个是自动的，占位参数。
                    也就是说后续的参数请用adb_log_leve=xx，这种形式进行传参
        :param adb_log_leve: 日志等级
            "INFO"
            "DEBUG"
            "WARNING"
            "ERROR"
        :param task_name: 任务名字
        :param end_view: 当前任务的结束点，也是下一个任务要成功运行的必要元素
        :param is_recording: 启用录屏
        :param is_profile: 启用性能采集
        :param run_again_num: 当前方法任务重复次数默认不重复
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self):
            func.only_run_this = True
            func.start_tag = False
            self.task_queue.queue.clear()
            self.task_queue.put(Task(func, self, adb_log_leve, task_name,
                                     end_view, is_recording, is_profile, run_again_num=run_again_num))

        return wrapper

    if callable(func_out):
        return decorator(func_out)
    else:
        return decorator


def check_func(msg=None):
    """
    报错忽略装饰器
    :param msg: 你想在报告中显示的列表名
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                func(*args, **kwargs)
                end_time = time.time()
                duration = round(end_time - start_time, 2)
                log.step(f"{msg if isinstance(msg, str) else ''} - func: {func.__name__} - duration: {duration} s")
                log_normal(
                    f"{' '.join(random_emoji() * 2)}: {msg if isinstance(msg, str) else ''} - func: {func.__name__}",
                    snapshot=True, start_time=start_time, end_time=end_time)
            except Exception as e:
                end_time = time.time()
                trace_msg = ''.join(traceback.format_exception(type(e), e, e.__traceback__))  # 报错堆栈信息
                log_error(trace_msg, desc=f":😈 😈 {msg if isinstance(msg, str) else ''} - func: {func.__name__}",
                          snapshot=True, start_time=start_time, end_time=end_time)
                if hasattr(thread_local, 'exception_queue'):
                    # print(thread_local.exception_queue)
                    thread_local.exception_queue.put(trace_msg)
                else:
                    # 如果线程本地存储中没有 exception_queue，在思考要不要直接就不处理了，因为你没有exception_queue证明不是状态机启动的
                    new_queue = queue.Queue()
                    new_queue.put(trace_msg)
                    thread_local.exception_queue = new_queue

                return None

        return wrapper

    if callable(msg):
        return decorator(msg)
    else:
        return decorator


def random_emoji():
    emoji = '🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍑🍒🍓🥝🍅🥥🥑🍆🥔🥕🌽🥒🥬🥦🧄🧅🍄🎃🎄🎆🎇🧨✨🎈🎉🎊🎋🎍🎎🎏🍖🍗🥩🥓🍔🍟🍕'
    return random.choice(emoji)


class TaskRunner(object):
    """
    任务执行器
    """

    def __init__(self, task_cases):
        self.taskState = [TestPreparation, StartTest, TaskException, TaskNormal, TaskEnd]
        self.adb = None
        self.taskMachine = None
        self.apk_name = None
        self.file_path = None
        self.project_device = DeviceManager()
        self.task_cases = task_cases
        self.task_queue = queue.Queue()
        self.connection_method = None

    def setup_task_runner(self, file_path, device_ids=None, connection_method="local", apk_name=None, level=None):
        """

        :param apk_name: 包名
        :param file_path: 传个__file__进来就好
        :param device_ids: id列表例子[123456,123456]或者直接传一个id "123456"，不传则是默认
        :param connection_method: local用于正常运行,uwa用于在uwa上运行脚本
        :param level: 日志等级， TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL
        """

        self.file_path = file_path
        self.connection_method = connection_method
        if connection_method == "local":
            if level:
                log.logger.remove()
                log.logger.add(sys.stdout, level=level)
            self.project_device.auto_setup(file_path, device_ids, True)
        elif connection_method == "uwa":
            log.logger.remove()
            log.logger.add(sys.stdout,  level="ERROR")
            from airtestProject.manager.DeviceManager import uwa_auto_setup
            uwa_auto_setup()
        self.apk_name = apk_name

    def start_app(self, apk_name=None):
        got = TestGot()
        if self.apk_name is not None:
            got.got_init(self.apk_name)
        elif apk_name is not None:
            self.apk_name = apk_name
            got.got_init(apk_name)

    def run(self, error_num_out=3):
        if isinstance(self.task_cases, list) is False:
            self.task_cases = [self.task_cases]
        for task_case in self.task_cases:
            # print(type(air.device()))
            # 按照方法定义顺序获取所有方法
            methods = [(name, method) for name, method in task_case.__class__.__dict__.items() if
                       inspect.isfunction(method) and not (name.startswith('__') and name.endswith('__'))]
            # print(methods)
            for name, method in methods:
                # 检查方法是否使用了装饰器
                if hasattr(method, '__wrapped__'):
                    # print(method.__wrapped__)  # 被装饰器装饰后的方法会有一个__wrapped__，__wrapped__属性里面存的就是被装饰的方法，可以通过这段代码查看
                    getattr(task_case, name)()  # getattr(self, name)等价于self.name()但是name是个变量所以可以运行不同的方法
                    if method.__wrapped__.only_run_this:
                        # print("终止装载")
                        break
                    if method.__wrapped__.start_tag and self.task_queue.empty() is False:
                        self.task_queue.queue.clear()
                else:
                    task_case.task_queue.put(Task(method, task_case, adb_log_leve="ERROR"))  # 更适合中国宝宝体质
            self.task_queue.queue.extend(task_case.task_queue.queue)
        if hasattr(thread_local, 'exception_queue'):
            thread_local.exception_queue.queue.clear()
        else:
            thread_local.exception_queue = queue.Queue()
        profile_on = True
        if isinstance(air.device(), Android):
            self.adb = air.device().adb
        elif self.connection_method == "uwa":
            profile_on = False
            try:
                from airtest.core.android import Android as AD
                if isinstance(air.device(), AD):
                    self.adb = air.device().adb
            except Exception as e:
                log.error(f"UWA 模式出现问题: {e}")
                self.adb = None
        else:
            log.info("非安卓手机")
            self.adb = None
        self.taskMachine = TaskMachine(self.taskState, self.adb, self.task_queue, self.apk_name,
                                       self.file_path, profile_on)
        self.taskMachine.run(error_num_out)
        log.info("任务队列执行结束")

    def to_report(self):
        self.project_device.to_report(self.taskMachine.profile_report)

    def recycle(self):
        got = TestGot()
        got.stop_app(self.apk_name)


class TaskCaseTemplate:
    """
    目前的作用就是分离开来而已，后面有什么需要的再加吧
    所有的测试用例书写都继承这个类
    """

    def __init__(self):
        self.task_queue = queue.Queue()
