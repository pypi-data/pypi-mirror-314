"""
这里准备用来解析Excel表，生成py测试用例的逻辑
"""
import os.path
import time
import genaratePy

from airtestProject import config

full_case_path_list = []

def ganerate_test_case(project="zg", page=0):
    test_case_data = genaratePy.parse_excel(project=project, page=page)

    def _format_param(param):
        if isinstance(param, str):
            return f'"{param}"'
        elif isinstance(param, int):
            return param

    for key, vals in test_case_data.items():
        class_name_context = ('#!/usr/bin/python\n'
                              '# coding:utf-8\n'
                              'import unittest\n'
                              'from airtest.core.api import *\n'
                              'from poco.drivers.unity3d import UnityPoco\n'
                              'from airtestProject import config\n'
                              'from airtestProject.commons.cases.appStart import AppStartCase\n'
                              'from airtestProject.commons.utils.utils import Utils\n'
                              'import threading\n'
                              'import time\n'
                              'from airtestProject.commons.manager.LogManager import LogManager\n'
                              'log_manager = LogManager(logfile=None)\n'
                              'class ' + key + '(AppStartCase):\n'
                              )
        def_init = ('    poco = None\n'
                    '    utils = None\n'
                    '    @classmethod\n'
                    '    def setUp(cls):\n'
                    '        super().setUpClass()\n'
                    '        # log_manager.log_step(f"执行启动APP方法，包名{APP_NAME}")\n'
                    '        # start_app(APP_NAME)\n'
                    '        time.sleep(config.START_APP_TIME)\n'
                    '        log_manager.log_step("实例化poco")\n'
                    '        cls.poco = UnityPoco()\n'
                    '        cls.poco1 = None\n'
                    '        # 用于多线程任务\n'
                    '        # time.sleep(15)\n'
                    '        log_manager.log_step(f"实例化utils：{config.ZG_APP_NAME}")\n'
                    '        cls.utils = Utils(config.ZG_APP_NAME, cls.poco)\n'
                    )
        def_tear_down = ('    @classmethod\n'
                         '    def tearDownClass(cls):\n'
                         '        log_manager.log_step("执行tearDownClass方法")\n'
                         '        log_manager.log_step("执行uwa_local_upload方法")\n'
                         '        cls.utils.uwa_local_upload(config.UWA_ACCOUNT,config.UWA_PASSWORD, 3600, 600)\n'
                         )
        create_file_path = os.path.join(config.ROOT_PATH, "cases", project)
        suffix = key + '.py'
        full_case_path = os.path.join(create_file_path, suffix)
        full_case_path_list.append(full_case_path)
        with open(full_case_path, 'w', encoding='utf-8') as f:
            f.write(class_name_context)
            f.write(def_init)

        for case_key, case_vals in vals.items():
            # 测试用例方法名
            def_test_case_method = ('    def %s(self):\n'
                                    '        log_manager.log_step("执行%s方法")\n') % (case_key, case_key)
            with open(full_case_path, 'a', encoding='utf-8') as f:
                f.write(def_test_case_method)
            for operate_key, operate_value in case_vals.items():
                case_context = ''
                # if len(operateValue) > 1:
                #     if isinstance(operateValue[0], int) or isinstance(operateValue[1], int):
                #         case_context = '        self.utils.%s("%s","%s")\n' % (
                #             operateKey, operateValue[0], operateValue[1])
                # else:
                #     if isinstance(operateValue[0], int):
                #         case_context = '        self.utils.%s(%s)\n' % (operateKey, operateValue[0])
                #     else:
                #         case_context = '        self.utils.%s("%s")\n' % (operateKey, operateValue[0])

                # 暂时按照utils中每个封装的方法来实现，另外一种思路是按照参数个数来分类实现也是可以的
                if operate_key == 'uwa_connect':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s:%s")\n'
                                    '        self.utils.%s("%s","%s")\n'
                                    '') % (
                                       operate_key, operate_value[0], operate_value[1], operate_key, operate_value[0],
                                       operate_value[1])
                elif operate_key == 'uwa_dump':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                    '        self.utils.%s("%s")\n') % (
                                       operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'uwa_tag':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                    '        self.utils.%s("%s")\n') % (
                                       operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'uwa_local_upload':
                    if len(operate_value) > 1:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s", %s)\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0],
                                           ', '.join(map(_format_param, operate_value[1:])))
                    else:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s")\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'poco_click':
                    if len(operate_value) > 1:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s:%s,%s")\n'
                                        '        self.utils.%s("%s","%s")\n') % (
                                           operate_key, operate_value[0], operate_value[1], operate_key,
                                           operate_value[0], operate_value[1])
                    else:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s")\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'poco_long_click':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s,%s")\n'
                                    '        self.utils.%s("%s",%s)\n') % (
                                       operate_key, operate_value[0], operate_value[1], operate_key, operate_value[0],
                                       operate_value[1])
                elif operate_key == 'poco_swipe':
                    if len(operate_value) > 1:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s", %s)\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0],
                                           ', '.join(map(_format_param, operate_value[1:])))
                    else:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s")\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'node_wait_for_appearance':
                    if len(operate_value) > 1:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s", %s)\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0],
                                           ', '.join(map(_format_param, operate_value[1:])))
                    else:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s")\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'node_wait_for_disappearance':
                    if len(operate_value) > 1:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s,%s")\n'
                                        '        self.utils.%s("%s",%s)\n') % (
                                           operate_key, operate_value[0], operate_value[1], operate_key,
                                           operate_value[0], operate_value[1])
                    else:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s")\n') % (
                                           operate_key, operate_value[0],
                                           operate_key, operate_value[0])
                elif operate_key == 'poco_dialog':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                    '        self.utils.%s("%s")\n') % (
                                       operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'poco_battle':
                    if len(operate_value) > 1:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s", %s)\n') % (
                                           operate_key, operate_value[0],
                                           operate_key, operate_value[0],
                                           ', '.join(map(_format_param, operate_value[1:])))
                    else:
                        case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                        '        self.utils.%s("%s")\n') % (
                                           operate_key, operate_value[0], operate_key, operate_value[0])
                elif operate_key == 'poco_use_skills':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s,%s,%s")\n'
                                    '        self.utils.%s("%s","%s","%s")\n') % (
                                       operate_key, operate_value[0], operate_value[1], operate_value[2], operate_key,
                                       operate_value[0], operate_value[1], operate_value[2])
                elif operate_key == 'sleep':
                    case_context = ('        log_manager.log_step("执行%s步骤，参数%s")\n'
                                    '        self.utils.%s(%s)\n') % (
                                       operate_key, operate_value[0], operate_key, operate_value[0])
                with open(full_case_path, 'a', encoding='utf-8') as f:
                    f.write(case_context)

        with open(full_case_path, 'a', encoding='utf-8') as f:
            f.write(def_tear_down)


def format_code_with_autopep8(file_path_list):
    import autopep8
    for file_path in file_path_list:
        print(file_path)
        with open(file_path, 'r+', encoding='utf-8') as f:
            source_code = f.read()
            formatted_code = autopep8.fix_code(source_code)
            f.seek(0)
            f.write(formatted_code)
            f.truncate()


if __name__ == '__main__':
    ganerate_test_case()
    format_code_with_autopep8(full_case_path_list)
