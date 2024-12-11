# -*- encoding=utf8 -*-

__author__ = "uwa"

import asyncio
import sys
import traceback

from airtestProject.airtest.core.android.constant import YOSEMITE_APK, YOSEMITE_PACKAGE
from airtestProject.airtest.utils.apkparser import APK
from concurrent.futures import ThreadPoolExecutor

# 导入UWA模块
from airtestProject.commons.UWA import *
from airtestProject.poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtestProject.factory.OperateFactory import operate
from airtestProject.commons.utils.logger import log as logger_log

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

auto_setup(__file__)

# 获取 UWA Pipeline 中的信息必须导入run_airtest_config模块
# import run_airtest_config


# deviceID = device().uuid

def install_apk(apk_path, apk_package):
    """
    提前装好这些包ime和poco
    Install or update the `.apk` file on the device
    :return
        None

    """
    apk_version = int(APK(apk_path).androidversion_code)
    installed_version = device().adb.get_package_version(apk_package)
    if installed_version is None or apk_version > int(installed_version):
        logger_log.info(
            "local version code is {}, installed version code is {}".format(apk_version, installed_version))
        try:
            device().adb.pm_install(apk_path, replace=True, install_options=["-t"])
        except:
            if installed_version is None:
                raise
            # If the installation fails, but the phone has an old version, do not force the installation
            print(traceback.format_exc())
            logger_log.warn(f"{apk_package} update failed, please try to reinstall manually({apk_path}).")


def check_install_permission(stop_event):
    asyncio.run(_async_check_install_permission(stop_event))


async def _async_check_install_permission(stop_event):
    permission_buttons = [
        "继续安装",
        "同意"
    ]
    tasks = [_async_click_permission_install(button, stop_event) for button in permission_buttons]
    await asyncio.gather(*tasks)


async def _async_click_permission_install(permission_button, stop_event):
    while not stop_event.is_set():
        if operate().exists(permission_button):
            operate().click(permission_button)
        await asyncio.sleep(0.1)


class TestGot:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.stop_event = asyncio.Event()

    def got_install(self):
        pass

    @logger_log.wrap("正在启动游戏")
    def got_init(self, apk_name):
        self.executor.submit(check_install_permission, self.stop_event)
        install_apk(YOSEMITE_APK, YOSEMITE_PACKAGE)
        a_poco = AndroidUiautomationPoco()  # 初始化 原生 poco 对象
        sleep(2)
        self.stop_event.set()

        stop_app("com.netease.open.pocoservice")
        sleep(2)
        start_app("com.netease.open.pocoservice")
        sleep(5)

        try:
            home()
            stop_app(apk_name)
        except:
            logger_log.step("APP is not running")

        start_app(apk_name)  # 运行App
        sleep(10)
        permission_buttons = [
            "同意",
            "允许",
            "始终允许",
            "总是允许",
            "立即开始",
            "确定",
            "稍后"
        ]

        logger_log.test("进行权限验证")
        for i in range(5):
            for button in permission_buttons:  # 权限校验
                if a_poco(text=button).exists():
                    a_poco(text=button).click()
                sleep(0.1)
        logger_log.test("权限验证结束")
        sleep(10)

    def got_connect(self, poco):
        GOT_Test.Connect(poco)
        sleep(3)
        logger_log.step("连接got")

    def got_start(self, poco, mode):
        GOT_Test.Start(poco, mode)
        logger_log.step("开始执行测试用例")

    def got_stop(self, poco):
        GOT_Test.Stop(poco)  # 关闭 GOT 模式()
        logger_log.step("开始上传")
        sleep(10)

    def got_upload(self, poco):
        GOT_Test.Upload(poco, 3000)  # 运行结束后自动上传至UWA官网()
        logger_log.step("上传结束")
        sleep(2)

    def stop_app(self, apk_name):
        stop_app(apk_name)  # 退出 App

    @staticmethod
    def sb():
        from airtestProject.poco.drivers.unity3d import UnityPoco
        # global poco

        poco = UnityPoco()
        return poco

    # def get_pipeline_info(self):
    #     """仅支持在UWA Pipeline中的Pipeline(流水线)中使用"""
    #     log("获取 设备信息")
    #     device_info = run_airtest_config.device_info
    #     log(f"设备信息为:{device_info}")
    #
    #     log("获取 package name")
    #     package_name = run_airtest_config.package_name
    #     log(f"包名的值为:{package_name}")
    #
    #     # UWA Pipeline 参数化构建与自动化测试脚本结合使用
    #     log("获取 参数化构建中设置的默认值")
    #     param_dict = {}
    #     custom_param = run_airtest_config.custom_param
    #     for custom_param_dict in custom_param:
    #         param_dict[custom_param_dict['name']] = custom_param_dict['value']
    #
    #     Name = param_dict['Name']
    #     # Out: UWA
    #     log(f"参数化构建中Name参数的值为:{Name}")
    #
    #     BoolValue = param_dict['BoolValue']
    #     # Out: False
    #     log(f"参数化构建中BoolValue参数的值为:{BoolValue}")       # 获取UWA Pipeline中信息的接口


if __name__ == '__main__':
    TestGot().got_init("com.sanqi.odin2022.weekly")
