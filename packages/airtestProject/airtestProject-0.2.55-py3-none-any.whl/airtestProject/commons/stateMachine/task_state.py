import logging
import re
import time
import traceback
from abc import ABC, abstractmethod
import asyncio
from concurrent.futures import ThreadPoolExecutor

from airtestProject.commons.stateMachine.task import Task
from airtestProject.commons.utils.tools import log_error, log_normal
from airtestProject.factory.OperateFactory import operate
from airtestProject.solox.public.apm import AppPerformanceMonitor
from airtestProject.commons.utils.logger import log

logger_error = logging.getLogger("State")
"""
状态机状态类
"""
ADB_LOG_LEVE_DICT = {
    "INFO": "logcat -d Unity:I AndroidRuntime:E CRASH:* *:S",
    "DEBUG": "logcat -d Unity:D AndroidRuntime:E CRASH:* *:S",
    "WARNING": "logcat -d Unity:W AndroidRuntime:E CRASH:* *:S",
    "ERROR": "logcat -d Unity:E AndroidRuntime:E CRASH:* *:S"
}


class State(ABC):

    def __init__(self, TaskMachine):
        self.TaskMachine = TaskMachine
        self.test_case = None

    @abstractmethod
    def run(self, test_case: Task):
        pass

    @abstractmethod
    def next_state(self):
        pass


class TestPreparation(State):
    def run(self, test_case):
        log.step(f"任务准备，任务：{test_case.task_name}")

        def perform_profile_task():
            log.info("性能测试初始化")
            this_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(this_loop)
            if self.TaskMachine.apm is None:
                self.TaskMachine.apm = AppPerformanceMonitor(script_name=self.TaskMachine.file_path,
                                                             pkgName=self.TaskMachine.apk_name,
                                                             platform='Android',
                                                             deviceId=self.TaskMachine.adb.serialno,
                                                             surfaceview=True,
                                                             noLog=False, pid=None, collect_all=True,
                                                             duration=0)
                this_loop.run_until_complete(self.TaskMachine.apm.collectAll(test_case.is_profile))

        # TODO 后续接入性能测试
        if self.TaskMachine.adb is not None:
            log.step("测试准备" + "设备id" + self.TaskMachine.adb.serialno)
            if self.TaskMachine.profile_on:
                if self.TaskMachine.executor is None and test_case.is_profile is True:
                    self.TaskMachine.executor = ThreadPoolExecutor(max_workers=1)
                    self.TaskMachine.executor.submit(perform_profile_task)
                elif self.TaskMachine.apm is not None and test_case.is_profile is False:
                    log.step("性能采集结束")
                    self.TaskMachine.loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.TaskMachine.loop)
                    self.TaskMachine.profile_report.append(
                        self.TaskMachine.loop.run_until_complete(self.TaskMachine.apm.collectAll(test_case.is_profile)))
                    # asyncio.run(self.TaskMachine.apm.collectAll(test_case.is_profile))
                    self.TaskMachine.executor = None
                    self.TaskMachine.apm = None
                    self.TaskMachine.loop.close()
                    self.TaskMachine.loop = None
            else:
                log.step("uwa模式不启动solox")
        if test_case.is_recording and self.TaskMachine.recorder is not None and self.TaskMachine.log_dir is not None:
            self.TaskMachine.recorder.start_recording()

    def next_state(self):
        return StartTest(self.TaskMachine)


class StartTest(State):

    def run(self, test_case):
        log.step("开始测试")
        self.test_case = test_case
        if self.TaskMachine.adb is not None:
            self.TaskMachine.adb.shell("logcat -c")
        test_case.start_time = time.time()
        test_case.run()
        if self.TaskMachine.adb is not None:
            test_case.adb_log = self.TaskMachine.adb.shell(ADB_LOG_LEVE_DICT.get(test_case.adb_log_leve))

    def next_state(self):
        if self.test_case.adb_log is not None and re.search(r'\bE\b', self.test_case.adb_log):
            return TaskException(self.TaskMachine)
        return TaskNormal(self.TaskMachine)


class TaskException(State):
    def __init__(self, TaskMachine):
        super().__init__(TaskMachine)
        self.exception = None
        self.exception_queue = None

    def set_exception(self, exception):
        self.exception = exception

    def set_exception_queue(self, exception_queue):
        self.exception_queue = exception_queue

    def run(self, test_case):
        log.step("测试异常")
        test_case.is_error = True
        test_case.end_time = time.time()
        e_message = "adb:" + "\n" + test_case.adb_log + "\n"
        if self.exception:
            # log.warn("怎么回事"+str(self.TaskMachine.error_num))
            trace_msg = ''.join(traceback.format_exception(type(self.exception), self.exception,
                                                           self.exception.__traceback__))
            self.TaskMachine.error_num += 1
            e_message = e_message + "ERROR:" + "\n" + trace_msg
            logger_error.error(trace_msg)
        if self.exception_queue:
            self.TaskMachine.error_queue_num += 1
            while not self.exception_queue.empty():
                exception_message = self.exception_queue.get()
                logger_error.error(exception_message)
        log_error(e_message,
                  desc=f":func: {test_case.task_name}",
                  snapshot=True, start_time=test_case.start_time, end_time=test_case.end_time)

    def next_state(self):
        return TaskEnd(self.TaskMachine)


class TaskNormal(State):
    def run(self, test_case):
        test_case.end_time = time.time()
        if test_case.adb_log != "":
            n_message = "adb:" + "\n" + test_case.adb_log + "\n"
            log_normal(n_message, desc=f"func: {test_case.task_name}",
                       snapshot=True, start_time=test_case.start_time, end_time=test_case.end_time)
        log_normal(f"func: {test_case.task_name}",
                   snapshot=True, start_time=test_case.start_time, end_time=test_case.end_time)
        log.step("测试正常")

    def next_state(self):
        return TaskEnd(self.TaskMachine)


class game_exceptions_handling(State):
    def run(self, test_case):
        print("woc需要处理想想怎么处理")
        pass

    def next_state(self):
        return TaskEnd(self.TaskMachine)


class TaskEnd(State):
    def run(self, test_case):
        if (self.TaskMachine.error_queue_num != 0 and
                self.TaskMachine.error_queue_num == self.TaskMachine.last_error_queue_num):
            self.TaskMachine.error_queue_num = 0
            self.TaskMachine.last_error_queue_num = 0
        self.test_case = test_case
        self.test_case.adb_log = ""
        if self.test_case.end_view is not None:
            log_normal("任务结束检查")
            flag = False
            for i in range(0, 3):
                if operate("air").exists(self.test_case.end_view):
                    log_normal("任务正常结束")
                    flag = True
                    break
            if flag is False:
                self.TaskMachine.sub_method_exception_thrown = True
                log_error("无法检查到任务结束点", desc="任务结束状态异常", snapshot=True)
        if self.test_case.is_recording:
            try:
                self.TaskMachine.recorder.stop_recording(
                    output=self.TaskMachine.log_dir + r"\任务视频{}.mp4".format(test_case.task_name))
            except Exception as e:
                log.error(f"停止视频失败：{e}")
        if self.TaskMachine.error_queue_num > self.TaskMachine.last_error_queue_num:
            self.TaskMachine.last_error_queue_num = self.TaskMachine.error_queue_num
        log.step("测试结束")

    def next_state(self):
        if self.test_case.run_again_num != 0:
            self.test_case.run_again_num = self.test_case.run_again_num - 1
            return StartTest(self.TaskMachine)
        return None
