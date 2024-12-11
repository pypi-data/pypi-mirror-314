import cv2
import os

from PIL import Image, ImageDraw
from airtestProject.commons.utils.my_template import myTemplate

"""
author liuhuatong
des UI遮挡检测
date 2024/4/29
"""

## 横版,左上角和右下角像素位置
_H_CONFIG = {
    "MI": {
        "MI-8": {"l_notch": (0, 201, 150, 879), "pixel": (1080, 2248)},
    }
}
H_CONFIG = {}
for key, values in _H_CONFIG.items():
    H_CONFIG.update(values)

class ScreenDetect:
    """

    """
    def __init__(self, device_mode, img_path, ui_path):
        self.device_mode =device_mode.replace(" ", "-")
        self.img_path = img_path
        self.ui_path = ui_path
        self.result = {}
        self.pixel = H_CONFIG[self.device_mode]["pixel"]

    def _get_image_paths(self, directory, extensions=('.jpg', '.jpeg', '.png')):
        """
        获取指定目录下所有图片的路径。

        :param directory: 要搜索的目录路径
        :param extensions: 图片文件的扩展名列表
        :return: 图片文件路径列表
        """
        image_paths = []  # 存储图片路径的列表
        # 遍历目录
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 检查文件扩展名是否在指定列表中
                if file.lower().endswith(extensions):
                    # 拼接完整的文件路径
                    full_path = os.path.join(root, file)
                    image_paths.append(full_path)

        return image_paths

    def _get_h_rec_by_height(self, height):
        """
        通过刘海屏高度，返回横屏可能遮挡区域
        """

        return [(0, 0,),(0,self.pixel[0]), (height,self.pixel[0]), (height,0)],[(self.pixel[1] - height, 0),(self.pixel[1] - height,self.pixel[0]), (self.pixel[1], self.pixel[0]),(self.pixel[1],0)]
    def _do_rectangles_overlap(self, rec1, rec2):
        """
        给出两个矩形的左上角和右下角顶点位置，判断两个矩形是否有重叠
        """
        # 给出两个矩形的左上角和右下角顶点位置，判断两个矩形是否有重叠
        print(rec1,rec2)
        return not (rec1[0] >= rec2[2] or rec1[2] <= rec2[0] or rec1[1] >= rec2[3] or rec1[3] <= rec2[1])


    def _match_ui(self,img,ui):
        """
        匹配ui坐标，返回位置信息
        """
        im_read = cv2.imread(img)
        rec = myTemplate(ui)._cv_match(im_read)
        return rec


    def h_detect_by_cv(self):
        """
        通过cv方式，检测ui遮挡
        """
        if self.device_mode not in H_CONFIG:
            self.result = {"success": False,
                           "message": "没有{}设备的刘海屏信息,请联系管理员补充!!!".format(self.device_mode)}
            return self.result

        # 刘海屏遮挡区域
        l_notch = H_CONFIG[self.device_mode]["l_notch"]
        r_notch = [self.pixel[1] - l_notch[2], self.pixel[0] - l_notch[3], self.pixel[1] - l_notch[0], self.pixel[0] - l_notch[1]]

        # 刘海屏警告区域
        l_notch_warn, r_notch_warn = self._get_h_rec_by_height(H_CONFIG[self.device_mode]["l_notch"][2])

        l_notch_warn_rec = [l_notch_warn[0][0], l_notch_warn[0][1], l_notch_warn[2][0], l_notch_warn[2][1]]
        r_notch_warn_rec = [r_notch_warn[0][0], r_notch_warn[0][1], r_notch_warn[2][0], r_notch_warn[2][1]]
        images_path = self._get_image_paths(self.img_path)
        ui_path = [self.ui_path] if os.path.isfile(self.ui_path) else self._get_image_paths(self.ui_path)


        self.result = {"sucess": True, "overlap": set(), "may_overlap": set(),"device_mode": self.device_mode}
        for img_path in images_path:
            # 打开截图文件
            img = Image.open(img_path)
            # 创建一个 ImageDraw 对象
            draw = ImageDraw.Draw(img)
            # 当刘海屏在左边的时候，画遮挡区域
            draw.rectangle(l_notch, fill='black', outline=None)
            # 当刘海屏在右边的时候，画遮挡区域
            draw.rectangle(r_notch, fill='black', outline=None)

            # 画刘海屏警告区域
            draw.line(l_notch_warn + [l_notch_warn[0]], fill='red', width=2)
            draw.line(r_notch_warn + [r_notch_warn[0]], fill='red', width=2)

            # 保存地址
            name = img_path.split("\\")[-1]
            front_dir = os.path.join(os.path.abspath(os.path.join((self.img_path), "..")), "notch", self.device_mode)
            if not os.path.exists(front_dir):
                os.makedirs(front_dir)
            save_path = os.path.join(front_dir, name.split(".")[0] + "_{}_notch".format(self.device_mode) + "." +
                                     name.split(".")[1])
            # 画匹配到的ui

            for ui in ui_path:
                # ui匹配
                rec = self._match_ui(img_path, ui)
                if rec:
                    rectangle = rec['rectangle']

                    # 画出匹配到的Ui
                    draw.line(rectangle + [rectangle[0]], fill='green', width=2)

                    # 判断是否存在遮挡
                    ui_rec = [rectangle[0][0], rectangle[0][1], rectangle[2][0], rectangle[2][1]]
                    if self._do_rectangles_overlap(ui_rec, l_notch) or self._do_rectangles_overlap(ui_rec, r_notch):
                        self.result["overlap"].add(save_path)

                    # 可能遮挡
                    if self._do_rectangles_overlap(ui_rec, l_notch_warn_rec) or self._do_rectangles_overlap(ui_rec, r_notch_warn_rec):
                        self.result["may_overlap"].add(save_path)
            # 保存修改后的图像

            img.save(save_path)
        self.result["may_overlap"] = self.result["may_overlap"] - self.result["overlap"]
        return self.result





if __name__ == '__main__':
    s = ScreenDetect("MI 8",r".\images", r".\ui")
    res = s.h_detect_by_cv()
    print(res)
    # result = s.detect_by_cv(ui_path=r".\ui", images_path=r".\images")