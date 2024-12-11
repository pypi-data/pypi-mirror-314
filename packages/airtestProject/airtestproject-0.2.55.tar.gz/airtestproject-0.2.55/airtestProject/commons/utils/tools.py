#!-*- coding = utf-8 -*-
# @Time : 2024/4/7 2:44
# @Author : 苏嘉浩
# @File : operate_base.py
# @Software : PyCharm
import copy
import functools
import json
import math
import os
import traceback
from pathlib import Path
import time
import numpy as np
import six

from airtestProject.airtest.core.android.touch_methods.base_touch import DownEvent, MoveEvent, UpEvent, SleepEvent
from airtestProject.airtest.core.helper import G
from airtestProject.airtest.core.settings import Settings as ST
from airtestProject.airtest.utils.snippet import get_absolute_coordinate


def log_error(arg, timestamp=None, desc="", snapshot=False, start_time=None, end_time=None):
    """
    Examples:
        >>> log_error("hello world", snapshot=True)
        >>> log_error({"key": "value"}, timestamp=time.time(), desc="log dict")

    """
    from airtestProject.airtest.core.cv import try_log_screen
    if G.LOGGER:
        depth = 0
        if snapshot:
            # 如果指定了snapshot参数，强制保存一张图片
            save_image = ST.SAVE_IMAGE
            ST.SAVE_IMAGE = True
            try:
                try_log_screen(depth=2)
            except AttributeError:
                # if G.DEVICE is None
                pass
            else:
                depth = 1
            finally:
                ST.SAVE_IMAGE = save_image
            G.LOGGER.log("info", {
                "name": desc or arg.__class__.__name__,
                'start_time': start_time, "traceback": arg, "end_time": end_time
            }, depth=depth, timestamp=timestamp, user_set=True)


def log_normal(arg, timestamp=None, desc="", snapshot=False, start_time=None, end_time=None):
    from airtestProject.airtest.core.cv import try_log_screen
    if G.LOGGER:
        depth = 0
        if snapshot:
            # 如果指定了snapshot参数，强制保存一张图片
            save_image = ST.SAVE_IMAGE
            ST.SAVE_IMAGE = True
            try:
                try_log_screen(depth=2)
            except AttributeError:
                # if G.DEVICE is None
                pass
            else:
                depth = 1
            finally:
                ST.SAVE_IMAGE = save_image
        if isinstance(arg, six.string_types):
            # 普通文本log内容放在"log"里，如果有trace内容放在"traceback"里
            # 在报告中，假如"traceback"有内容，将会被识别为报错，这个步骤会被判定为不通过
            G.LOGGER.log("info", {"name": desc or arg, 'start_time': start_time,
                                  "end_time": end_time, "traceback": None, "log": arg}, depth=depth,
                         timestamp=timestamp, user_set=True)
            G.LOGGING.info(arg)
        else:
            G.LOGGER.log("info", {"name": desc or repr(arg), 'start_time': start_time,
                                  "end_time": end_time, "traceback": None, "log": repr(arg)}, depth=depth,
                         timestamp=timestamp, user_set=True)


def get_folder_path_up(current_path, folder_name):
    """
    向上寻找文件夹路径，找到后返回对应路径。
    :param current_path: 当前文件路径
    :param folder_name: 需要寻找的文件夹名字
    :return: 返回找到的文件夹
    """
    result_path = os.path.dirname(os.path.abspath(current_path))
    while True:
        if os.path.exists(os.path.join(result_path, folder_name)):
            # 当前文件路径下有对应文件夹路径
            result_path = os.path.join(result_path, folder_name)
            break
        elif result_path == os.path.dirname(result_path):
            # 去到根目录还未找到文件夹路径
            folder_Parent = find_case_parent_directory(os.path.abspath(current_path), "case")
            reports_patch = os.path.join(folder_Parent, folder_name)
            os.makedirs(reports_patch, exist_ok=True)
            result_path = os.path.abspath(reports_patch)
        else:
            # 向上查找文件夹路径
            result_path = os.path.dirname(result_path)
    return result_path


def get_folder_path_down(current_path, folder_name):
    # 检查当前路径下是否有 'images' 文件夹
    if folder_name in os.listdir(current_path):
        return os.path.join(current_path, folder_name)

    # 在每个子目录中递归查找
    for subdir in os.listdir(current_path):
        full_subdir = os.path.join(current_path, subdir)
        if os.path.isdir(full_subdir):
            result = get_folder_path_down(current_path, folder_name)
            if result is not None:
                return result

    # 如果在当前路径及其所有子目录中都没有找到 'images' 文件夹，返回 None
    return None


