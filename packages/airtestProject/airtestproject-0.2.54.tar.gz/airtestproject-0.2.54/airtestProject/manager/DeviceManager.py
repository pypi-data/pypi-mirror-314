import datetime
import os
import platform
import time

from airtestProject.airtest.cli.parser import cli_setup
from airtestProject.airtest.core.api import auto_setup, init_device
from airtestProject import config
from airtestProject.airtest.core.helper import G, device_platform
from airtestProject.airtest.core.settings import Settings as ST
from airtestProject.commons.utils.command import adb_shell
from airtestProject.commons.utils.report_util import ReportUtil
from airtestProject.commons.utils.tools import get_folder_path_up, find_case_parent_directory
from airtestProject.manager.LogManager import LogManager, catch_error

"""
author liuhuatong
des 设备状态管理控制
date 2024/4/29
"""

# state: no_connect/connect/occupation/free
DEVICE_INFO = {"320aa6ec": "小米mix2", "32883753": "小米11"}


def uwa_auto_setup():
    from airtest.core.helper import G as AG
    from airtest.core.helper import device_platform as AG_device_platform
    from airtest.core.settings import Settings as AST
    init_device(AG_device_platform(), AG.DEVICE.uuid)
    AG.LOGGER.set_logfile(None)
    ST.LOG_DIR = AST.LOG_DIR
    G.LOGGER.set_logfile(os.path.join(ST.LOG_DIR, ST.LOG_FILE))


class DeviceManager:
    def __init__(self):
        self.report_path = None
        self.logdir = None
        self.file_name = None
        self.file_path = None
        self.log_manager = LogManager("")

        self.devices = {}


    def auto_setup(self, file_path, device_ids=None, logdir=False):
        """Airtest 设备连接
        :param file_path: 脚本文件目录, 必传参数
        :param logdir: 是否开启日志
        :param device_ids: 设备id
        :return: 返回日志保存路径
        """

        if not file_path:
            self.file_path = __file__
        else:
            self.file_path = file_path
        self.file_name = os.path.basename(self.file_path).split('.')[0]

        project_root = os.getcwd()  # 获取脚本运行路径

        if logdir is True:
            logdir_path = get_folder_path_up(self.file_path, "logs")
            self.logdir = os.path.join(logdir_path, r"{}-{}.log".format(self.file_name,
                                                                        datetime.datetime.now()
                                                                        .strftime('%Y-%m-%d_''%H-%M-%S')))

        reports_patch = get_folder_path_up(self.file_path, "reports")
        self.report_path = os.path.join(reports_patch, r"reports.{}-{}"
                                        .format(self.file_name, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        if not device_ids:
            auto_setup(self.file_path, devices=[f"Android:///"], project_root=project_root, logdir=self.logdir)
            return self.logdir

        if isinstance(device_ids, str):
            device_ids = [device_ids]

        if not cli_setup():
            devices = []
            for i in device_ids:
                devices.append(f"android://127.0.0.1:5037/{i}?touch_method=MAXTOUCH&")
            auto_setup(self.file_path, devices=devices, project_root=project_root, logdir=self.logdir)
        return self.logdir

    def to_report(self, profile_report_dir=None):
        size = -1
        start_time = time.time()
        while time.time() - start_time < 60:
            if not os.path.exists(self.logdir):
                time.sleep(1)
                continue
            current_size = os.path.getsize(self.logdir)
            if current_size == size:
                break  # 文件大小没有变化，认为日志生成完毕
            else:
                size = current_size
                time.sleep(1)  # 等待一秒再次检查
        report = ReportUtil(script_root=self.file_path, log_root=self.logdir,
                            export_dir=self.report_path,
                            profile_report_dir=profile_report_dir,
                            logfile=self.logdir + r"\log.txt",
                            lang='zh',
                            plugins=None)
        report.report()

    @catch_error
    def get_free_devices(self):
        """获取空闲设备信息
        :return: {}
        """
        self.get_devices()

        free_devices = {}
        if not self.devices:
            return {}

        for device_id, value in self.devices.items():
            if value["state"] == "free":
                free_devices.update({device_id: value})
        return free_devices

    @catch_error
    def get_device_name(self, device_id=None):
        """根据设备id获取设备名字
        :param device_id: 设备id
        :return: {}
        """
        devices_name = None
        try:

            devices_name = adb_shell("getprop ro.product.model", device_id)
        except:
            pass

        return devices_name

    @catch_error
    def get_sdk_version(self, device_id=None):
        """获取设备sdk版本号
        :param device_id: 设备id
        :return: str()
        """
        if device_id not in self.devices and device_id != None:
            self.log_manager.log_step("{} 设备没有连接!".format(device_id))
            return None
        api_verison = int(adb_shell("getprop ro.build.version.sdk", device_id))
        return api_verison

    @catch_error
    def get_runing_package(self, device_id=None):
        """获取运行中的包名字
        :param device_id: 设备id
        :return: str()
        """
        if device_id not in self.devices and device_id != None:
            self.log_manager.log_step("{} 设备没有连接!".format(device_id))
            return None

        packages_list = adb_shell("dumpsys window | findstr mCurrentFocus", device_id)
        if "com" not in packages_list:
            return ""
        package = packages_list.split("/")[0].split(" ")[-1]
        return package

    @catch_error
    def filter_type(self):
        """根据不同平台选择出pipe 过滤的方法
        :return: str()
        """
        """Select the pipe filtering method according to the system"""
        filter_type = ('grep', 'findstr')[platform.system() == config.PLATFORM["Windows"]]
        return filter_type

    @catch_error
    def get_pid(self, device_id, pkg_name):
        """获取设备运行中的pkg的pid
        :param device_id: 设备id
        :param pkg_name: 包名
        :return: str()
        """
        try:
            if device_id not in self.devices:
                self.log_manager.log_step("{}设备没有连接".format(device_id))
                return ""
            sdk_version = self.get_sdk_version(device_id)
            self.log_manager.log_step("filter", self.filter_type())
            self.log_manager.log_step(
                os.popen(f"adb -s {device_id} shell ps -ef | {self.filter_type()} {pkg_name}").readlines())
            if sdk_version and int(sdk_version) < 26:
                result = os.popen(f"adb -s {device_id} shell ps | {self.filter_type()} {pkg_name}").readlines()
                process_list = [{'{}'.format(process.split()[1]): '{}'.format(process.split()[8])} for process in
                                result]
            else:
                result = os.popen(f"adb -s {device_id} shell ps -ef | {self.filter_type()} {pkg_name}").readlines()
                process_list = [{'{}'.format(process.split()[1]): '{}'.format(process.split()[7])} for process in
                                result]
            if len(process_list) == 0:
                self.log_manager.log_step('{}: no pid found'.format(pkg_name))
        except Exception as e:
            process_list = []
            self.log_manager.log_error(e)
        return process_list

    @catch_error
    def reboot(self, device_id):
        """重启设备
        :param device_id: 设备id
        :return:
        """
        if device_id not in self.devices:
            self.log_manager.log_step("{} 设备没有连接!".format(device_id))
            return None

        result = adb_shell("reboot", device_id)
        self.log_manager.log_step("{} {} 设备重启\n{}".format("reboot", device_id, result))
        return True


if __name__ == "__main__":
    d = DeviceManager()

    print(d.get_runing_package())
    print(d.get_pid("d1236ad8", "com.global.bcslg"))
    #
    # print(d.get_runing_package("320aa6ec"))
    # print(d.get_pid("320aa6ec", "com.global.bcslg.test"))
    # print(d.get_sdk_version("320aa6ec"))
    # print(d.get_sdk_version("32883753"))
