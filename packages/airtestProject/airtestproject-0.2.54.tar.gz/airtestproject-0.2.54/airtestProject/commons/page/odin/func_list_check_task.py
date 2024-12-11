import os
import time
from collections import deque

from airtestProject.airtest.core.error import TargetNotFoundError
from airtestProject.commons.stateMachine.task_machine import check_func, TaskCaseTemplate, put_task, stop_machine_f, \
    only_run_this, start_tag

from airtestProject.commons.utils.logger import log
from airtestProject.factory.OperateFactory import operate


class FuncListCheckPage:
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

        @check_func(f'正在打开{ui}界面')
        def _open_ui_from_ui_list():
            if self._swipe_list(fun_name, ui, swipe_point, first_ui, final_ui,
                                [0, 0.18], [0, -0.23], 300):
                if operate(fun_name).wait_next_element(ui, ui_view) is True:
                    operate(fun_name).sleep(3)
                    log.info(f"成功点击打开{ui}")
                else:
                    operate(fun_name).sleep(3)
                    log.info(f"打开{ui}失败")

        _open_ui_from_ui_list()

    def open_ui(self, ui, ui_view, fun_name="air"):
        @check_func(f'正在打开{ui}界面')
        def _open_ui():
            if operate(fun_name).wait_next_element(ui, ui_view) is True:
                operate(fun_name).sleep(1)
                log.info(f"成功点击打开{ui}")
            else:
                operate(fun_name).sleep(1)
                log.info(f"打开{ui}失败")

        _open_ui()

    def close_ui(self, ui_view, close_pos, fun_name='air'):
        """

        :param ui_view: 当前界面
        :param close_pos: 关闭按钮
        :param fun_name: 选用poco或air
        :return:
        """

        @check_func(f'关闭ui界面{ui_view}')
        def _close_ui():
            if operate(fun_name).wait_element_appear(close_pos,timeout=60):
                operate(fun_name).click(close_pos)
                if operate(fun_name).wait_disappear_element(ui_view):
                    log.info("关闭ui界面")
                else:
                    log.error(f"关闭{ui_view}失败")

        _close_ui()

    def click_ui(self, ui, ocrPlus=None, fun_name='air'):
        @check_func(f"点击{ui}")
        def _click_ui():
            if ocrPlus:
                operate(fun_name).click(ui, ocr_plus=ocrPlus)
            operate(fun_name).click(ui)
            operate(fun_name).sleep(2)
            log.info("点击ui")

        _click_ui()

    def click_ui_from_ui_list(self, ui, swipe_point, first_ui, final_ui, fun_name='air'):
        @check_func(f"从列表点击{ui}")
        def _click_ui_from_ui_list():
            if self._swipe_list(fun_name, ui, swipe_point, first_ui, final_ui,
                                [0, 0.18], [0, -0.23], 300):
                operate(fun_name).click(ui)
                operate(fun_name).sleep(3)
                log.info(f"点击{ui}")

        _click_ui_from_ui_list()

    def open_list(self, list_pos, next_pos, fun_name="air", ocrPlus=True):
        @check_func(f'打开{list_pos}列表')
        def _open_list():
            if operate(fun_name).wait_element_appear(list_pos, ocr_plus=ocrPlus):
                if operate(fun_name).wait_next_element(list_pos, next_pos, ocr_plus=ocrPlus) is False:
                    log.error('打开列表失败')
            else:
                log.error('无法找到列表打开按钮')
                raise TargetNotFoundError('找不到列表打开按钮')

        _open_list()

    def check_scenes(self, scenes_pos, wait_pos, swipe_point, first_ui, final_ui, fun_name="air"):
        @check_func(f'跳转场景{scenes_pos}')
        def _check_scenes():
            if self._swipe_list(fun_name, scenes_pos, swipe_point, first_ui, final_ui,
                                [0, 0.18], [0, -0.13], 300):
                operate(fun_name).click(scenes_pos)
            else:
                log.info("跳转场景按钮不存在")
            operate(fun_name).sleep(0.5)
            if operate(fun_name).exists(wait_pos):
                operate(fun_name).wait_disappear_element(wait_pos)
                operate(fun_name).sleep(0.5)
            else:
                log.info("可能是已处于对应场景")
                # air.snapshot(filename="screenshot{}点击无反应的界面.png".format(scenes_pos))
                operate(fun_name).sleep(0.5)
                return False

        _check_scenes()

    def swip_ui(self, swipe_pos, fun_name="air"):
        @check_func(f"滑动测试{swipe_pos}")
        def _swip_ui():
            operate(fun_name).swipe(swipe_pos)
            operate(fun_name).sleep(2)
            log.info("滑动界面")

        _swip_ui()

    # TODO: 队列版本后续开发一个识别黑框的会方便点（poco其实不用这么麻烦，我后续想想怎么整合(poco可以知道ui节点也就知道了黑框存在)）
    def Plot(self, dialogue_ui_list, stop_ui, choice_ui=None, jump_ui=None, start_ui=None, fun_name="air"):
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
        if choice_ui is None:
            choice_ui = []

        @check_func("过剧情")
        def _Plot():
            if start_ui is not None:
                operate(fun_name).wait_element_appear(start_ui, timeout=60)
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
            operate(fun_name).sleep(2)
            log.info("过完剧情")

        _Plot()

    def _swipe_list(self, fun_name, ui, swipe_point, first_ui, final_ui, swipe_up_list, swipe_down_list,
                    swipe_out_time):
        while operate(fun_name).exists(ui) is False:
            operate(fun_name).swipe(swipe_point, vector_direction=swipe_down_list)
            if operate(fun_name).exists(final_ui) is not False:
                start_time = time.time()
                while operate(fun_name).exists(ui) is False:
                    if time.time() - start_time > swipe_out_time or operate(fun_name).exists(first_ui) is not False:
                        log.info(f"无法找到该{ui}请检查调整参数或查看页面")
                        return False
                    operate(fun_name).swipe(swipe_point, vector_direction=swipe_up_list)
        return True


