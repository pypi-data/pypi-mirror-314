import os
import requests

from airtestProject import config
from airtest.utils.logger import get_logger

from airtestProject.manager.LogManager import LogManager, catch_error

"""
author liuhuatong
des 包管理模块
date 2024/4/29
"""


log_manager = LogManager()
class PackageManager:
    @catch_error
    @staticmethod
    def download_file(link, project=None):
        """根据链接下载包体
        :param link: 链接
        :return:
        """
        path = os.path.join(config.ROOT_PATH, "packages", project)
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, link.split("/")[-1])
        # 发起GET请求，设置stream=True开启流式传输
        with requests.get(link, stream=True) as response:
            if response.status_code == 200:
                # 打开一个文件进行二进制写操作
                with open(file_path, 'wb') as file:
                    # 指定chunk_size大小，逐块读取和保存文件
                    for chunk in response.iter_content(chunk_size=1024*8):
                        # 过滤掉keep-alive的新块
                        if chunk:
                            file.write(chunk)
                log_manager.log_step("{} 文件下载成功!".format(link))
            else:
                log_manager.log_step("{} 文件下载失败，状态码： {}".format(link, response.status_code))

    @catch_error
    def install_file(self, device_id, file_path, platform=None):
        """安装包体
        :param device_id: 设备id
        :param file_path: 包路径
        :param platform: 平台
        :return: Bool()
        """
        if not platform:
            result = os.popen('adb -s %s install -r %s' % (device_id, file_path)).read()
            log_manager.log_step('install_file {} {}'.format(device_id, result))
            if "success" in result.lower():
                return True
            else:
                return False
        else:
            result = os.popen('tidevice --udid %s install %s' % (device_id, file_path)).read()
            pass

    @catch_error
    def uninstall_file(self, device_id, package_name, platform=None):
        """卸载包体
        :param device_id: 设备id
        :param package_name: 包名字
        :param platform: 平台
        :return: Bool()
        """
        if not platform:
            result = os.popen('adb -s %s uninstall %s' % (device_id, package_name)).read()
            log_manager.log_step('uninstall_file {} {}'.format(device_id, result))
            if "success" in result.lower():
                return True
            else:
                return False
        else:
            result = os.popen('tidevice --udid %s uninstall %s' % (device_id, package_name)).read()
            pass
