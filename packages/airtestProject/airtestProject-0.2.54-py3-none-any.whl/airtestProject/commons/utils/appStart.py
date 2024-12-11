# coding=utf-8
import os
import unittest

from airtestProject.airtest.cli.parser import cli_setup
from airtestProject.airtest.core.api import auto_setup


class AppStartCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(AppStartCase, cls).setUpClass()
        # connect_device('android://127.0.0.1:5037/98f8139f')
        # cls.poco = UnityPoco()
        log_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\log"
        print(log_path)
        if not cli_setup():
            auto_setup(__file__, logdir=False,
                       devices=["android://127.0.0.1:5037/c049289f?touch_method=MAXTOUCH&", ])
            print('设备连接成功')