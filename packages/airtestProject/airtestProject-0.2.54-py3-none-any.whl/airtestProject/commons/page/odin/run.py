"""
主界面
"""
import time
import threading
from random import choice
from airtestProject.commons.utils.page import Page
from airtestProject.commons.page.odin.func_list_check import FuncListCheckPage
from airtestProject.factory.OperateFactory import operate
from airtestProject.airtest.core.api import *
from airtestProject.commons.utils.logger import log
from airtestProject.solox.public.apm import initPerformanceService
from airtestProject.solox.public.common import Devices
import re
import cv2
import numpy as np

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

    def __init__(self, adb, script_root, Project=None, log_path=None):
        """

        :param project: 如果想采用命名代替文件夹路径的方法需要传入一个文件夹名让air生成对应字典。
        """
        self.adb = adb
        if Project is not None:
            operate("air").set_dict(script_root, Project)
        if log_path is not None:
            self.log_path = log_path
        else:
            self.log_path = None
        self.funcListCheck = FuncListCheckPage(adb, script_root, Project, log_path)

    @log.wrap('点击场景按钮成功')
    def click_scene(self, scenes_pos, scenes_view_pos, fun_name="air"):
        start_time = time.time()
        while operate(fun_name).exists(scenes_view_pos) is False:
            operate(fun_name).click(scenes_pos)
            log.step('点击场景按钮')
            if start_time - time.time() > 30:
                log('点击失败')
                break
        log.step('弹出场景选择页面')
        #
        # for i in range(5):
        #     if not operate(fun_name).exists(scenes_view_pos):
        #         operate(fun_name).click(scenes_pos)
        #         log.step('点击场景按钮')
        #     else:
        #         log.step('弹出场景选择界面')
        #         break
        #     return False

    @log.wrap('点击斗罗流式加载场景按钮')
    def click_streaming_scenes(self, streaming_scenes_pos, fun_name="air"):
        operate(fun_name).click(streaming_scenes_pos)

    @log.wrap('关闭场景页面')
    def close_scene_view(self, scenes_view_pos, scenes_pos, fun_name="air"):
        for i in range(5):
            if operate(fun_name).exists(scenes_view_pos):
                operate(fun_name).click(scenes_pos)
                return True
            else:
                log.step("等待")
                operate(fun_name).sleep(1.0)
        log.error("没有关闭场景页面")

    @log.wrap('点击功能按钮')
    def click_fun(self, fun_pos, fun_view, fun_name="air"):
        operate(fun_name).wait_next_element(fun_pos, fun_view)

    @log.wrap('滑动功能列表至最底')
    def swipe_fun_view_last(self, running_pos, fun_view_pos, fun_name="air"):
        for i in range(3):
            if not operate(fun_name).exists(running_pos):
                log.step('未找到自动跑图,尝试滑动')
                operate(fun_name).swipe(fun_view_pos, v2=None, vector_direction=[0, -1.0], duration=0.5)
            else:
                break

    @log.wrap('点击自动跑图按钮')
    def click_running(self, running_pos, fun_name="air"):
        operate(fun_name).click(running_pos)

    @log.wrap('点击退出按钮')
    def click_exit(self, exit_pos, fun_name="air"):
        operate(fun_name).click(exit_pos)

    @log.wrap('设置跑图参数')
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

    @log.wrap('关闭跑图界面')
    def close_running_view(self, close_running_pos, fun_name="air"):
        for i in range(3):
            if operate(fun_name).exists(close_running_pos):
                operate(fun_name).click(close_running_pos)
            else:
                break

    def check_running_end(self, fun_name="air", apm=None):
        print("进入检查结束")
        apm.collectAll(True)
        if fun_name == "poco":
            while True:
                axis = index.findall(operate(fun_name).get_text(axis_pos))
                log.step(f'当前坐标为-{axis}')
                operate(fun_name).sleep(5)
                if axis == running_pos_end_1:
                    break
        else:
            # TODO:
            # ocr坐标作为判断
            while True:
                diff1 = operate(fun_name).snapshot(10, 10)
                time.sleep(3)  # 停顿三秒截图查看差异
                diff2 = operate(fun_name).snapshot(10, 10)

                diff1 = np.array(diff1)
                diff2 = np.array(diff2)

                mse = np.mean((diff1 - diff2) ** 2)  # 使用均方误差（MSE）判断差异
                threshold = 10  # 根据实际情况调整阈值
                if mse < threshold:
                    print('画面没有变动，疑似卡住')
                    break

        apm.collectAll(False)
        print("采集完毕")


    @log.wrap('打开自动跑图界面，输入参数')
    def start_running_1(self, button_dict, fun_name="air"):
        self.click_scene()
        self.click_streaming_scenes()
        operate(fun_name).sleep(10.0)
        self.click_fun()
        operate(fun_name).sleep(1.0)
        self.swipe_fun_view_last()
        operate(fun_name).sleep(2.0)
        self.click_running()
        operate(fun_name).sleep(0.5)
        self.set_scene_param(["20002", "1", "1"])

    @log.wrap('点击开启跑图')
    def start_running_2(self):
        self.funcListCheck.open_list("功能", "功能列表")
        self.funcListCheck.open_ui_from_ui_list("自动跑图", "开始跑图", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        self.set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20002", "1", "1"])
        self.start_run("开始跑图")
        self.check_running_end()

    @log.wrap('点击开启跑图')
    def start_running_3(self):
        self.funcListCheck.open_list("功能", "功能列表")
        self.funcListCheck.open_ui_from_ui_list("自动跑图", "开始跑图", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        self.set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20002", "1", "1"])
        self.start_run("开始跑图")
        self.close_running_view("close_running_pos")




def run_test_poco():
    run_main = RunPage(None, __file__, "odin")
    run_main.click_scene(scenes_pos, scenes_view_pos, fun_name="poco")
    run_main.click_streaming_scenes(streaming_scenes_pos, fun_name="poco")
    run_main.close_scene_view(scenes_view_pos, scenes_pos, fun_name="poco")
    run_main.click_fun()


def run_test():
    run_main = RunPage(None, __file__, "odin")
    run_main.click_scene("Scene", "场景跳转")
    run_main.click_streaming_scenes("斗罗场景（流式加载）")
    run_main.close_scene_view("场景跳转", "Scene")
    run_main.click_fun("Func", "功能列表")
    run_main.swipe_fun_view_last("AutoMapRunning", "FuncListSwipe")
    run_main.click_running("AutoMapRunning")
    run_main.set_scene_param("场景:", "路径下标：", "路点下标  从1开始:", ["20002", "1", "1"])
    run_main.start_run("开始跑图")



if __name__ == '__main__':
    connect_device("Android:///fe8b96af")
    run_test()
