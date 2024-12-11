import time

from airtestProject.commons.page.odin.login import LoginPage
from airtestProject.commons.utils.gotCommon import TestGot
from airtestProject.commons.UWA import *
from airtestProject.commons.utils.logger import log
# from poco.drivers.unity3d import UnityPoco


class OdinProfile:

    def __init__(self):
        self.odin_poco_apk = "com.sanqi.odin.poco"
        self.odin_weekly_apk = "com.sanqi.odin.weekly"
        self.odin_2022weekly_apk = "com.sanqi.odin2022.weekly"
        self.odin_uwa_apk = "com.sanqi.odinUWA"
        self.odin_2022uwa_apk = "com.sanqi.odin2022.uwa"
        self.got = TestGot()
        # self.mainPage = MainPage()

    @log.wrap("跑图并上传UWA")
    def test_running_uwa(self):
        self.got.got_init(self.odin_2022uwa_apk)
        stop_app(self.odin_poco_apk)

    @log.wrap("跑checklist")
    def test_check_list(self):
        self.got.got_init(self.odin_2022uwa_apk)
        # 登录



if __name__ == '__main__':
    odin = OdinProfile()
    odin.test_running_uwa()
