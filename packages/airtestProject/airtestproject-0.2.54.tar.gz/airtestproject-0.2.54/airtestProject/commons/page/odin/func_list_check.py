import os
import time
from collections import deque

from airtestProject.airtest.core import api as air
from airtestProject.airtest.core.android.recorder import Recorder
from airtestProject.airtest.report.report import LogToHtml

from airtestProject.commons.utils.logger import log
from airtestProject.factory.OperateFactory import operate


class FuncListCheckPage:

    def __init__(self, adb, script_root, Project=None, log_path=None):
        self.adb = adb
        if Project is not None:
            operate('air').set_dict(script_root, Project)
        if log_path is not None:
            self.log_path = log_path
        else:
            self.log_path = None

    def open_ui_from_ui_list(self, ui, ui_view, swipe_point, first_ui, final_ui, fun_name="air"):
        """

        :param ui: 需要点击的ui
        :param ui_view: 打开后的ui界面
        :param swipe_point: 滑动点
        :param first_ui: 列表第一元素
        :param final_ui: 列表最后元素
        :param fun_name: 选用poco或air
        :return:
        """

        @log.wrap(f'正在打开{ui}界面')
        def _open_ui_from_ui_list():
            self.adb.shell("logcat -c")
            while operate(fun_name).exists(ui) is False:
                operate(fun_name).swipe(swipe_point, vector_direction=[0, -0.2])
                if operate(fun_name).exists(final_ui) is not False:
                    start_time = time.time()
                    while operate(fun_name).exists(ui) is False:
                        if time.time() - start_time > 300 or operate(fun_name).exists(first_ui) is not False:
                            log.info(f"无法找到该{ui}请检查调整参数或查看页面")
                            return
                        operate(fun_name).swipe(swipe_point, vector_direction=[0, 0.18])
            if operate(fun_name).wait_next_element(ui, ui_view) is True:
                air.sleep(3)
                log.info(f"成功点击打开{ui}")
                adb_log = self.adb.shell("logcat -d Unity:E *:S")
                log.log_adb_out(adb_log)
            else:
                air.sleep(3)
                log.info(f"打开{ui}失败")
                adb_log = self.adb.shell("logcat -d Unity:W *:S")
                log.log_adb_out(adb_log)

        _open_ui_from_ui_list()

    def open_ui(self, ui, ui_view, fun_name="air"):

        @log.wrap(f'正在打开{ui}界面')
        def _open_ui():
            self.adb.shell("logcat -c")
            if operate(fun_name).wait_next_element(ui, ui_view) is True:
                air.sleep(1)
                log.info(f"成功点击打开{ui}")
                adb_log = self.adb.shell("logcat -d Unity:E *:S")
                log.log_adb_out(adb_log)
            else:
                air.sleep(1)
                log.info(f"打开{ui}失败")
                adb_log = self.adb.shell("logcat -d Unity:W *:S")
                log.log_adb_out(adb_log)

        _open_ui()

    def close_ui(self, ui_view, close_pos, fun_name='air'):
        """

        :param ui_view: 当前界面
        :param close_pos: 关闭按钮
        :param fun_name: 选用poco或air
        :return:
        """
        self.adb.shell("logcat -c")

        @log.wrap(f'关闭ui界面{ui_view}')
        def _close_ui():
            if operate(fun_name).wait_element_appear(close_pos):
                operate(fun_name).click(close_pos)
                if operate(fun_name).wait_disappear_element(ui_view):
                    adb_out = self.adb.shell("logcat -d Unity:E *:S")
                    log.log_adb_out(adb_out)
                    log.info("关闭ui界面")
                else:
                    log.error(f"关闭{ui_view}失败")
                    adb_out = self.adb.shell("logcat -d Unity:W *:S")
                    log.log_adb_out(adb_out)

        _close_ui()

    def click_ui(self, ui, ocrPlus=None, fun_name='air'):

        @log.wrap(f"点击{ui}")
        def _click_ui():
            self.adb.shell("logcat -c")
            if ocrPlus:
                operate(fun_name).click(ui, ocrPlus=ocrPlus)
            operate(fun_name).click(ui)
            air.sleep(2)
            adb_out = self.adb.shell("logcat -d Unity:W *:S")
            log.log_adb_out(adb_out)
            log.info("点击ui")

        _click_ui()

    def click_ui_from_ui_list(self, ui, swipe_point, first_ui, final_ui, fun_name='air'):
        self.adb.shell("logcat -c")

        @log.wrap(f"从列表点击{ui}")
        def _click_ui_from_ui_list():
            while operate(fun_name).exists(ui) is False:
                operate(fun_name).swipe(swipe_point, vector_direction=[0, -0.2])
                if operate(fun_name).exists(final_ui) is not False:
                    start_time = time.time()
                    while operate(fun_name).exists(ui) is False:
                        if time.time() - start_time > 300 or operate(fun_name).exists(first_ui) is not False:
                            log.info(f"无法找到该{ui}请检查调整参数或查看页面")
                            return
                        operate(fun_name).swipe(swipe_point, vector_direction=[0, 0.1])
            operate(fun_name).click(ui)
            air.sleep(3)
            adb_out = self.adb.shell("logcat -d Unity:W *:S")
            log.log_adb_out(adb_out)
            log.info("点击ui")

        _click_ui_from_ui_list()

    def open_list(self, list_pos, next_pos, fun_name="air"):
        @log.wrap(f'打开{list_pos}列表')
        def _open_list():
            if operate(fun_name).wait_next_element(list_pos, next_pos) is False:
                log.error('打开列表失败')

        _open_list()

    def check_scenes(self, scenes_pos, wait_pos, fun_name="air"):
        self.adb.shell("logcat -c")

        @log.wrap(f'跳转场景{scenes_pos}')
        def _check_scenes():
            operate(fun_name).click(scenes_pos)
            air.sleep(0.2)
            if operate(fun_name).exists(wait_pos):
                operate(fun_name).wait_disappear_element(wait_pos)
                air.sleep(0.5)
                adb_out = self.adb.shell("logcat -d Unity:W *:S")
                log.log_adb_out(adb_out)
            else:
                log.info("点击无反应，可能是已处于对应场景")
                # air.snapshot(filename="screenshot{}点击无反应的界面.png".format(scenes_pos))
                air.sleep(0.5)
                adb_out = self.adb.shell("logcat -d Unity:W *:S")
                log.log_adb_out(adb_out)
                print(adb_out)
                return False

        _check_scenes()

    def swip_ui(self, swipe_pos, fun_name="air"):

        @log.wrap(f"滑动测试{swipe_pos}")
        def _swip_ui():
            self.adb.shell("logcat -c")
            operate(fun_name).swipe(swipe_pos)
            air.sleep(2)
            adb_out = self.adb.shell("logcat -d Unity:W *:S")
            log.log_adb_out(adb_out)
            log.info("滑动界面")

        _swip_ui()

    # TODO: 队列版本后续开发一个识别黑框的会方便点（poco其实不用这么麻烦，我后续想想怎么整合(poco可以知道ui节点也就知道了黑框存在)）
    def Plot(self, dialogue_ui_list, stop_ui, choice_ui=None, jump_ui=None, start_ui=None, log_path=None,
             fun_name="air"):
        """

        :param dialogue_ui_list: 对话list（记得按顺序，以队列遍历，遍历一个删一个）
        :param stop_ui: 剧情停止标识
        :param choice_ui: 选择按钮列表
        :param jump_ui: 跳过按钮可填无
        :param start_ui: 开始剧情界面
        :param log_path: 视频保存路径
        :param fun_name: poco或airtest
        :return:
        """
        self.adb.shell("logcat -c")
        recorder = Recorder(self.adb)
        if choice_ui is None:
            choice_ui = []
        recorder.start_recording()

        @log.wrap("过剧情")
        def _Plot():
            if start_ui is not None:
                operate(fun_name).wait_element_appear(start_ui)
            dialogue_ui_queue = deque(dialogue_ui_list)
            while operate(fun_name).exists(stop_ui) is False:
                temp = True
                if jump_ui and operate(fun_name).exists(jump_ui):
                    operate(fun_name).click(jump_ui)
                    break
                for i in choice_ui:
                    if operate(fun_name).exists(i):
                        operate(fun_name).click(i)
                        temp = False
                        break
                if temp is True:
                    while dialogue_ui_queue:
                        dialogue = dialogue_ui_queue.popleft()
                        if operate(fun_name).exists(dialogue):
                            operate(fun_name).click(dialogue)
                            break
            air.sleep(2)
            adb_out = self.adb.shell("logcat -d Unity:W *:S")
            log.log_adb_out(adb_out)
            log.info("过完剧情")

        _Plot()
        if log_path is not None:
            recorder.stop_recording(output=log_path + r"\剧情视频{}.mp4".format(start_ui))
        else:
            recorder.stop_recording()

    def scenes_jump(self):
        self.open_list("Scene", "场景跳转")
        self.check_scenes("斗罗场景", "WaitingBar")
        self.open_list("Scene", "场景跳转")
        self.check_scenes("TestShader", "WaitingBar")
        self.open_list("Scene", "场景跳转")
        self.check_scenes("斗罗场景 (流式加载)", "WaitingBar")

    def she_zhi_view(self):
        self.open_list("功能", "功能列表")
        self.open_ui_from_ui_list("设置", "SettingsPage", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.close_ui("SettingsPage", "CloseSet")

    def hua_zhi_view(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("画质", "PictureQualityPage", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui("veryLow")
        self.click_ui("Application")
        self.click_ui("Low")
        self.click_ui("Application")
        self.click_ui("Mid")
        self.click_ui("Application")
        self.click_ui("其它")
        self.click_ui("画质")
        self.close_ui("PictureQualityPage", "BackButton")

    def ji_neng_view(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("技能装配UI", "skillView", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui("skillViewAttackKey")
        self.close_ui("skillView", "BackButton")

    def demo_ui_view(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("DemoUI", "demoUIView", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui("点击发事件")
        self.click_ui("列表组件")
        self.click_ui("基础组件")
        self.close_ui("demoUIView", "BackButton")

    def sound_setting_view(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("soudsetingview", "MusicSettingInterface", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui("使用Wwise", ocrPlus=True)
        self.click_ui("Destroy Audio")
        self.click_ui("使用 UnityAudio")
        self.click_ui("创建机关")
        self.close_ui("MusicSettingInterface", "CloseMusicView")

    def DemoRTShowHighQualityShadowView(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("DemoRTShowHighQualityShadowView", "HDshadowModelInterface", "FuncListSwipe", "创建怪物",
                                  "配置按需加载")
        self.close_ui("HDshadowModelInterface", "BackButton")

    def DemoRTShowOrthographicView(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("DemoRTShowOrthographicView", "DemoRTShowOrthographicViewIn", "FuncListSwipe", "创建怪物",
                                  "配置按需加载")
        self.close_ui("DemoRTShowOrthographicViewIn", "BackButton")

    def DemoRTShowPlanarShadowView(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("DemoRTShowPlanarShadowView", "PlanarShadow", "FuncListSwipe", "创建怪物",
                                  "配置按需加载")
        self.close_ui("PlanarShadow", "BackButton")

    def SRPBatcherProfiler(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("SRPBatcherProfiler", "关闭SRP Batcher", "FuncListSwipe", "创建怪物",
                                  "配置按需加载")
        self.click_ui("关闭SRP Batcher")
        self.click_ui("开启SRP Batcher")
        self.open_list("Func", "功能列表")
        self.close_ui("关闭SRP Batcher", "SRPBatcherProfiler")

    def TestUIMoldeClipView(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("TestUIMoldeClipView", "TestMoldeView", "FuncListSwipe", "创建怪物",
                                  "配置按需加载")
        self.swip_ui("TestMoldeSwipe")
        self.click_ui("打开新")
        self.click_ui("TestUIMoldeClipView")
        self.close_ui("TestMoldeView", "TestMoldeCloseBtn")

    def xie_yi_view(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("Proto", "测试发送", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui("恢复监听发送")
        self.click_ui("恢复监听接收")
        self.click_ui("测试发送")
        self.click_ui("清空")
        self.close_ui("测试发送", "ProtoCloseBtn")

    def shi_pin(self):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("AVPro视频", "VideoView", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.close_ui("VideoView", "VideoInterfaceCloseButton")

    def ce_shi_ju_qin1(self, log_path):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("测试剧情1", "TestPlotBlackCurtain1", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.Plot(["最近怪物横行，请少侠前往击杀"], "功能", ["挑战Boss"], start_ui="TestPlotStart1", log_path=log_path)

    def ce_shi_ju_qin2(self, log_path):
        self.open_list("Func", "功能列表")
        self.open_ui_from_ui_list("测试剧情2", "TestPlotBlackCurtain2", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.Plot(["最近怪物横行，请少侠前往击杀", "这个小怪有点强，你要不要和我一起去？", "不是吧，小怪还要我帮忙啊！",
                  "两个人一起，不是打的快些嘛", "好吧，陪你走一遭"], stop_ui="功能", start_ui="TestPlotStart2", log_path=log_path)

    def run_step(self):
        self.scenes_jump()

        self.she_zhi_view()

        self.hua_zhi_view()

        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("reloadall", "FuncListSwipe", "创建怪物", "配置按需加载")

        self.ji_neng_view()

        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("testloadrawdata", "FuncListSwipe", "创建怪物", "配置按需加载")

        self.demo_ui_view()

        self.sound_setting_view()

        self.DemoRTShowHighQualityShadowView()

        self.DemoRTShowOrthographicView()

        self.DemoRTShowPlanarShadowView()

        self.SRPBatcherProfiler()

        self.TestUIMoldeClipView()

        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("checkForUpdates", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("镜头切换", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("镜头切换", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("镜头切换", "FuncListSwipe", "创建怪物", "配置按需加载")

        self.xie_yi_view()

        self.shi_pin()

        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("whetherOrNotObjID", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("whetherOrNotObjID", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("记录协议", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("显示ping", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("errorPromptView", "FuncListSwipe", "创建怪物", "配置按需加载")
        self.click_ui_from_ui_list("DamageText Test", "FuncListSwipe", "创建怪物", "配置按需加载")

        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("GCTest", "FuncListSwipe", "创建怪物", "配置按需加载")

        self.open_list("Func", "功能列表")
        self.click_ui_from_ui_list("测试报错", "FuncListSwipe", "创建怪物", "配置按需加载")

        self.ce_shi_ju_qin1(self.log_path)

        self.ce_shi_ju_qin2(self.log_path)


def _wait_for_log_generation(log_path, timeout=60):
    size = -1
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not os.path.exists(log_path):
            time.sleep(1)
            continue
        current_size = os.path.getsize(log_path)
        if current_size == size:
            break  # 文件大小没有变化，认为日志生成完毕
        else:
            size = current_size
            time.sleep(1)  # 等待一秒再次检查


if __name__ == '__main__':
    project_root = r"G:\pyProject\odin-testautomation\TestAutomation\airtestProjects\commons\page\odin"
    log_path = r"/airtestProject\commons\page\odin\log"
    air.auto_setup(__file__, devices=["Android:///"], project_root=project_root, logdir=True)
    serialno = air.device().adb.serialno
    # output_html_path = r"G:\pyProject\odin-testautomation\TestAutomation\airtestProject\commons\page\odin\log\log
    # .html"
    _wait_for_log_generation(log_path)
    func_list_check_report = LogToHtml(script_root=__file__, log_root=log_path,
                                       export_dir=project_root + r"\report", logfile=log_path + r"\log.txt", lang='zh',
                                       plugins=None)
    func_list_check_report.report()
