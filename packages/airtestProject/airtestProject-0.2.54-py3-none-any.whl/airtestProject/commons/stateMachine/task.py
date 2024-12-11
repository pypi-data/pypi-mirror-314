from asyncio import Queue, LifoQueue


class TaskQueue:
    """
    状态队列
    TODO:配合状态机控制任务轮换,后续换成这个队列来写，目前用不上
    """

    def __init__(self, num=50, lifo=False):
        self.queue = Queue(num) if not lifo else LifoQueue(num)

    def put_queue(self, key):
        """存测试方法"""
        try:
            if not self.check_queue(key):
                self.queue.put(key)
        except Exception as e:
            print(f"{key}队列异常{e}")

    def check_queue(self, key):
        """检查存入数据"""
        for i in range(self.queue.qsize()):
            task_key = self.queue.get()
            if task_key == key:
                self.queue.put(task_key)
                return True
            else:
                self.queue.put(task_key)
        return False

    def task_over(self, over_key):
        """销毁任务"""
        for i in range(self.queue.qsize()):
            task_key = self.queue.get()
            if task_key == over_key:
                return True
            else:
                self.queue.put(task_key)
        return False

    def get_task(self):
        """按照队列取数据"""
        if self.queue.empty():
            return False
        else:
            task = self.queue.get()
            return task

    def clear(self):
        for i in range(self.queue.qsize()):
            self.queue.get()


class Task(object):
    """
    Task包装类，用于储存方法信息
    """
    def __init__(self, func, instance, adb_log_leve, task_name=None, end_view=None,
                 is_recording=False, is_profile=None, run_again_num=0, stop_Machine=False, error_run_again_num=0,
                 is_uwa_profile=False):
        """

        :param func: 被包装的方法
        :param instance: 调用方法的实例
        :param adb_log_leve: adb等级
        :param task_name: 任务名
        :param end_view: 结束点
        :param is_recording: 录像
        :param is_profile: 性能采集
        :param run_again_num: 重新运行
        :param stop_Machine: 停止状态机
        :param error_run_again_num: 报错后重新运行
        :param is_uwa_profile: uwa性能
        is_error属于判定该任务是否报错
        """
        self.func = func
        self.instance = instance
        self.adb_log_leve = adb_log_leve
        self.task_name = task_name if task_name else func.__name__
        self.adb = None
        self.adb_log = ""
        self.start_time = None
        self.end_time = None
        self.end_view = end_view
        self.is_recording = is_recording
        self.is_profile = is_profile
        self.is_uwa_profile = is_uwa_profile
        self.run_again_num = run_again_num
        self.stop_Machine = stop_Machine
        self.error_run_again_num = error_run_again_num
        self.is_error = False

    def run(self):
        self.func(self.instance)
