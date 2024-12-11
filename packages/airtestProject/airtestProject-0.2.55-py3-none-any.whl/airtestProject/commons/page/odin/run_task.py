"""
主界面
"""
import time
import threading
from random import choice
from airtestProject.commons.utils.page import Page
from airtestProject.commons.page.odin.func_list_check_task import FuncListCheckPage
from airtestProject.factory.OperateFactory import operate
from airtestProject.airtest.core.api import *
from airtestProject.commons.utils.logger import log
from airtestProject.solox.public.apm import initPerformanceService
from airtestProject.solox.public.common import Devices
import re
import cv2
import numpy as np
from airtestProject.commons.stateMachine.task_machine import check_func, TaskCaseTemplate, put_task, stop_machine_f, \
    only_run_this, start_tag

pos = [0, 0]

scenes_pos = "btnScenes"  # 场景按钮
common_scenes_pos = "text=斗罗场景"
test_scenes_pos = "text=测试场景"
streaming_scenes_pos = "text=斗罗场景（流式加载）"
scenes_view_pos = "ScenesSwitchView(Clone)"

fun_view_pos = "funGridView"  # 功能列表
fun_pos = "btnFunView"  # 功能按钮
running_pos = "text=自动跑图"

running_param_1 = "inputFieldScene"
running_param_2 = "inputFieldPathIndex"
running_param_3 = "inputFieldPositionIndex"

start_running_pos = "btnStart"  # 开始跑图按钮
close_running_pos = "btnClose"  # 关闭跑图界面
exit_pos = "btnExit"

axis_pos = "txtDes"
index = re.compile(r'\b(\d+)\.\d+')
running_pos_end_1 = ["1525.03", "5.63", "949.79"]


class RunPage:

    def __init__(self, script_root, Project=None):
        """

        :param project: 如果想采用命名代替文件夹路径的方法需要传入一个文件夹名让air生成对应字典。
        """
        if Project is not None:
            operate("air").set_dict(script_root, Project)


    @check_func('关闭场景页面')
    def close_scene_view(self, scenes_view_pos, scenes_pos, fun_name="air"):
        for i in range(5):
            if operate(fun_name).exists(scenes_view_pos):
                operate(fun_name).click(scenes_pos)
                return True
            else:
                log.step("等待")
                operate(fun_name).sleep(1.0)
        log.error("没有关闭场景页面")


    @check_func('设置跑图参数')
    def set_scene_param(self, running_param_1, running_param_2, running_param_3, params: list, fun_name="air"):
        operate(fun_name).set_text(running_param_1, params[0])
        operate(fun_name).set_text(running_param_2, params[1])
        operate(fun_name).set_text(running_param_3, params[2])

    def start_run(self, start_running_pos, fun_name="air"):
        for i in range(3):
            if operate(fun_name).exists(start_running_pos):
                operate(fun_name).click(start_running_pos)
            else:
                break

    @check_func('关闭跑图界面')
    def close_running_view(self, close_running_pos, fun_name="air"):
        for i in range(3):
            if operate(fun_name).exists(close_running_pos):
                operate(fun_name).click(close_running_pos)
            else:
                break


class run_test(TaskCaseTemplate, FuncListCheckPage):
    def __init__(self, script_root, project=None, fun_name="air"):
        super(run_test, self).__init__()
        self.obj = RunPage(script_root, project)
        self.fun_name = fun_name

    @put_task(is_profile=True)
    def run_test(self):
        super().open_list("Scene", "场景跳转")
        super().check_scenes("20003场景 (流式加载)", "WaitingBar","FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
        super().open_list("Scene", "场景跳转")
        super().check_scenes("斗罗场景 (流式加载)", "WaitingBar","FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
        super().open_list("功能", "功能列表")
        super().open_ui_from_ui_list("自动跑图", "开始跑图", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        self.obj.set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20002", "1", "1"])
        self.obj.start_run("开始跑图")
        self.obj.close_running_view("close_running_pos")

    def check_running_end(self):
        print("进入检查结束")
        if self.fun_name == "poco":
            while True:
                axis = index.findall(operate(self.fun_name).get_text(axis_pos))
                log.step(f'当前坐标为-{axis}')
                operate(self.fun_name).sleep(5)
                if axis == running_pos_end_1:
                    break
        else:
            # TODO:
            # ocr坐标作为判断
            while True:
                diff1 = operate(self.fun_name).snapshot(10, 10)
                time.sleep(3)  # 停顿三秒截图查看差异
                diff2 = operate(self.fun_name).snapshot(10, 10)

                diff1 = np.array(diff1)
                diff2 = np.array(diff2)

                mse = np.mean((diff1 - diff2) ** 2)  # 使用均方误差（MSE）判断差异
                threshold = 10  # 根据实际情况调整阈值
                if mse < threshold:
                    print('画面没有变动，疑似卡住')
                    break

    def run_test2(self):
        super().open_list("Scene", "场景跳转")
        super().check_scenes("20003场景 (流式加载)", "WaitingBar","FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
        super().open_list("功能", "功能列表")
        super().open_ui_from_ui_list("自动跑图", "开始跑图", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        self.obj.set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20003", "1", "1"])
        self.obj.start_run("开始跑图")
        self.obj.close_running_view("close_running_pos")

    def check_running_end2(self):
        print("进入检查结束")
        if self.fun_name == "poco":
            while True:
                axis = index.findall(operate(self.fun_name).get_text(axis_pos))
                log.step(f'当前坐标为-{axis}')
                operate(self.fun_name).sleep(5)
                if axis == running_pos_end_1:
                    break
        else:
            # TODO:
            # ocr坐标作为判断
            while True:
                diff1 = operate(self.fun_name).snapshot(10, 10)
                time.sleep(3)  # 停顿三秒截图查看差异
                diff2 = operate(self.fun_name).snapshot(10, 10)

                diff1 = np.array(diff1)
                diff2 = np.array(diff2)

                mse = np.mean((diff1 - diff2) ** 2)  # 使用均方误差（MSE）判断差异
                threshold = 10  # 根据实际情况调整阈值
                if mse < threshold:
                    print('画面没有变动，疑似卡住')
                    break


if __name__ == '__main__':
    connect_device("Android:///fe8b96af")
    # run_test()
