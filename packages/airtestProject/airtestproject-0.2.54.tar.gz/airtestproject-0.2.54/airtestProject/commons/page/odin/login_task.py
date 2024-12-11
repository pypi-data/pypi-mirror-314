"""
登录操作
"""
import random
import string

from random import choice

import numpy as np

from airtestProject.airtest.core.api import *
from airtestProject.commons.stateMachine.task_machine import check_func
from airtestProject.commons.utils.logger import log
from airtestProject.factory.OperateFactory import operate
from airtestProject.commons.stateMachine.task_machine import check_func, TaskCaseTemplate, put_task, stop_machine_f, \
    only_run_this, start_tag

reset_pos = [0, 0]

login_pos = 'btnLogin'  # 进入选择服务器界面
input_account_pos = "inputFieldAccountName"  # 输入账号
input_account_text_pos = "inputFieldAccountName-Text"  # 输入账号-文本
change_server_pos = "btnChangedServer"  # 选择服务器
enter_game_pos = "btnEnterGame"  # 进入选角界面
create_role_page = "CreateRoleView(Clone)"  # 创建角色界面
select_role_page = "SelectRoleView(Clone)"  # 选择角色界面
input_name_pos = "InputField"  # 输入创角名字
enter_pos = "Button_Enter"  # 进入游戏按钮
loading_page = "LoadingView(Clone)"  # 登陆界面
map_pos = "btnMinMap"  # 游戏内小地图按钮
tip_pos = "tipsLab"

pos_pos = "inputFieldAccountName"

all_role_pos = {"liuerlong": "0", "longnv": "1", "kuangzhanshi": "2", "tangsan": "3", "mahongjun": "4"}  # 角色按钮
gender_pos = {"male": 'Gender-Toggle', "female": 'Toggle (1)'}  # 性别按钮
account = ["luohaifeng", "luohaifeng02", "luohaifeng03", "test01", "test02", "test03", "test04", "test05", "test06",
           "test07", "test08", "test09"]  # 账号数据
all_server_pos = {"public": "0", "yuanyao": "1"}  # 服务器按钮


def r_user_name():
    # 生成一个包含所有文字的字符集
    chinese_chars = ''.join(chr(i) for i in range(0x4E00, 0x9FFF)) + \
                    ''.join(chr(i) for i in range(0x3400, 0x4DBF))
    english_chars = string.ascii_letters
    all_chars = chinese_chars + english_chars

    # 使用random.choice随机选择字符，生成指定长度的字符串
    random_string = ''
    for i in range(6):
        if random.randint(0, 1) == 0:
            random_string += random.choice(chinese_chars)
        else:
            random_string += random.choice(english_chars)
    return random_string


