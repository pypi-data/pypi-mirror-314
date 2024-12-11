# -*- encoding=utf8 -*-
import re

from airtestProject.poco.exceptions import PocoTargetTimeout

from airtestProject.commons.UWA import *
from airtestProject.manager.LogManager import LogManager


class Utils:

    def __init__(self, package_name, poco, project):
        self.log_manager = LogManager(logfile=None,project=project)

        # todo 实例化poco前需要确保游戏已经稳定启动
        self.log_manager.log_step(f"实例化Utils{str(type(poco))}")
        self.package_name = package_name
        self.poco = poco

    def uwa_connect(self, modle, projectId):
        """
        连接uwa
        :param modle: uwa的录制模式
        :param projectId: 项目ID，可以从uwa项目中查看
        :return:TRUE/False
        """
        time.sleep(20)
        self.log_manager.log_subprocess('uwa_dump', modle, projectId)
        if modle is not None and modle != 'default' and projectId is not None:
            self.log_manager.log_step("GOT测试=》connect")
            GOT_Test.Connect(self.poco)
            self.log_manager.log_step("GOT测试=》start=》modle={}".format(modle))
            GOT_Test.Start(self.poco, modle)
            return True
        return False

    def uwa_dump(self, dumpType):
        """
        手动 dump，采集更多信息
        :param poco: poco实例对象
        :param dumpType: dump的类型，可用dump类型：mono/lua/resources/overdraw，类型为String
        :Example:
            >>> Utils.uwa_dump('overdraw')
        """
        dump = ['mono', 'lua', 'resources', 'overdraw']
        self.log_manager.log_subprocess('uwa_dump', dumpType)
        if dumpType not in dump:
            self.log_manager.log_step("执行GOT_Test.Dump方法{}".format(dumpType))
            GOT_Test.Dump(self.poco, dumpType)
            return True
        self.log_manager.log_error("执行uwa_dump方法，参数错误{}".format(dumpType))
        return False

    def uwa_tag(self, tag):
        """
        打tag标签
        :param poco: poco实例对象
        :param tag:区间标记
        :return:
        """
        self.log_manager.log_step("执行GOT_Test.Tag方法{}".format(tag))
        GOT_Test.Tag(self.poco, tag)

    def uwa_local_upload(self, account, password, timeLimits=3600, uploadTimeLimits=600):
        """
        上传本地uwa数据
        :param poco: poco实例化对象
        :param account: uwa账户名
        :param password: uwa账户密码
        :param timeLimits:测试时长限制，默认3600秒（1个小时）
        :param uploadTimeLimits:数据上传超时限制600秒
        :return:
        """
        self.log_manager.log_subprocess('uwa_local_upload', account, password, timeLimits, uploadTimeLimits)
        self.log_manager.log_step("执行GOT_Test.Stop方法")
        GOT_Test.Stop(self.poco)
        self.log_manager.log_step('执行GOT_Test.LocalUpload方法{}'.format(account, password, timeLimits, uploadTimeLimits))
        GOT_Test.LocalUpload(self.poco, account, password, timeLimits, uploadTimeLimits)
        self.log_manager.log_step('上传成功！执行stop_app方法{}'.format(self.package_name))
        stop_app(self.package_name)

    @logwrap
    def poco_click(self, node, index=0):
        """
        节点点击
        :param index: 是否有多个相同的node节点，如果有则填下标：
        eg:
        airtest中抓到node节点有3个相同的节点,需要获取第二个节点
        item_button
        item_button
        item_button
        >>> Utils.poco_click('item_button',1)
        :param node:poco节点
        :param index:相同节点的下标，从0开始
        :return:
        """
        pattern = r"image\d+\.png"
        match = re.search(pattern, node)
        if match:
            if exists(Template(node)):
                touch(Template(node))
            else:
                self.log_manager.log_step("{} 不存在，点击失败!".format(node))
        else:
            try:
                if '=' in node:
                    self.log_manager.log_step('节点包含=号：' + node)
                    poco_key = node.split('=')[0].strip()
                    poco_value = node.split('=')[1].strip().strip('"')
                    attr_dict = {poco_key: poco_value}
                    if not self.poco(attr_dict).exists():
                        return
                    self.log_manager.log_step('点击{}:{}节点'.format_map(attr_dict))
                    self.poco(**attr_dict).click()
                    return
                else:
                    if not self.poco(node).exists():
                        self.log_manager.log_error("节点{}不存在".format(node))
                        return
                    if index == 0:
                        self.log_manager.log_step('点击无相同元素的节点{}'.format(node))
                        # poco(node).get_position()得到的数据是[x,y]数组
                        # click(tuple(self.poco(node).get_position()))
                        self.poco(node).click(self.poco(node).get_position())
                        return
                    self.log_manager.log_step('点击有多个相同元素的节点,点击第{}个{}节点'.format(index, node))
                    self.poco(node)[index].click()
                    return
            except:
                self.log_manager.log_error("poco_click方法执行失败，节点为{}".format(node))

    def poco_long_click(self, node, seconds=3):
        """
        # 存在就点击
        :param node: 点击节点
        :param seconds: 长按时长(秒)
        :return:
        """
        try:
            self.log_manager.log_subprocess('poco_long_click', node, seconds)
            cur_node = self.poco(node)
            cur_node.long_click(duration=seconds)
        except:
            self.log_manager.log_error("执行poco_long_click方法错误，节点{}".format(node))

    def poco_swipe(self, node, direction=0, offset=0.3, duration=0.5):
        """
        滑动&长按
        :param duration: 持续时间，默认0.5,如果是长按
        :param direction: 滑动方向：0,1,2,3分别表示水平向右，水平向左，垂直向下，垂直向上
        :param node: uwa节点
        :param offset: 偏移量
        :return:
        """
        self.log_manager.log_subprocess('poco_swipe', node, direction, offset, duration)
        _pos = self.poco(node).get_position()
        # 正反方向水平滑动
        forward_pos = (_pos[0] + offset, 0)
        opposite_pos = (_pos[0] - offset, 0)
        # 上下方向垂直滑动
        down_pos = (0, _pos[1] - offset)
        up_pos = (0, _pos[1] + offset)
        other_pos = (_pos[0] + offset, _pos[1] + offset)
        if direction == 0:
            # 水平向右
            self.log_manager.log_step('向右滑动节点{}'.format(node))
            swipe(_pos, vector=forward_pos, duration=duration)
        elif direction == 1:
            self.log_manager.log_step('向左滑动节点{}'.format(node))
            swipe(_pos, vector=opposite_pos, duration=duration)
        elif direction == 2:
            self.log_manager.log_step('向下滑动节点{}'.format(node))
            swipe(_pos, vector=down_pos, duration=duration)
        elif direction == 3:
            self.log_manager.log_step('向上滑动节点{}'.format(node))
            swipe(_pos, vector=up_pos, duration=duration)
        else:
            self.log_manager.log_step('其他方向滑动节点{}'.format(node))
            swipe(_pos, vector=other_pos, duration=duration)

    def node_wait_for_appearance(self, target_node, timeout=120):
        """
        等待元素出现
        :param poco: poco实例化
        :param target_node: 目标节点
        :param timeout: 持续时间
        :return:
        """
        self.log_manager.log_subprocess("node_wait_for_appearance", target_node, timeout)
        if '=' in target_node:
            self.log_manager.log_step('节点包含=号：' + target_node)
            poco_key = target_node.split('=')[0].strip()
            poco_value = target_node.split('=')[1].strip().strip('=')
            attr_dict = {poco_key: poco_value}
            start = time.time()
            log(attr_dict)
            temp_node = self.poco(**attr_dict)
            while not temp_node.exists():
                time.sleep(2)
                temp_node = self.poco(**attr_dict)
                log(temp_node)
                if time.time() - start > timeout:
                    self.log_manager.log_error('等待超时，节点{}'.format(target_node))
                    raise PocoTargetTimeout('appearance', self)
            position = temp_node.get_position()
            if position[0] > 1 or position[1] > 1:
                # 如果坐标位置超过1，则说明元素在屏幕外，可以忽略
                self.log_manager.log_error('{}节点坐标位置在屏幕外'.format(temp_node))
                return
            return temp_node
        else:
            start = time.time()
            while not self.poco(target_node).exists():
                self.log_manager.log_step('等待元素{}出现'.format(str(self.poco(target_node).exists())))
                # position = self.poco(**attr_dict).get_position
                time.sleep(2)
                if time.time() - start > timeout:
                    self.log_manager.log_error('等待超时，节点{}'.format(target_node))
                    raise PocoTargetTimeout('disappearance', self)
            return self.poco(target_node)

    def node_wait_for_disappearance(self, target_node, timeout=120):
        """
        # 等待元素消失
        :param poco:poco实例化
        :param target_node: 目标节点
        :param timeout: 超时时间
        :return:
        """
        self.log_manager.log_subprocess('node_wait_for_disappearance', target_node, timeout)
        if '=' in target_node:
            poco_key = target_node.split('=')[0].strip()
            poco_value = target_node.split('=')[1].strip().strip('=')
            attr_dict = {poco_key: poco_value}
            start = time.time()
            while self.poco(**attr_dict).exists():
                # position = self.poco(**attr_dict).get_position
                time.sleep(2)
                if time.time() - start > timeout:
                    self.log_manager.log_error('等待元素消失步骤，等待超时{}:{}'.format_map(attr_dict))
                    raise PocoTargetTimeout('disappearance', self)
            # if position[0] > 1 or position[1] > 1:
            #     # 如果坐标位置超过1，则说明元素在屏幕外，可以忽略
            #     return True
        else:
            start = time.time()
            while self.poco(target_node).exists():
                # position = self.poco(**attr_dict).get_position
                time.sleep(2)
                if time.time() - start > timeout:
                    self.log_manager.log_error('等待元素消失步骤，等待超时{}:{}'.format_map(target_node))
                    raise PocoTargetTimeout('disappearance', self)
        return True

    def poco_dialog(self, node):
        """
        剧情对话点击
        :param node:对话节点
        :return:
        """
        self.log_manager.log_subprocess('poco_dialog', node)
        dialog_node = self.poco(node)
        # todo 这里可能出现判断失败的情况，需要后续观察
        while dialog_node.exists():
            self.log_manager.log_step('对话节点存在{}'.format(node))
            self.log_manager.log_step('点击对话节点{}'.format(node))
            self.poco_click(node)
            sleep(2)
        # return

    def poco_battle(self, skill_node, stop_node):
        """
        战斗逻辑：进入战斗后
        :param stop_node:停止的节点，用来判断是否需要停止战斗的节点
        :param skill_node:使用技能的节点
        :return:
        """
        self.log_manager.log_subprocess('poco_battle', skill_node, stop_node)
        use_skill = self.poco(skill_node)
        stop = self.poco(stop_node)
        while stop.exists():
            time.sleep(1)
            # 检查攻击目标UI是否存在，不存在可能怪物已死
            btn_search_and_lock = self.poco('btnSearchAndLock')
            if btn_search_and_lock:
                # 连击3次
                self.poco(use_skill)
                self.poco(use_skill)
                self.poco(use_skill)
                # 如果死亡了
                # btnReviveNormal =
            else:
                btn_search_and_lock.click()
                time.sleep(1)
                self.poco(use_skill)
                self.poco(use_skill)
                self.poco(use_skill)
            stop = self.poco(stop_node)
        stop.click()
        # return True

    def poco_use_skills(self, skill_nodes, task_node="", cur_task_name=""):
        """
        # 攻击
        :param skill_nodes: 
        :param cur_task_name: 
        :param task_node: 
        :param skill_node:技能节点列表([])
        :return:
        """

        log(skill_nodes)

        cur_task = self.poco(task_node)
        while cur_task.attr("text") == cur_task_name:
            btn_search_and_lock = self.poco('btnSearchAndLock')

            if not btn_search_and_lock:
                self.poco_click("attackSkill")
                self.poco_click('btnSearchAndLock')

            if len(skill_nodes) == 1:
                self.poco_long_click(skill_nodes[0], t=3)
            else:
                for i, node in enumerate(skill_nodes[1:]):
                    log("攻击技能", node)
                    self.poco_click(node)
                    self.poco_long_click(skill_nodes[0], t=3)
            cur_task = self.poco(task_node)
            print(cur_task.attr("text"), cur_task_name)


    def sleep(self, seconds=60):
        self.log_manager.log_step('睡眠{}秒'.format(seconds))
        time.sleep(seconds)
