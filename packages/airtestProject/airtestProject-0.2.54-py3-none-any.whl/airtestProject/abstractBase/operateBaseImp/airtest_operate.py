"""
airtest核心api的二次封装，操作具体实现类
"""
import os
import queue
import asyncio

from airtestProject.airtest.core import api as air
from airtestProject.airtest.core.android import Android
from airtestProject.airtest.core.error import TargetNotFoundError
from airtestProject.airtest.core.helper import G, logwrap

from airtestProject.commons.utils.logger import log
from airtestProject.abstractBase.operate_base import OperateABC
import time

from airtestProject.commons.utils.my_template import MyTemplate
from airtestProject.commons.utils.ocr_template import OcrTemplate
from airtestProject.commons.utils.tools import get_folder_path_up


class MyAirTest(OperateABC):

    def __init__(self, language):
        super(MyAirTest, self).__init__()
        self.this_dict = None
        self.language = language

    def set_language(self, language):
        self.language = language

    def set_dict(self, script_root: str, project=None):
        """
        各种兼容还有路径转换。ps images文件夹只能在脚本的上级或者同级否则无法正常工作
        :param script_root: 脚本当前目录
        :param project: 定位到的具体图片文件夹
        :return:
        """
        if self.this_dict is None:
            files_dict = {}
            images_abs_path = get_folder_path_up(script_root, 'images')  # 获取图片文件夹的绝对路径
            # script_root_dir = os.path.dirname(script_root)  # 获取脚本文件夹的绝对路径
            # images_relative_path = os.path.relpath(images_abs_path, script_root_dir)  # 构造为图片文件夹的相对路径
            if project:
                images_project_relative_path = os.path.join(images_abs_path, project)  # 构造为图片文件夹和project的相对路径
            else:
                images_project_relative_path = images_abs_path
            # 遍历指定目录下的所有文件
            for filename in os.listdir(images_project_relative_path):
                file_path = os.path.join(images_project_relative_path, filename)
                if os.path.isfile(file_path):
                    file_name_without_ext, _ = os.path.splitext(filename)
                    files_dict[file_name_without_ext] = file_path
            print(files_dict)
            self.this_dict = files_dict

    def init_device(self, platform=None, uuid=None, **kwargs):
        try:
            air.init_device(platform=platform, uuid=uuid, **kwargs)
            log.info(f"init device success, platform: {platform}, uuid:  {uuid}")
        except Exception as e:
            log.error(f"failed to init device, platform: {platform}, uuid:  {uuid}")
            raise e

    def connect_device(self, uri):
        log.info('🍇 🍉 ready to connect device host ...')
        try:
            air.connect_device(uri)
            log.info(f'🍊 🍋 connect device succeeded... host: {uri}')
        except ConnectionError as e:
            log.error(f'connect device failed... host: {uri}')
            raise ConnectionError from e

    def device(self):
        current_active_device = air.device()
        log.info(f'get current active device: {current_active_device}')
        return current_active_device

    def set_current(self, idx):
        try:
            log.info(f"set current active device idx: {idx}")
            air.set_current(idx)
        except Exception as e:
            log.error(f"failed to set current active device idx: {idx}")
            raise e

    def auto_setup(self, basedir=None, devices=None, logdir=None, project_root=None, compress=None):
        air.auto_setup(basedir=basedir, devices=devices, logdir=logdir, project_root=project_root, compress=compress)

    def shell(self, cmd):
        try:
            log.info(f"execute adb shell command: {cmd}")
            return air.shell(cmd)
        except Exception as e:
            log.error(f"failed to execute adb shell command: {cmd}")
            raise e

    def start_app(self, package, activity=None):
        try:
            air.start_app(package, activity)
            log.info(f"start app: {package}, activity: {activity}")
        except Exception as e:
            log.error(f"failed start app {package}, activity: {activity}")
            raise e

    def stop_app(self, package):
        try:
            air.stop_app(package)
            log.info(f"stop the application on device, package: {package}")
        except Exception as e:
            log.error(f"failed to stop the application on device, package: {package}")
            raise e

    def clear_app(self, package):
        try:
            air.clear_app(package)
            log.info(f"clear data of the application on device, package: {package}")
        except Exception as e:
            log.error(f"failed to clear data of the application on device, package: {package}")
            raise e

    def install(self, filepath, **kwargs):
        try:
            log.info(f"install application: {filepath}")
            return air.install(filepath, **kwargs)
        except Exception as e:
            log.error(f"failed to install application: {filepath}")
            raise e

    def uninstall(self, package):
        try:
            log.info(f"uninstall application: {package}")
            return air.uninstall(package)
        except Exception as e:
            log.error(f"failed to uninstall application: {package}")
            raise e

    def snapshot(self, quality=None, max_size=None):
        try:
            return G.DEVICE.snapshot()
        except Exception as e:
            log.error(f"failed to wake up and unlock the device")
            raise e

    def wake(self):
        try:
            log.info(f"wake up and unlock the device")
            return air.wake
        except Exception as e:
            log.error(f"failed to wake up and unlock the device")
            raise e

    def home(self, package):
        raise NotImplementedError

    def click(self, pos, times=1, rgb=False, translucent=False, ocr_plus=False, ocr_match_type=False, **kwargs):
        try:
            log.info(f"perform the touch action on the device screen, pos: {pos}")
            kwargs.pop('focus', None)
            kwargs.pop('sleep_interval', None)
            value = self._check_value(pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus,
                                      ocr_match_type=ocr_match_type)
            return air.touch(value, times, **kwargs)
        except Exception as e:
            log.error(f"failed to perform the touch action on the device screen, pos: {pos}")
            raise e

    def _click_nolog(self, pos, times=1, ocr_plus=False, ocr_match_type=False, rgb=False, translucent=False, **kwargs):
        try:
            log.info(f"click_nolog  pos: {pos}")
            kwargs.pop('focus', None)
            kwargs.pop('sleep_interval', None)
            value = self._check_value(pos, ocr_plus, rgb=rgb, translucent=translucent, ocr_match_type=ocr_match_type)
            return air.touch_nolog(value, times, **kwargs)
        except Exception as e:
            log.error(f"failed to perform the touch action on the device screen, pos: {pos}")
            raise e

    def double_click(self, v1, v2=None, vector=None, **kwargs):
        log.info(f"perform double click")
        return air.double_click(v1, v2, vector, **kwargs)

    def swipe(self, value, v2=None, vector_direction=None, ocr_plus=False, ocr_match_type=False,
              rgb=False, translucent=False, **kwargs):
        kwargs.pop('duration', None)
        kwargs.pop('focus', None)
        if vector_direction is None:
            vector_direction = [0, -3.0]
        log.info("Perform the swipe action on the device screen.")
        value = self._check_value(value, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type,
                                  rgb=rgb, translucent=translucent)
        if v2 is not None:
            v2 = self._check_value(v2, ocr_plus=ocr_plus, rgb=rgb, translucent=translucent, ocr_match_type=ocr_match_type)
        return air.swipe(value, v2, vector=vector_direction, **kwargs)

    def swipe_along(self, pos, coordinates_list, duration=0.8, step=5, rgb=False, translucent=False):
        if isinstance(pos, tuple) or isinstance(pos, list):
            first_pos = pos
        else:
            first_pos = self.exists(pos, rgb=rgb, translucent=translucent)
        coordinates_list.insert(0, first_pos)
        if isinstance(air.device(), Android):
            air.device().swipe_along(coordinates_list, duration, step=step)
            return True
        else:
            raise TypeError("Device is not an Android device")

    def swipe_plus(self, value, v2=None, down_event_sleep=None, vector_direction=None, ocr_plus=False, rgb=False,
                   translucent=False, ocr_match_type=False, **kwargs):
        value = self._check_value(value, ocr_plus=ocr_plus, rgb=rgb, translucent=translucent,
                                  ocr_match_type=ocr_match_type)
        if isinstance(value, (MyTemplate, OcrTemplate)):
            pos1 = air.exists(value)
            if pos1:
                print(pos1)
            else:
                raise TargetNotFoundError(value)
        else:
            pos1 = value
        if v2:
            v2 = self._check_value(v2, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type, rgb=rgb, translucent=translucent)
            if isinstance(v2, (MyTemplate, OcrTemplate)):
                pos2 = air.exists(v2)
                if pos2 is False:
                    raise TargetNotFoundError(v2)
            else:
                pos2 = v2
            print(pos2)
        elif vector_direction:
            if vector_direction[0] <= 1 and vector_direction[1] <= 1:
                w, h = G.DEVICE.get_current_resolution()
                vector_direction = (int(vector_direction[0] * w), int(vector_direction[1] * h))
            pos2 = (pos1[0] + vector_direction[0], pos1[1] + vector_direction[1])
        else:
            raise Exception("no enough params for swipe")
        if isinstance(air.device(), Android):
            air.device().swipe_plus(pos1, pos2, down_event_sleep, **kwargs)
            return True
        else:
            raise TypeError("Device is not an Android device")

    def pinch(self, in_or_out='in', percent=0.5, center=None):
        log.info(f"perform the pinch action on the device screen")
        return air.pinch(in_or_out, center, percent)

    def keyevent(self, keyname, **kwargs):
        log.info(f"perform key event keyname: {keyname} on the device.")
        return air.keyevent(keyname, **kwargs)

    def set_text(self, pos=None, text=None, enter=True, rgb=False, translucent=False, **kwargs):
        try:
            self.click(pos, rgb=rgb, translucent=translucent)
            log.info(f"input {text} on the target device")
            for i in range(20):
                air.keyevent("KEYCODE_DEL")
                log.info(f"我在删除")
            return air.text(text, enter, **kwargs)
        except Exception as e:
            log.error(f"failed to input {text} on the target device")
            raise e

    def sleep(self, secs=1.0):
        time.sleep(secs)
        log.info(f'time sleep {secs} seconds')

    def wait(self, pos, timeout=None, interval=0.5, ocr_plus=False, intervalfunc=None, rgb=False, translucent=False,
             ocr_match_type=False,
             **kwargs):
        try:
            pos = self._check_value(pos, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type, rgb=rgb,
                                    translucent=translucent)
            return air.wait(pos, timeout, interval, intervalfunc)
        except Exception as e:
            log.warn(f"failed to input {pos} on the target device")
            return False

    def _wait_nolog(self, pos, timeout=None, interval=0.5, ocr_plus=False, intervalfunc=None, rgb=False,
                    translucent=False, ocr_match_type=False, **kwargs):
        try:
            pos = self._check_value(pos, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type, rgb=rgb,
                                    translucent=translucent)
            return air.wait_nolog(pos, timeout, interval, intervalfunc)
        except Exception as e:
            log.warn(f"failed to input {pos} on the target device")
            return False

    def wait_disappear_element(self, pos, timeout=180, rgb=False, translucent=False, ocr_plus=False,
                               ocr_match_type=False):
        start_loading_time = time.time()
        while self.exists(pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus,
                          ocr_match_type=ocr_match_type) is not False:
            if time.time() - start_loading_time > timeout:
                log.info(f"{pos}存在超时，请注意查看")
                return False
        log.info(f"{pos}消失")
        return True

    def wait_element_appear(self, pos, timeout=180, rgb=False, translucent=False, ocr_plus=False, ocr_match_type=False):
        start_loading_time = time.time()
        while self.exists(pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus,
                          ocr_match_type=ocr_match_type) is False:
            if time.time() - start_loading_time > timeout:
                log.info(f"{pos}寻找超时，请注意查看")
                return False
        log.info(f"{pos}出现")
        return True

    def exists(self, pos, ocr_plus=False, ocr_match_type=False, rgb=False, translucent=False):
        try:
            pos = self._check_value(pos, ocr_plus, rgb=rgb, translucent=translucent, ocr_match_type=ocr_match_type)
            return air.exists(pos)
        except Exception as e:
            log.error(f"the node: {pos} not exists.")
            raise e

    def persistent_element_exists(self, pos):
        pass

    def wait_for_any(self, pos_list: list, timeout=30, rgb=False, translucent=False,
                     ocr_plus=False, ocr_match_type=False):
        """

        :param ocr_plus: 是否开启二值化f
        :param translucent: 是否为半透
        :param rgb: 开启色值判断
        :param pos_list: 需要等待的列表元素
        :param timeout: 超出时长
        :return:
        """
        start = time.time()
        while True:
            for pos in pos_list:
                if self.exists(pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type):
                    return pos
            if time.time() - start > timeout:
                raise TargetNotFoundError(f'any to appear{pos_list}')

    def wait_for_all(self, pos_list: list, timeout=30, rgb=False, translucent=False, ocr_plus=False,
                     ocr_match_type=False):
        start = time.time()
        while True:
            all_exist = True
            for pos in pos_list:
                if not self.exists(pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus,
                                   ocr_match_type=ocr_match_type):
                    all_exist = False
                    break
            if all_exist:
                return
            if time.time() - start > timeout:
                raise TargetNotFoundError(f'all to appear{pos_list}')

    def wait_next_element(self, last_click_pos, next_pos, timeout=180, rgb=False, translucent=False,
                          ocr_plus=False, ocr_match_type=False):
        """
        等待下一个元素出现
        :param ocr_plus: 开启二值化
        :param timeout: 超时时间
        :param last_click_pos: 需要点击的元素
        :param next_pos: 将会出现的元素
        :param translucent: 是否为半透
        :param rgb: 开启色值判断
        :param ocr_match_type: 匹配类型True为模糊匹配，默认为False
        :return:
        """
        start_time = time.time()
        last_click_pos_staging = None
        while self.exists(next_pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus,
                          ocr_match_type=ocr_match_type) is False:
            log.info(f"{next_pos}没有出现正在尝试点击")
            if last_click_pos_staging is None:
                last_click_pos_staging = self.click(last_click_pos, rgb=rgb, translucent=translucent,
                                                    ocr_plus=ocr_plus, ocr_match_type=ocr_match_type)
            else:
                self.click(last_click_pos_staging)
            air.sleep(0.8)
            if time.time() - start_time > timeout:
                log.info(f"{next_pos}没有出现")
                return False
        return True

    def wait_next_element_then_click(self, next_element, timeout=180, rgb=False, translucent=False,
                                     ocr_plus=False, ocr_match_type=False):
        start_time = time.time()
        while True:
            next_pos = self.exists(next_element, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus,
                                   ocr_match_type=ocr_match_type)
            if next_pos is not False:
                break
            if time.time() - start_time > timeout:
                log.info(f"{next_pos}没有出现")
                return False
        return self.click(next_pos)

    def wait_last_element_disappear(self, last_click_pos, last_pos, timeout=180, rgb=False, translucent=False,
                                    ocr_plus=False, ocr_match_type=False):
        start_time = time.time()
        last_click_pos_2 = None
        while self.exists(last_pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type):
            log.info(f"{last_pos}没有消失正在尝试点击")
            if last_click_pos_2 is None:
                last_click_pos_2 = self.click(last_click_pos, rgb=rgb, translucent=translucent, ocr_plus=ocr_plus, ocr_match_type=ocr_match_type)
            else:
                self.click(last_click_pos_2)
            air.sleep(0.5)
            if time.time() - start_time > timeout:
                log.info(f"{last_pos}没有消失")
                return False
        return True

    def get_text(self, pos=None):
        if pos is not None:
            return OcrTemplate().find_text(pos)
        else:
            image = G.DEVICE.snapshot()
            return OcrTemplate().find_text(image)

    @logwrap
    def fight(self, check_pos_list, attack_pos_list, other_button_list=None, check_stop_time=3,
              other_button_click_interval=3, appear=False, fight_time_out=0, attack_click_interval=0.01,
              ocr_match_type=False):
        check_pos_list = [check_pos_list] if not isinstance(check_pos_list, list) else check_pos_list
        asyncio.run(self._async_fight(check_pos_list, attack_pos_list, other_button_list,
                                      check_stop_time, other_button_click_interval, appear,
                                      fight_time_out, attack_click_interval, ocr_match_type))

    def _check_value(self, val, ocr_plus=False, ocr_match_type=False, threshold=0.7, translucent=False, rgb=False):
        """
        用于判定是否是可以直接使用字典取值。如果不可以判断是否为文件夹路径是的话采用图片识别
        :param rgb: 图像识别是否开启rgb对比
        :param translucent: 图像识别是否半透
        :param threshold: 图像识别匹配阈值
        :param ocr_plus: 主要用于传递是否开启增强识别(不一定增强)
        :param ocr_match_type: 改变ocr的识别方式
        :param val: 需要检查的参数
        :return:
        """
        if isinstance(val, str):
            # 先判断是否为文件路径
            if os.path.isfile(val):
                return MyTemplate(val, threshold=threshold, rgb=rgb, translucent=translucent)

            dict_value = self.this_dict.get(val) if self.this_dict else None

            if dict_value is not None:
                return MyTemplate(dict_value, threshold=threshold, rgb=rgb, translucent=translucent)

            return OcrTemplate(val, language=self.language, ocrPlus=ocr_plus, match_type=ocr_match_type)

        return val

    def get_region_text(self, region=None, pos=None):
        if pos is not None:
            return OcrTemplate().find_region_text(pos, region)
        else:
            image = G.DEVICE.snapshot()
            return OcrTemplate().find_region_text(image, region)

    async def _async_fight(self, check_pos_list, attack_pos_list, other_button_list,
                           check_stop_time, other_button_click_interval, appear, fight_time_out, attack_click_interval, ocr_match_type):
        fight_stop_even = asyncio.Event()
        tasks = [asyncio.to_thread(self._attack, attack_pos, fight_stop_even, attack_click_interval) for attack_pos in attack_pos_list]
        if other_button_list is not None:
            tasks.append(asyncio.to_thread(self._click_other_button, other_button_list,
                                           fight_stop_even, other_button_click_interval))
        tasks.append(asyncio.to_thread(self._check_stop_fight, check_pos_list, fight_stop_even, check_stop_time, appear,
                                       fight_time_out, ocr_match_type))
        await asyncio.gather(*tasks)

    def _check_stop_fight(self, check_pos_list, fight_stop_even, check_stop_time, appear, fight_time_out, ocr_match_type):
        this_time = time.time()
        while not fight_stop_even.is_set():
            if fight_time_out > 0:
                if int(time.time() - this_time) >= fight_time_out:
                    fight_stop_even.set()
            else:
                for check_pos in check_pos_list:
                    result = self._wait_nolog(check_pos, timeout=check_stop_time, ocr_match_type=ocr_match_type)
                    if (not appear and not result) or (appear is True and result):
                        fight_stop_even.set()
                        break

    def _attack(self, attack_pos, fight_stop_even, attack_click_interval):
        while not fight_stop_even.is_set():
            self._click_nolog(attack_pos)
            time.sleep(attack_click_interval)

    def _click_other_button(self, other_button_list, fight_stop_even, other_button_click_interval):
        change_people_pos_que = queue.Queue()
        already_click_deque = queue.Queue()
        for pos in other_button_list:
            change_people_pos_que.put(pos)
        while not fight_stop_even.is_set():
            time.sleep(other_button_click_interval)
            if not change_people_pos_que.empty():
                change_pos = change_people_pos_que.get()
                self._click_nolog(change_pos)
                already_click_deque.put(change_pos)
            elif not already_click_deque.empty():
                change_people_pos_que.queue.extend(already_click_deque.queue)
                already_click_deque.queue.clear()


if __name__ == '__main__':
    air.sleep()