class LoginPage:
    def __init__(self, script_root, project=None, log_path=None):
        """

        :param project: 如果想采用命名代替文件夹路径的方法需要传入一个文件夹名让air生成对应字典。
        """
        if project is not None:
            operate("air").set_dict(script_root, project)
        if log_path is not None:
            self.log_path = log_path
        else:
            self.log_path = None

    @check_func("登录入口")
    def check_enter_login_view(self, pos, fun_name="air"):
        if operate(fun_name).wait_element_appear(pos, timeout=600):
            log.step("进入登录界面成功")
            return True
        else:
            log.step("进入登录界面失败")
            return False

    @check_func('输入账号')
    def input_account(self, account_pos, fun_name="air"):
        user = choice(account)
        operate(fun_name).set_text(account_pos, ''.join(str(random.randint(1, 9)) for _ in range(6)))
        log.step(f'输入账号-{user}')

    @check_func('点击登录')
    def click_login(self, login_button, into_game_btn, fun_name="air"):
        """

        :param login_button: 登陆按钮控件
        :param into_game_btn: 下一个页面要出现的元素
        :param fun_name: air或poco
        :return:
        """
        start_time = time.time()
        while operate(fun_name).exists(into_game_btn) is False:
            operate(fun_name).click(login_button)
            if time.time() - start_time > 120:
                log.step("疑似点击登录失败")
            operate(fun_name).sleep(2.0)

    @check_func('打开服务器列表')
    def open_server_list(self, change_server_pos, fun_name="air"):
        """

        :param change_server_pos:
        :param fun_name: air或poco
        :return:
        """
        for i in range(5):
            if operate(fun_name).exists(change_server_pos):
                operate(fun_name).click(change_server_pos)
                break
            else:
                log.error('找不到登录界面，尝试等待')
                operate(fun_name).sleep(1.0)
            operate(fun_name).sleep(1.0)

    @check_func('选择区服')
    def select_server(self, server_name, fun_name="air"):
        operate(fun_name).click(server_name, focus=reset_pos)
        operate(fun_name).sleep(1.0)

    @check_func('进入选角界面')
    def click_enter_game(self, enter_game_pos, fun_name="air"):
        """

        :param enter_game_pos: 进入游戏按钮
        :param fun_name: air或poco
        :return:
        """
        for i in range(3):
            if operate(fun_name).exists(enter_game_pos):
                operate(fun_name).click(enter_game_pos)
            else:
                return False
            operate(fun_name).sleep(2.0)

    def is_create_role(self, fun_name="air"):
        if operate(fun_name).exists(create_role_page):
            return True
        return False

    @check_func("选择角色")
    def select_role(self, role, fun_name="air"):
        operate(fun_name).click(role)

    @check_func("选择性别")
    def select_gender(self, gender, fun_name="air"):
        operate(fun_name).click(gender)

    @check_func('创建角色or选择角色')
    def create_role(self, create_role_page, select_role_page, role, gender,
                    input_name_pos, enter_game_pos, create_pos,
                    next_page_pos, fun_name="air"):
        """

        :param two_page_list: 双页面等待，任何一个页面出现都会执行一下步
        :param role: 要创建的角色
        :param gender: 要创建的性别
        :param fun_name: air或poco
        :return:
        """
        operate(fun_name).wait_for_any([create_role_page, select_role_page])
        bool = operate(fun_name).exists(create_role_page)
        log.step(f'是否未创角-{bool}')
        # random_name = factory.random_word()
        if bool:
            operate(fun_name).click(role, focus=reset_pos)
            operate(fun_name).click(gender, focus=reset_pos, ocr_plus=True)
            operate(fun_name).set_text(input_name_pos, r_user_name())
            operate(fun_name).sleep(1.0)
            log.step(f'创建角色-test')
            for i in range(3):
                if operate(fun_name).exists(next_page_pos) is False:
                    operate(fun_name).click(create_pos)
                    log.step('点击进入游戏')
                else:
                    break
        else:
            for i in range(3):
                if operate(fun_name).exists(next_page_pos) is False:
                    operate(fun_name).click(enter_game_pos)
                    log.step('点击进入游戏')
                else:
                    break

    @check_func('检查进入游戏结果')
    def check_enter_success(self, tip_pos, fun_name="air"):
        """

        :param tip_pos: loding页面存在的元素
        :param fun_name: air或poco
        :return:
        """
        if operate(fun_name).wait_disappear_element(tip_pos) is True:
            log.step('进入游戏成功')
            return True
        else:
            log.step('进入游戏失败')
            return False

    @check_func('检查重名')
    def check_name_taken(self, name_taken, ConfirmButton, fun_name="air"):
        for i in range(3):
            if operate(fun_name).exists(name_taken):
                operate(fun_name).click(ConfirmButton)
                log.step('有重名确认')
            else:
                log.step('无重名')
                break

    def odin_login(self):
        self.check_enter_login_view(login_pos, "poco")
        self.input_account(input_account_pos, "poco")
        self.click_login(login_pos, change_server_pos, "poco")
        self.open_server_list(change_server_pos, "poco")
        self.select_server(all_server_pos["public"], "poco")
        self.click_enter_game(enter_game_pos, "poco")
        self.create_role(create_role_page, select_role_page, create_role_page, all_role_pos['tangsan']
                         , gender_pos['male'], input_name_pos, enter_pos, enter_pos, tip_pos, "poco")
        # self.check_login_success()
        if self.check_enter_success(tip_pos, "poco"):
            return True


class OdinLogin(TaskCaseTemplate):
    def __init__(self, script_root, project=None):
        super(OdinLogin, self).__init__()
        self.obj = LoginPage(script_root, project)

    def odin_login_air(self):
        self.obj.check_enter_login_view("LoginBtn")
        self.obj.input_account("AccountInputBox")
        self.obj.click_login("LoginBtn", "ZoneChangeButton")
        self.obj.open_server_list("ZoneChangeButton")
        self.obj.select_server("Odin外网共公服")
        self.obj.click_enter_game("EnterGame")
        self.obj.create_role("CreateRole", "EnterGame (SelectCharacter)", "马红俊", "女",
                             "NameTxt", "EnterGame (SelectCharacter)", "CreateRole", "WaitingBar")
        self.obj.check_name_taken("name_taken", 'ConfirmButton', )
        if self.obj.check_enter_success("WaitingBar"):
            return True


if __name__ == '__main__':
    # poco("inputFieldAccountName").set_text("fdshj")
    # connect_device("Android:///e7970f92")
    # odin_login_air()
    print(r_user_name())
