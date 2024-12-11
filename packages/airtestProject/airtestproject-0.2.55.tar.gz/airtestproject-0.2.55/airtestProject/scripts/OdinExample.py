from poco.drivers.unity3d import UnityPoco
from airtestProject.commons.UWA import *
from airtestProject.airtest.core.api import *

from airtestProject.commons.utils.appStart import AppStartCase
import time
import unittest


class TestBaseCase(AppStartCase):

    def setUp(self):
        """
        开始自动化测试的准备工作：
        1、启动APP
        2、实例化poco，注意：unitypoco的实例化需要等游戏启动稳定后再实例化，否则可能会出现实例化失败的情况
        3、连接uwa接口
        4、启动uwa测试模式
        """
        print('unittest测试')
        # start_app('com.sanqi.odinUWA')
        time.sleep(10)
        self.poco = UnityPoco()
        time.sleep(5)
        GOT_Test.Connect(self.poco)
        # start需要带上mode模式，不能不带，否则上传不了，可能uwa.py的源码些得有点问题
        GOT_Test.Start(self.poco, 'overview')
        # time.sleep(5)


    def test_login(self):
        """
        用例测试过程，整体时间需要超过60s，否则uwa可能无法上传数据
        """
        time.sleep(5)
        print('开始执行点击登录按钮')
        self.poco("btnLogin").click()
        print('点击登录完毕')
        # dump
        GOT_Test.Dump(self.poco, 'overdraw')
        self.poco().wait_for_appearance()


    def tearDown(self):
        # 账号：wangmo@37.com
        # 密码：37youxi123456
        print("执行tearDown步骤")
        GOT_Test.Stop(self.poco)
        GOT_Test.LocalUpload(self.poco, account='wangmo@37.com', password='37youxi123456', projectID=1775,
                             timeLimitS=300)
        # 数据上传后，会显示一个uwa数据上传完成的确定界面，但是界面不可点击操作，因此每次自动化跑完后，需要stop掉APP
        stop_app('com.sanqi.odinUWA')


# if __name__ == '__main__':
    # unittest.suite