class FuncListCheckTask(TaskCaseTemplate, FuncListCheckPage):

    def __init__(self, script_root, Project=None):
        super().__init__()
        if Project is not None:
            operate('air').set_dict(script_root, Project)

    @put_task(is_profile=True)
    def scenes_jump(self):
        super().open_list("Scene", "场景跳转")
        super().check_scenes("斗罗场景", "WaitingBar","FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
        super().open_list("Scene", "场景跳转")
        super().check_scenes("TestShader", "WaitingBar","FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
        super().open_list("Scene", "场景跳转")
        super().check_scenes("20003场景 (流式加载)", "WaitingBar","FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
        super().open_list("Scene", "场景跳转")
        super().check_scenes("斗罗场景 (流式加载)", "WaitingBar", "FuncListSwipe", "遍历特效", "20003场景 (流式加载)")
    @put_task
    def she_zhi_view(self):
        super().open_list("功能", "功能列表")
        super().open_ui_from_ui_list("设置", "SettingsPage", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().close_ui("SettingsPage", "CloseSet")

    @put_task
    def hua_zhi_view(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("画质", "PictureQualityPage", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        # super().click_ui("veryLow")
        # super().click_ui("Application")
        # super().click_ui("Low")
        # super().click_ui("Application")
        # super().click_ui("Mid")
        # super().click_ui("Application")
        # super().click_ui("其它")
        # super().click_ui("画质") 去除切换，否则所有机器都一个画质不合适
        super().close_ui("PictureQualityPage", "BackButton")

    def reloadall_check(self):
        super().open_list("Func", "功能列表")
        super().click_ui_from_ui_list("reloadall", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")

    @put_task
    def ji_neng_view(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("技能装配UI", "skillView", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().click_ui("skillViewAttackKey")
        super().close_ui("skillView", "BackButton")

    def test_load_rawdata(self):
        super().open_list("Func", "功能列表")
        super().click_ui_from_ui_list("testloadrawdata", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")

    @put_task
    def demo_ui_view(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("DemoUI", "demoUIView", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().click_ui("点击发事件")
        super().click_ui("列表组件")
        super().click_ui("基础组件")
        super().close_ui("demoUIView", "BackButton")

    @put_task
    def sound_setting_view(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("soudsetingview", "MusicSettingInterface", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().click_ui("使用Wwise", ocrPlus=True)
        super().click_ui("Destroy Audio")
        super().click_ui("使用 UnityAudio")
        super().click_ui("创建机关")
        super().close_ui("MusicSettingInterface", "CloseMusicView")

    @put_task
    def DemoRTShowHighQualityShadowView(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("DemoRTShowHighQualityShadowView", "HDshadowModelInterface", "FuncListSwipe",
                             "创建怪物",
                             "点击界面外关闭界面")
        super().close_ui("HDshadowModelInterface", "BackButton")

    @put_task
    def DemoRTShowOrthographicView(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("DemoRTShowOrthographicView", "DemoRTShowOrthographicViewIn", "FuncListSwipe",
                             "创建怪物",
                             "点击界面外关闭界面")
        super().close_ui("DemoRTShowOrthographicViewIn", "BackButton")

    @put_task
    def DemoRTShowPlanarShadowView(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("DemoRTShowPlanarShadowView", "PlanarShadow", "FuncListSwipe", "创建怪物",
                             "点击界面外关闭界面")
        super().close_ui("PlanarShadow", "BackButton")

    @put_task
    def SRPBatcherProfiler(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("SRPBatcherProfiler", "关闭SRP Batcher", "FuncListSwipe", "创建怪物",
                             "点击界面外关闭界面")
        super().click_ui("关闭SRP Batcher")
        super().click_ui("开启SRP Batcher")
        super().open_list("Func", "功能列表")
        super().close_ui("关闭SRP Batcher", "SRPBatcherProfiler")

    @put_task
    def TestUIMoldeClipView(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("TestUIMoldeClipView", "TestMoldeView", "FuncListSwipe", "创建怪物",
                             "点击界面外关闭界面")
        super().swip_ui("TestMoldeSwipe")
        super().click_ui("打开新")
        super().click_ui("TestUIMoldeClipView")
        super().close_ui("TestMoldeView", "TestMoldeCloseBtn")

    def check_for_updates(self):
        super().open_list("Func", "功能列表")
        super().click_ui_from_ui_list("checkForUpdates", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")

    def shot_cut(self):
        super().open_list("Func", "功能列表")
        super().click_ui_from_ui_list("镜头切换", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().click_ui_from_ui_list("镜头切换", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().click_ui_from_ui_list("镜头切换", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")

    # @put_task
    @put_task
    def xie_yi_view(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("Proto", "测试发送", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().click_ui("恢复监听发送")
        super().click_ui("恢复监听接收")
        super().click_ui("测试发送")
        super().click_ui("清空")
        super().close_ui("测试发送", "ProtoCloseBtn")

    @put_task
    def shi_pin(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("avpro", "VideoView", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().close_ui("VideoView", "VideoInterfaceCloseButton")
    def shi_pin2(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("video", "VideoView", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().close_ui("VideoView", "VideoInterfaceCloseButton")

    def ce_shi_ju_qin1(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("测试剧情1", "TestPlotBlackCurtain1", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().Plot(["最近怪物横行，请少侠前往击杀"], "功能", ["挑战Boss"], start_ui="TestPlotStart1")

    @put_task(is_recording=True, is_profile=True)
    def ce_shi_ju_qin2(self):
        super().open_list("Func", "功能列表")
        super().open_ui_from_ui_list("测试剧情2", "TestPlotBlackCurtain2", "FuncListSwipe", "创建怪物", "点击界面外关闭界面")
        super().Plot(["最近怪物横行，请少侠前往击杀", "这个小怪有点强，你要不要和我一起去？", "不是吧，小怪还要我帮忙啊！",
              "两个人一起，不是打的快些嘛", "好吧，陪你走一遭"], stop_ui="功能", start_ui="TestPlotStart2")
