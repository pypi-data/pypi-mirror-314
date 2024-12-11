import os
import unittest
import cv2
import numpy as np
import itertools

from airtestProject.airtest.core.helper import logwrap
from airtestProject.commons.Listen.listen import tag_listener
from airtestProject.commons.utils.logger import log

size = 1600


def generate_colors(n):
    color_iter = itertools.cycle([(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)])
    return [next(color_iter) for _ in range(n)]


def draw_color_block_rect(img, rects_list, colors=None):
    """
    绘制多个色块的矩形区域
    """
    # 自动生成颜色，如果传入的颜色列表不足
    if colors is None or len(colors) < len(rects_list):
        colors = generate_colors(len(rects_list))
    canvas = np.copy(img)

    for rects, color in zip(rects_list, colors):
        # 遍历矩形区域
        for rect in rects:
            (x, y, w, h) = rect
            # 绘制矩形区域
            cv2.rectangle(canvas, pt1=(x, y), pt2=(x + w, y + h), color=color, thickness=3)

    return canvas


def color_block_finder(img, lowerb, upperb, min_w=0, max_w=None, min_h=0, max_h=None):
    '''
    色块识别 返回矩形信息
    '''
    min_w = 0
    max_w = None
    min_h = 0
    max_h = None
    # 转换色彩空间 HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 根据颜色阈值转换为二值化图像
    img_bin = cv2.inRange(img_hsv, lowerb, upperb)
    # cv2.imshow('img_bin',img_bin)

    # 寻找轮廓
    contours, hier = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    canvas = np.copy(img)
    rects = []

    if max_w is None:
        # 图像的宽度
        max_w = img.shape[1]
    if max_h is None:
        # 图像的高度
        max_h = img.shape[0]

    # 遍历所有的边缘轮廓集合
    for _, cnt in enumerate(contours):

        (x, y, w, h) = cv2.boundingRect(cnt)
        if w >= min_w and w <= max_w and h >= min_h and h <= max_h:
            rects.append((x, y, w, h))
    return rects


def color_block_finder_in_directory(directory, lowerb_list, upperb_list):
    """
    遍历目录中的所有图片文件，进行色块识别
    """

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        img_path = os.path.join(directory, filename)
        # 检查是否为文件
        if os.path.isfile(img_path):
            # 检查文件是否为图片
            if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                process_image(img_path, lowerb_list, upperb_list)


def process_image(img_path, lowerb_list, upperb_list):
    """
    处理单张图片的色块识别,用不同的颜色在同一张图上绘制所有识别结果
    """
    # 读入图片
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"图片 {img_path} 读取失败，请检查路径。")
        return

    cv2.namedWindow('result', cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    rects_list = []

    # 识别色块并获取矩形区域数组
    for lowerb, upperb in zip(lowerb_list, upperb_list):
        rects = color_block_finder(img, lowerb, upperb)
        if rects:
            for rect in rects:
                x, y, w, h = rect
                if w * h > size:
                    rects_list.append(rects)

    # 如果有识别，绘制它们
    if rects_list:
        canvas = draw_color_block_rect(img, rects_list)
        cv2.imshow('result', canvas)
        cv2.waitKey(0)  # 等待任意按键按下
        cv2.destroyAllWindows()
    else:
        print(f"在图片 {img_path} 中没有找到色块。")


def color_block_recognition(screen, lowerb_list, upperb_list):
    '''
    处理单张图片的色块识别
    '''
    rects_list = []
    # 识别色块 获取矩形区域数组
    for lowerb, upperb in zip(lowerb_list, upperb_list):
        rects = color_block_finder(screen, lowerb, upperb)
        if rects:
            for rect in rects:
                x, y, w, h = rect
                if w * h > size:
                    rects_list.append(rects)

    # 如果有，绘制它们
    if not rects_list:
        tag_listener.tag = 0
        return screen
    canvas = draw_color_block_rect(screen, rects_list)
    tag_listener.tag = -1
    return canvas


def color_block_finder_in_video(video_path, lowerb_list, upperb_list):
    """
    处理视频文件，进行色块识别，使用不同的颜色标注结果
    """
    colors = generate_colors(len(lowerb_list))

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"视频 {video_path} 打开失败，请检查路径。")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rects_list = []

        # 遍历阈值列表和颜色列表
        for lowerb, upperb, color in zip(lowerb_list, upperb_list, colors):
            rects = color_block_finder(frame, lowerb, upperb)
            if rects:
                rects_list.append((rects, color))

        # 如果有，绘制它们
        if rects_list:
            # 绘制色块的矩形区域
            for rects, color in rects_list:
                for (x, y, w, h) in rects:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    lowerb_list = [(127, 164, 208), (46, 124, 171)]
    upperb_list = [(180, 255, 255), (114, 188, 255)]
    # color_block_finder_in_directory(directory="image", lowerb_list=lowerb_list, upperb_list=upperb_list)
    color_block_finder_in_video(video_path="video/ceshi.mp4", lowerb_list=lowerb_list, upperb_list=upperb_list)
    # process_image(img_path="ziyuanqueshi.png", lowerb_list=lowerb_list, upperb_list=upperb_list)
