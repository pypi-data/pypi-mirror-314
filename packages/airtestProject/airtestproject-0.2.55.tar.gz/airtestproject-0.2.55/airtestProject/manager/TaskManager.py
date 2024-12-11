import time
from queue import Queue, Empty
from threading import Thread
from airtestProject.manager.TestCaseManager import TestCaseManager


class Task:
    def __init__(self, test_case, status="Free"):
        self.test_case = test_case
        self.status = status  # 任务状态：Pending, Running, Completed


class TaskManager:
    def __init__(self):
        self.task_queue = Queue()
        self.running_task = None
        self.statues = ["Running", "Free"]

    def add_task(self, test_case):
        task = Task(test_case)
        self.task_queue.put(task)

    def execute_tasks(self):
        while True:
            try:
                if self.running_task is None:
                    self.running_task = self.task_queue.get(block=False)
                    self.running_task.status = "Running"
                    # logger.info(f"Starting execution of test case: {self.running_task.test_case}")
                    # 模拟执行测试用例
                    time.sleep(3)
                    # 模拟异常处理
                    if self.running_task.test_case == "Test Case 2":
                        raise Exception("Test Case 2 failed")
                    self.running_task.status = "Completed"
                    # logger.info(f"Test case execution completed: {self.running_task.test_case}")
                    self.running_task = None
            except Empty:
                # 队列为空时退出循环
                break
            except Exception as e:
                # 异常处理
                # logger.error(f"Error occurred while executing test case: {self.running_task.test_case}, Error: {e}")
                self.running_task.status = "Failed"
                self.running_task = None
