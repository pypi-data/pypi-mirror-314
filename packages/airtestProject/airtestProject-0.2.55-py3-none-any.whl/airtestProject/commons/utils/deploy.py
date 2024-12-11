# _*_ coding: UTF-8 _*_
from airtestProject.airtest.core.api import *
from airtestProject.airtest.cli.parser import cli_setup


# from PIL import Image
# import matplotlib.pyplot as plt
import sys
from airtestProject.airtest.core.android.adb import ADB

# auto_setup(__file__,logdir=False,devices= ["Android://127.0.0.1:5037/46HDU19307002391"])


class startDeploy():
    """
    定义启动类
    """

    def __init__(self):
        """
        定义部署元素
        """
        #airtest输入法
        self.ym = "com.netease.nie.yosemite/.ime.ImeService"
        self.ime_list = []

        #相对坐标
        self.w = ()
        self.h = ()

        #安装包相关
        self.pwd = os.path.dirname(__file__)
        # self.pkg = "com.sanqi.odin.uwa.mono"

        #连接设备号
        # self.device_list = [
        #     ["Android://127.0.0.1:5037/46HDU19307002391"],#荣耀V20
        #     ["Android://127.0.0.1:5037/R5CTB17E1EX"]
        # ]
        self.url = "Android://127.0.0.1:5037/"

    def get_deviceId(self):
        """
        获取device
        """
        device = os.popen("adb devices").readlines()
        device_id = device[1]

        return self.url + device_id.split()[0]

    def get_auto_setup(self,device_list):
        """
        环境接口
        """
        return auto_setup(__file__, logdir=False, devices=[device_list])

    def get_url(self):
        return self.url

    def get_current_resolution(self):
        """
        相对坐标
        """
        self.w , self.h = device().get_current_resolution()
        return self.w, self.h

    # def switch_ime(self, param):
    #     """
    #     切换输入法
    #     """
    #     list = device().yosemite_ime._get_ime_list()
    #     def set_ime(ime):
    #         shell("ime enable " + ime)
    #         shell("ime set " + ime)
    #
    #     self.ime_list.append(self.ym)
    #
    #     for ime in list:
    #         if ime != self.ym:
    #             self.ime_list.append(ime)
    #             break
    #
    #     # 切换输入法
    #     if param == const.IME_YOSEMITE :
    #         set_ime(self.ime_list[0]) #Yosemite
    #
    #     else:
    #         set_ime(self.ime_list[1]) #手机自带


# dep = startDeploy()
# # 获取连接设备
# deviceId = dep.get_deviceId()
# print(deviceId)
# # startDeploy().get_auto_setup("Android://127.0.0.1:5037/46HDU19307002391")
# startDeploy().get_auto_setup("Android://127.0.0.1:5037/R5CTB17E1EX")
# st = startDeploy()
# # startDeploy().get_ime("YOSEMITE")
# 切换输入法
# str = startDeploy().get_deviceId()
# print(get_deviceId)
# startDeploy().get_auto_setup(str)
# log(str+'已连上')
