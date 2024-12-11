"""
基于poco对象、air二次封装的操作方法
"""
from airtestProject.commons.utils.exception import NoSuchNodeException
from airtestProject.poco.exceptions import PocoNoSuchNodeException, PocoTargetRemovedException
from airtestProject.abstractBase.operate_base import OperateABC

from airtestProject.poco.drivers.unity3d import UnityPoco
import re
import time
from airtestProject.airtest.core import api as air
from airtestProject.commons.utils.logger import log
import time

identifier: str = '-'
index_compile = re.compile(r'(?<=\[)\d+?(?=\\])')
input_type = "InputField"


class Page:

    def __init__(self, poco_instance):

        self.poco = poco_instance or UnityPoco()

    def get_poco(self, pos):
        return self.parser_pos(pos)

    def click(self, pos, focus=None, sleep_interval: float = None):
        try:
            return self.parser_pos(pos).click(focus, sleep_interval)
        except PocoNoSuchNodeException:
            try:
                log.debug(f"尝试再次点击： {pos}")
                return self.parser_pos(pos).click(focus, sleep_interval)
            except PocoNoSuchNodeException:
                raise NoSuchNodeException(f'找不到节点 "{pos}"')

    def exists(self, pos):
        try:
            return self.parser_pos(pos).exists()
        except (PocoTargetRemovedException, PocoNoSuchNodeException):
            return False

    def long_click(self, pos: str, duration: float = 2.0):
        return self.parser_pos(pos).long_click(duration)

    # def double_click(self, pos: str, focus=None, sleep_interval: float = None):
    #     return self.parser_pos(pos).double_click(focus, sleep_interval)
    #
    # def rclick(self, pos: str, focus=None, sleep_interval: float = None):
    #     return self.parser_pos(pos).rclick(focus, sleep_interval)

    def swipe(self, pos: str, direction, focus=None, duration: float = 0.5):
        return self.parser_pos(pos).swipe(direction, focus, duration)

    def scroll(self, pos: str, direction='vertical', percent: float = 0.6, duration: float = 2.0):
        return self.parser_pos(pos).scroll(direction, percent, duration)

    def pinch(self, pos: str, direction='in', percent: float = 0.6, duration: float = 2.0, dead_zone: float = 0.1):
        return self.parser_pos(pos).pinch(direction, percent, duration, dead_zone)

    def set_text(self, pos: str, text: str):
        pos = self.parser_pos(pos)
        if pos.attr("type") == input_type:
            return pos.set_text(text)
        else:
            pos.click()
            for i in range(20):
                self.keyevent("KEYCODE_DEL")
            self.text(text)

    def get_text(self, pos: str):
        return self.parser_pos(pos).get_text()

    def get_name(self, pos: str):
        return self.parser_pos(pos).get_name()

    def drag_to(self, pos: str, target: str, duration=0.5):
        return self.parser_pos(pos).drag_to(self.parser_pos(target), duration)

    def wait_for_any(self, pos_list: list, timeout=30):
        return self.poco.wait_for_any(self.parser_pos_list(pos_list), timeout)

    def wait_for_all(self, pos_list: list, timeout=30):
        return self.poco.wait_for_all(self.parser_pos_list(pos_list), timeout)

    def wait_for_appearance(self, pos, timeout=30):
        return self.parser_pos(pos).wait_for_appearance(timeout)

    def wait_for_disappearance(self, pos, timeout=30):
        return self.parser_pos(pos).wait_for_disappearance(timeout)

    def sleep(self, secs: float = 1.0):
        log.step(f"sleep {secs} seconds .")
        time.sleep(secs)

    def regex_pos_index(self, pos: str):
        """
        正则匹配定位的下标
        :param pos:
        :return:
        """
        s = index_compile.search(pos)
        if s:
            index = s.group()
            rep_pos = pos.replace(f"[{index}]", "")
            return rep_pos, int(index)
        return pos, 0

    def parser_pos(self, pos: str):
        """
        解析pos定位，基于poco定位方式，支持更简便的一行式书写定位方法，支持五种定位方法；
        传入的pos为中文时，使用text文本定位，不以中文开头不会匹配text文本；
        属性定位与正则定位属于同一种书写方式，均采用关键字方式书写，例如：text=确定、textMatches=确定；
        传入的pos为元素时，使用普通方式定位，并且当存在多级定位时，使用 - 符号连结，程序自动拆解，并自动解析index；
        相对定位与顺序定位可结合使用，采用先切割后取值的方式解析定位，例如：Bg_Front[1]-Close；
        :param pos: 定位
        :return:
        example：
            基本定位："Btn_Enter"
            顺序定位："Bg_Front[1]"
            相对定位: "Bg_Front[1]-Close"
            属性定位："text=确定"
            正则定位："textMatches=确定"
        """

        if '=' in pos:
            attr, pos = pos.split('=')
            return self.poco(**{attr: pos})

        if identifier not in pos:
            if index_compile.search(pos):
                rep_pos, index = self.regex_pos_index(pos)
                return self.poco(rep_pos)[index]

            return self.poco(pos)

        value_list = pos.split(identifier)
        pos_list = [self.regex_pos_index(value) for value in value_list]

        p0, n0 = pos_list[0]
        p1, n1 = pos_list[1]

        return self.poco(p0)[n0].child(p1)[n1]

    def parser_pos_list(self, pos_list: list):
        poco_list = []

        for pos in pos_list:
            poco_list.append(self.poco(pos))

        return poco_list

    def shell(self, cmd):
        try:
            log.info(f"启动远程shell并执行命令成功: {cmd}")
            return self.air.shell(cmd)
        except Exception as e:
            log.error(f"启动远程shell并执行命令失败: {cmd}")
            raise e

    def start_app(self, package, activity=None):
        try:
            self.air.start_app(package, activity)
            log.info(f"启动APP: {package}, activity: {activity}")
        except Exception as e:
            log.error(f"启动APP失败 {package}, activity: {activity}")
            raise e

    def stop_app(self, package):
        try:
            self.air.stop_app(package)
            log.info(f"停止APP, package: {package}")
        except Exception as e:
            log.error(f"停止APP失败, package: {package}")
            raise e

    def clear_app(self, package):
        try:
            self.air.clear_app(package)
            log.info(f"清除APP的数据, package: {package}")
        except Exception as e:
            log.error(f"清除APP的数据失败, package: {package}")
            raise e

    def snapshot(self, filename=None, msg="", quality=None, max_size=None):
        try:
            log.info(f"设备执行截图:{filename}.")
            return self.air.snapshot(filename, msg, quality, max_size)
        except Exception as e:
            log.error(f"设备执行截图失败")
            raise e

    def wake(self):
        try:
            log.info(f"设备执行滑动解锁")
            return self.air.wake
        except Exception as e:
            log.error(f"设备执行滑动解锁失败")
            raise e

    def home(self, package):
        raise NotImplementedError

    def touch(self, v, times=1, **kwargs):
        try:
            log.info(f"设备上执行点击, pos: {v}")
            return self.air.touch(v, times, **kwargs)
        except Exception as e:
            log.error(f"设备上点击失败, pos: {v}")
            raise e

    def double_click(self, v1, v2=None, vector=None, **kwargs):
        log.info(f"设备上执行双击")
        return self.air.double_click(v1, v2, vector, **kwargs)

    # def swipe(self,v1, v2=None, vector=None, **kwargs):
    #     log.info("设备上执行滑动")
    #     return self.air.swipe(v1, v2, vector, **kwargs)

    # def pinch(self,in_or_out='in', center=None, percent=0.5):
    #     log.info(f"设备上执行缩放")
    #     return self.air.pinch(in_or_out, center, percent)

    def keyevent(self, keyname, **kwargs):
        log.info(f"设备上执行: {keyname} 按键")
        return self.air.keyevent(keyname, **kwargs)

    def text(self, value, enter=True, **kwargs):
        try:
            log.info(f"输入 {value} ")
            return self.air.text(value, enter, **kwargs)
        except Exception as e:
            log.error(f"输入 {value} 失败")
            raise e

    def wait(self):
        raise NotImplementedError

    # def exists(self,v):
    #     try:
    #         log.info(f"节点: {v} 存在.")
    #         return self.air.exists(v)
    #     except Exception as e:
    #         log.error(f"节点: {v} 不存在.")
    #         raise e

