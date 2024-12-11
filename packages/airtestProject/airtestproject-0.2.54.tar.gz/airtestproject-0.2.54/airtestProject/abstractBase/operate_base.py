#!-*- coding = utf-8 -*-
# @Time : 2024/4/7 2:44
# @Author : 苏嘉浩
# @File : operate_base.py
# @Software : PyCharm
from abc import ABC, abstractmethod

"""
airtest核心api和poco的二次封装，操作具体基类
"""


class OperateABC(ABC):

    @abstractmethod
    def click(self, pos, *args, **kwargs):
        """
        poco: 可以传入focus参数点击上下左右
        :param pos:
        :param args:
        :param kwargs:
        airtest可传参数 ocrPlus=True,可以开启二值化 , rgb可以开启色彩校验
        :return:
        """
        pass

    @abstractmethod
    def exists(self, pos, **kwargs):
        """

        :param pos: 传入的元素
        :param kwargs: 如果是使用ocr可以传入ocrPlus=True,可以开启二值化
        :return: 找到返回元素坐标，找不到返回FAlSE
        """
        pass

    @abstractmethod
    def sleep(self, secs):
        """

        :param secs: 延迟秒数
        :return:
        """
        pass

    @abstractmethod
    def swipe(self, value, v2=None, vector_direction=None, **kwargs):
        """

        :param value: 要滑动的元素
        :param v2: airtest可以选填滑动到的元素（poco其实底层也是有两个元素的，但是封装后现在没有，后续考虑airtest也去掉第二个元素）
        :param vector_direction: （按比例滑动）
        :param kwargs: 定义参数，熟悉poco的可以自己添加
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def swipe_along(self, pos, coordinates_list: list, **kwargs):
        """
        目前只支持安卓后续考虑支持win和linux。
            :param pos: 第一个滑动点
            :param coordinates_list: 多个滑动点的列表
            :param kwargs: 可以传入滑动间隔
            :return:
        """
        pass

    @abstractmethod
    def swipe_plus(self, value, v2=None, down_event_sleep=None, vector_direction=None, **kwargs):
        """
        poco还没实现
        :param value: 要滑动的元素
        :param v2: airtest可以选填滑动到的元素（poco其实底层也是有两个元素的，但是封装后现在没有，后续考虑airtest也去掉第二个元素）
        :param down_event_sleep:滑到终点时停留的时间
        :param vector_direction: （按比例滑动）
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def pinch(self, in_or_out, percent=0.5, **kwargs):
        """

        :param in_or_out: 缩放方向in就是里面out就是往外
        :param percent: 屏幕捏动百分比
        :param kwargs: airtest和poco还有一些小参数可以自己定义
        :return:
        """
        pass

    @abstractmethod
    def set_text(self, pos, text, *args, **kwargs):
        """

        :param pos: 输入框元素
        :param text: 文字
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def wait(self, pos, timeout=None, *args, **kwargs):
        pass

    @abstractmethod
    def wait_disappear_element(self, pos, timeout=180, *args, **kwargs):
        """
        等待元素消失
        :param timeout: 超时时间
        :param pos: 元素
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def wait_element_appear(self, pos, timeout=180, *args, **kwargs):
        """
        等待元素出现
        :param timeout: 超时时间
        :param pos:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def persistent_element_exists(self, pos):
        """
        暂时未实现，判断元素是否一直存在
        :param pos:
        :return:
        """
        pass

    def set_dict(self, script_root, project):
        """
        图片识别需要设定路径用文件名代替路径, 通过airtest调用
        :param script_root: 脚本当前目录
        :param project: 定位到的具体图片文件夹
        :return:
        """
        pass

    @abstractmethod
    def wait_for_any(self, pos_list: list, timeout=30, **kwargs):
        """
        等待列表中的某一个元素
        :param pos_list: 元素列表
        :param timeout:
        :return:
        """
        pass

    @abstractmethod
    def wait_for_all(self, pos_list: list, timeout=30, **kwargs):
        """

        :param pos_list: 等待列表中的全部元素
        :param timeout:
        :return:
        """
        pass

    @abstractmethod
    def wait_next_element(self, last_click_pos, next_pos, timeout=180, **kwargs):
        """
        等待下一个元素，没有出现就点击上一个
        :param timeout: 超时时间
        :param last_click_pos: 上一个需要点击的元素
        :param next_pos: 下一个元素
        :return:
        """
        pass

    @abstractmethod
    def wait_next_element_then_click(self, next_element, timeout=180, **kwargs):
        """
        等待下一个元素出现并点击
        :param timeout: 超时时间
        :param next_element: 上一个需要点击的元素
        :return:
        """
        pass

    @abstractmethod
    def wait_last_element_disappear(self, last_click_pos, last_pos, timeout=180, **kwargs):
        """
        等待上一个界面或元素消失，没有出现就点击上一个需要点击的元素
        :param timeout: 超时时间
        :param last_click_pos: 上一个需要点击的元素
        :param last_pos: 上一个元素
        :return:
        """
        pass

    @abstractmethod
    def get_text(self, pos=None):
        """
        :param pos: 元素
        :return:
        """
        pass

    @abstractmethod
    def snapshot(self):
        """
        与airtest的截图不同这是返回opencv格式的数组，并不会保存图片
        :return: numpy数组
        """
        pass

    def get_region_text(self, region=None, pos=None):
        """
        :param pos: 元素
        :param region: 设定区域
        :return:
        """
        pass

    @abstractmethod
    def fight(self, check_pos_list, attack_pos_list, other_button_list=None,
              check_stop_time=3, other_button_click_interval=3, appear=False, fight_time_out=0,
              attack_click_interval=0.01, **kwargs):
        """
        自动战斗
        :param check_pos_list: 用于停止判断的检测元素，与appear参数搭配使用
        :param appear:默认False, False为检测check_pos消失泽停止，True为检测存在则停止
        :param attack_pos_list: 需要点击的技能按钮列表，轮询点击
        :param other_button_list: 其他需要点击的按钮列表，会按列表顺序按一定间隔点击，点完后重新循环列表
        :param check_stop_time: 检查元素是否存在的时长
        :param other_button_click_interval:其他需要点击的元素，点击间隔, 默认3秒
        :param fight_time_out: 默认不会算超时结束，填写大于0的数后会超时自动退出
        :param attack_click_interval: 连续点击按钮的点击间隔
        :return:
        """
        pass

# class OperateClass:
#     def __init__(self, operate: OperateABC):
#         self.operate = operate