def get_screenshot_cv():
    from airtestProject.airtest.core.helper import G
    return G.DEVICE.snapshot(quality=ST.SNAPSHOT_QUALITY)


def coordinate_transformation(player_start_point, player_forward_move,
                              player_left_move, player_move_target, swipe_time, circle_center, radius):
    """

    :param player_start_point: 玩家初始坐标
    :param player_forward_move: 玩家向前移动后的坐标
    :param player_left_move: 玩家向左移动后的坐标
    :param player_move_target: 玩家需要移动的目标点
    :param swipe_time: 单次滑动时长
    :param circle_center: 圆心
    :param radius: 遥感半径
    :return:
    """

    def angle_between_vectors(vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        length1 = np.sqrt(np.dot(vector1, vector1))
        length2 = np.sqrt(np.dot(vector2, vector2))
        # 计算夹角的cos值
        cos_angle = dot_product / (length1 * length2)
        # 求得夹角（弧度制）
        angle_radians = np.arccos(np.clip(cos_angle, -1.0, 1.0))  # 使用 np.clip 防止浮点数误差

        return angle_radians * 180 / np.pi

    #  计算该夹角在圆上的点
    def circular_coordinates(angle_degrees):
        # 定义半径和角度
        radius = 1
        # 将角度从度数转换为弧度
        angle_radians = math.radians(angle_degrees)

        # 计算x和y坐标
        x = round(radius * math.cos(angle_radians), 5)
        y = round(radius * math.sin(angle_radians), 5)
        return [x, y]

    def angle_move(start_point, move_point_90, move_point_180, move_target, angle_move_time):
        origin = np.array(start_point)
        # 90 度方向的点
        point_90 = np.array(move_point_90)
        # 180 度方向的点
        point_180 = np.array(move_point_180)
        # 目标点
        target = np.array(move_target)

        # 计算向量
        vector_90 = origin - point_90
        vector_180 = origin - point_180
        vector_target = origin - target

        # 计算移动时间
        move_first_length = np.linalg.norm(point_90 - origin)
        move_target_length = np.linalg.norm(target - origin)
        player_speed = move_first_length / (angle_move_time + 0.55)
        time_to_target = move_target_length / player_speed

        angle_90_target_degrees = angle_between_vectors(vector_90, vector_target)
        angle_180_target_degrees = angle_between_vectors(vector_180, vector_target)
        print(angle_90_target_degrees)
        print(angle_180_target_degrees, "看看是否可以根据这个来计算")

        # 计算在遥感圆内要移动的角度
        if angle_180_target_degrees > 90:
            if angle_90_target_degrees > 90:
                angle_to_move = 270 + (90 - (angle_90_target_degrees - 90))
            else:
                angle_to_move = 90 - angle_90_target_degrees
        else:
            angle_to_move = angle_90_target_degrees + 90

        print("在遥感圆内要移动的角度为：", angle_to_move, "度")
        return circular_coordinates(angle_to_move), time_to_target

    final_move_point, move_time = angle_move(player_start_point, player_forward_move, player_left_move,
                                             player_move_target, swipe_time)
    print(f"遥感移动坐标，单位圆坐标{final_move_point[0], final_move_point[1]}")

    def map_point(x1, y1):
        # 将第一个圆的坐标系中的点映射到第二个圆的坐标系中
        # 取反y坐标
        y1 = -y1
        # 缩放坐标
        x1 *= radius
        y1 *= radius
        # 平移坐标
        x2 = x1 + 0.15
        y2 = y1 + 0.75
        return x2, y2

    x, y = map_point(final_move_point[0], final_move_point[1])
    return x, y, move_time


def coordinate_transformation_right(player_start_point, player_forward_move,
                                    player_right_move, player_move_target, swipe_time, circle_center, radius):
    """

    :param player_start_point: 玩家初始坐标
    :param player_forward_move: 玩家向前移动后的坐标
    :param player_right_move: 玩家向右移动后的坐标
    :param player_move_target: 玩家需要移动的目标点
    :param swipe_time: 单次滑动时长
    :param circle_center: 圆心
    :param radius: 遥感半径
    :return:
    """

    def angle_between_vectors(vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        length1 = np.sqrt(np.dot(vector1, vector1))
        length2 = np.sqrt(np.dot(vector2, vector2))
        # 计算夹角的cos值
        cos_angle = dot_product / (length1 * length2)
        # 求得夹角（弧度制）
        angle_radians = np.arccos(np.clip(cos_angle, -1.0, 1.0))  # 使用 np.clip 防止浮点数误差

        return angle_radians * 180 / np.pi

    #  计算该夹角在圆上的点
    def circular_coordinates(angle_degrees):
        # 定义半径和角度
        radius = 1
        # 将角度从度数转换为弧度
        angle_radians = math.radians(angle_degrees)

        # 计算x和y坐标
        x = round(radius * math.cos(angle_radians), 5)
        y = round(radius * math.sin(angle_radians), 5)
        return [x, y]

    def angle_move(start_point, move_point_90, move_point_0, move_target, angle_move_time):
        origin = np.array(start_point)
        # 90 度方向的点
        point_90 = np.array(move_point_90)
        # 0 度方向的点
        point_0 = np.array(move_point_0)
        # 目标点
        target = np.array(move_target)

        # 计算向量
        vector_90 = origin - point_90
        vector_0 = origin - point_0
        vector_target = origin - target

        # 计算移动时间
        move_first_length = np.linalg.norm(point_90 - origin)
        move_target_length = np.linalg.norm(target - origin)
        player_speed = move_first_length / (angle_move_time + 0.55)
        time_to_target = move_target_length / player_speed

        angle_90_target_degrees = angle_between_vectors(vector_90, vector_target)
        angle_0_target_degrees = angle_between_vectors(vector_0, vector_target)
        print(angle_90_target_degrees)
        print(angle_0_target_degrees, "看看是否可以根据这个来计算")

        # 计算在遥感圆内要移动的角度
        if angle_0_target_degrees < 90:
            if angle_90_target_degrees > 90:
                angle_to_move = 270 + (90 - (angle_90_target_degrees - 90))
            else:
                angle_to_move = 90 - angle_90_target_degrees
        else:
            angle_to_move = angle_90_target_degrees + 90

        print("在遥感圆内要移动的角度为：", angle_to_move, "度")
        return circular_coordinates(angle_to_move), time_to_target

    final_move_point, move_time = angle_move(player_start_point, player_forward_move, player_right_move,
                                             player_move_target, swipe_time)
    print(f"遥感移动坐标，单位圆坐标{final_move_point[0], final_move_point[1]}")

    def map_point(x1, y1):
        # 将第一个圆的坐标系中的点映射到第二个圆的坐标系中
        # 取反y坐标
        y1 = -y1
        # 缩放坐标
        x1 *= radius
        y1 *= radius
        # 平移坐标
        x2 = x1 + circle_center[0]
        y2 = y1 + circle_center[1]
        return x2, y2

    x, y = map_point(final_move_point[0], final_move_point[1])
    return x, y, move_time


def find_case_parent_directory(file_path, current):
    current_path = Path(file_path).resolve()
    for parent in current_path.parents:
        if (parent / current).exists():
            return parent
    return current_path.parent


# 局部截图
def get_snapshot_range(start_point, end_point):
    screen = G.DEVICE.snapshot()
    image_np = np.array(screen)
    snapshot_list = [(slice(start_point[0], end_point[0]), slice(start_point[1], end_point[1]))]
    image = image_np[snapshot_list[0]]
    return image


# 定时器
def run_with_timer(start_func, interval, max_executions, stop_func):
    """
    以固定间隔执行函数A，执行次数上限为m。

    :param start_func: 要执行的函数
    :param interval: 执行间隔（秒）
    :param max_executions: 最大执行次数
    :param stop_func: 一个函数，当该函数返回不为False时，停止定时器
    """
    executions = 0

    while executions < max_executions and not stop_func():
        start_func()
        executions += 1
        time.sleep(interval)


def run_json_script(json_script_file: str):
    """

    :param json_script_file: 运行json脚本文件路径
    :return:
    """
    try:
        with open(json_script_file, 'r') as file:
            script_data = json.load(file)
    except:
        script_data = None
    # print(data2) script_dict = {'o0': [{'DOWN': (0.6064814814814815, 0.535958904109589)}, {'SLEEP':
    # 0.05511283874511719, 'MOVE': (0.6064814814814815, 0.5333904109589042)}, {'SLEEP': 0.007013559341430664,
    # 'MOVE': (0.6064814814814815, 0.5321061643835616)}, {'SLEEP': 0.007963895797729492, 'MOVE': (0.6064814814814815,
    # 0.528681506849315)}, {'SLEEP': 0.008005380630493164, 'MOVE': (0.6064814814814815, 0.5222602739726028)},
    # {'SLEEP': 0.008044004440307617, 'MOVE': (0.6064814814814815, 0.5136986301369864)}, {'SLEEP':
    # 0.007988452911376953, 'MOVE': (0.6064814814814815, 0.504708904109589)}, {'SLEEP': 0.008099555969238281,
    # 'MOVE': (0.6064814814814815, 0.4974315068493151)}, {'SLEEP': 0.008005857467651367, 'MOVE': (0.6092592592592593,
    # 0.4884417808219178)}, {'SLEEP': 0.007979154586791992, 'MOVE': (0.612037037037037, 0.4798801369863014)},
    # {'SLEEP': 0.008135795593261719, 'MOVE': (0.6148148148148148, 0.4708904109589041)}, {'SLEEP':
    # 0.007969379425048828, 'MOVE': (0.6175925925925926, 0.4661815068493151)}, {'SLEEP': 0.007978677749633789,
    # 'MOVE': (0.6175925925925926, 0.4597602739726027)}, {'SLEEP': 0.007978677749633789, 'MOVE': (0.6203703703703703,
    # 0.4533390410958904)}, {'SLEEP': 0.007979154586791992, 'MOVE': (0.6231481481481481, 0.4460616438356164)},
    # {'SLEEP': 0.008125543594360352, 'MOVE': (0.6231481481481481, 0.4396404109589041)}, {'SLEEP':
    # 0.007992982864379883, 'MOVE': (0.6259259259259259, 0.4323630136986301)}, {'SLEEP': 0.007981538772583008,
    # 'MOVE': (0.6287037037037037, 0.4233732876712329)}, {'SLEEP': 0.007978677749633789, 'MOVE': (0.6305555555555555,
    # 0.4148116438356164)}, {'SLEEP': 0.009973287582397461, 'MOVE': (0.6333333333333333, 0.4096746575342466)},
    # {'SLEEP': 0.005984306335449219, 'MOVE': (0.6333333333333333, 0.4049657534246575)}, {'SLEEP':
    # 0.007977724075317383, 'MOVE': (0.6361111111111111, 0.3998287671232877)}, {'SLEEP': 0.007978439331054688,
    # 'MOVE': (0.6388888888888888, 0.3934075342465753)}, {'SLEEP': 0.008101224899291992, 'MOVE': (0.6388888888888888,
    # 0.3886986301369863)}, {'SLEEP': 0.008000850677490234, 'MOVE': (0.6388888888888888, 0.3848458904109589)},
    # {'SLEEP': 0.007978677749633789, 'MOVE': (0.6416666666666667, 0.3809931506849315)}, {'SLEEP':
    # 0.007978439331054688, 'MOVE': (0.6416666666666667, 0.3758561643835616)}, {'SLEEP': 0.010006189346313477,
    # 'MOVE': (0.6416666666666667, 0.3711472602739726)}, {'SLEEP': 0.005988121032714844, 'MOVE': (0.6444444444444445,
    # 0.3672945205479452)}, {'SLEEP': 0.00997304916381836, 'MOVE': (0.6472222222222223, 0.3634417808219178)},
    # {'SLEEP': 0.0, 'UP': (0.6472222222222223, 0.3634417808219178)}], 'o1': [{'SLEEP': 4.719709396362305,
    # 'DOWN': (0.19444444444444445, 0.5059931506849316)}, {'SLEEP': 0.06353163719177246, 'UP': (0.19444444444444445,
    # 0.5059931506849316)}]} print(data2 == script_dict)
    ret_all = []
    if script_data is not None:
        for key, value_list in script_data.items():
            ret = []
            for value_dict in value_list:
                for action, value in value_dict.items():
                    pos_value = copy.deepcopy(value)
                    if action == 'DOWN':
                        pos_value = get_absolute_coordinate(pos_value, G.DEVICE)
                        ret.append(DownEvent(G.DEVICE.touch_proxy.ori_transformer(pos_value), pressure=50))
                    if action == "MOVE":
                        pos_value = get_absolute_coordinate(pos_value, G.DEVICE)
                        ret.append(MoveEvent(G.DEVICE.touch_proxy.ori_transformer(pos_value), pressure=50))
                    if action == 'UP':
                        ret.append(UpEvent())
                    if action == "SLEEP":
                        ret.append(SleepEvent(pos_value))
            ret_all.append(ret)

        for ret in ret_all:
            G.DEVICE.touch_proxy.perform(ret)
