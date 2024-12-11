#!-*- coding = utf-8 -*-
# @Time : 2024/4/28 8:08
# @Author : 苏嘉浩
# @File : ocr_template.py
# @Software : PyCharm
import threading

import cv2
import easyocr
import numpy as np

import torch
from airtestProject.airtest import aircv
from airtestProject.airtest.core.cv import Template
from airtestProject.airtest.core.error import InvalidMatchingMethodError
from airtestProject.airtest.utils.transform import TargetPos
from airtestProject.airtest.core.helper import G, logwrap
from airtestProject.airtest.core.settings import Settings as ST  # noqa
from paddleocr import PaddleOCR
from airtestProject.commons.utils.logger import log
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

language_mapping = {
    "abq": {"PaddleOCR": "abq", "EasyOCR": "abq"},
    "ady": {"PaddleOCR": "ady", "EasyOCR": "ady"},
    "af": {"PaddleOCR": "af", "EasyOCR": "af"},
    "ar": {"PaddleOCR": "ar", "EasyOCR": "ar"},
    "ava": {"PaddleOCR": "ava", "EasyOCR": "ava"},
    "az": {"PaddleOCR": "az", "EasyOCR": "az"},
    "be": {"PaddleOCR": "be", "EasyOCR": "be"},
    "bn": {"PaddleOCR": "bn", "EasyOCR": "bn"},
    "bh": {"PaddleOCR": "bh", "EasyOCR": "bh"},
    "bho": {"PaddleOCR": "bho", "EasyOCR": "bho"},
    "bs": {"PaddleOCR": "bs", "EasyOCR": "bs"},
    "bg": {"PaddleOCR": "bg", "EasyOCR": "bg"},
    "ch": {"PaddleOCR": "ch", "EasyOCR": "ch_sim"},
    "ch_tra": {"PaddleOCR": "chinese_cht", "EasyOCR": "ch_tra"},
    "cs": {"PaddleOCR": "cs", "EasyOCR": "cs"},
    "da": {"PaddleOCR": "da", "EasyOCR": "da"},
    "dar": {"PaddleOCR": "dar", "EasyOCR": "dar"},
    "nl": {"PaddleOCR": "nl", "EasyOCR": "nl"},
    "en": {"PaddleOCR": "en", "EasyOCR": "en"},
    "et": {"PaddleOCR": "et", "EasyOCR": "et"},
    "fr": {"PaddleOCR": "fr", "EasyOCR": "fr"},
    "de": {"PaddleOCR": "german", "EasyOCR": "de"},
    "hi": {"PaddleOCR": "hi", "EasyOCR": "hi"},
    "hu": {"PaddleOCR": "hu", "EasyOCR": "hu"},
    "is": {"PaddleOCR": "is", "EasyOCR": "is"},
    "id": {"PaddleOCR": "id", "EasyOCR": "id"},
    "inh": {"PaddleOCR": "inh", "EasyOCR": "inh"},
    "ga": {"PaddleOCR": "ga", "EasyOCR": "ga"},
    "it": {"PaddleOCR": "it", "EasyOCR": "it"},
    "ja": {"PaddleOCR": "japan", "EasyOCR": "ja"},
    "kn": {"PaddleOCR": "kn", "EasyOCR": "kn"},
    "ko": {"PaddleOCR": "korean", "EasyOCR": "ko"},
    "ku": {"PaddleOCR": "ku", "EasyOCR": "ku"},
    "la": {"PaddleOCR": "la", "EasyOCR": "la"},
    "lv": {"PaddleOCR": "lv", "EasyOCR": "lv"},
    "lt": {"PaddleOCR": "lt", "EasyOCR": "lt"},
    "mai": {"PaddleOCR": "mai", "EasyOCR": "mai"},
    "ms": {"PaddleOCR": "ms", "EasyOCR": "ms"},
    "mt": {"PaddleOCR": "mt", "EasyOCR": "mt"},
    "mr": {"PaddleOCR": "mr", "EasyOCR": "mr"},
    "mn": {"PaddleOCR": "mn", "EasyOCR": "mn"},
    "ne": {"PaddleOCR": "ne", "EasyOCR": "ne"},
    "no": {"PaddleOCR": "no", "EasyOCR": "no"},
    "oc": {"PaddleOCR": "oc", "EasyOCR": "oc"},
    "pi": {"PaddleOCR": "pi", "EasyOCR": "pi"},
    "pl": {"PaddleOCR": "pl", "EasyOCR": "pl"},
    "pt": {"PaddleOCR": "pt", "EasyOCR": "pt"},
    "ro": {"PaddleOCR": "ro", "EasyOCR": "ro"},
    "ru": {"PaddleOCR": "ru", "EasyOCR": "ru"},
    "rs_cyrillic": {"PaddleOCR": "rs_cyrillic", "EasyOCR": "rs_cyrillic"},
    "rs_latin": {"PaddleOCR": "rs_latin", "EasyOCR": "rs_latin"},
    "sk": {"PaddleOCR": "sk", "EasyOCR": "sk"},
    "sl": {"PaddleOCR": "sl", "EasyOCR": "sl"},
    "es": {"PaddleOCR": "es", "EasyOCR": "es"},
    "sw": {"PaddleOCR": "sw", "EasyOCR": "sw"},
    "tl": {"PaddleOCR": "tl", "EasyOCR": "tl"},
    "te": {"PaddleOCR": "te", "EasyOCR": "te"},
    "tr": {"PaddleOCR": "tr", "EasyOCR": "tr"},
    "ug": {"PaddleOCR": "ug", "EasyOCR": "ug"},
    "uk": {"PaddleOCR": "uk", "EasyOCR": "uk"},
    "ur": {"PaddleOCR": "ur", "EasyOCR": "ur"},
    "uz": {"PaddleOCR": "uz", "EasyOCR": "uz"},
    "vi": {"PaddleOCR": "vi", "EasyOCR": "vi"}
}


class EasyOcr:
    def __init__(self, language=None):
        """
        :param language: 语言默认为中文和英文。可能会比较慢，后续可以建议为单引擎
        """
        if language is None:
            self.easy_language = ['en', 'ch_sim']
        else:
            self.easy_language = [language_mapping[lang]["EasyOCR"] for lang in language if lang in language_mapping]
        self.reader = easyocr.Reader(self.easy_language, gpu=True)

    def ocr_match(self, img, input_text, match_type=False):
        # 读取图像

        result = self.reader.readtext(img)
        # 转为 {'result': (1606, 1116), 'rectangle': [(1271, 1046), (1271, 1187), (1941, 1187), (1941, 1046)],
        # 'confidence': 0.8403522074222565, 'time': 0.7186686992645264}
        result_list = []
        if result:
            for res in result:
                result_dict = {}
                (bbox, text, prob) = res
                bbox = [(float(point[0]), float(point[1])) for point in bbox]
                (tl, tr, br, bl) = bbox
                center_x = (tl[0] + br[0]) / 2
                center_y = (tl[1] + br[1]) / 2
                result_dict['result'] = (center_x, center_y)
                result_dict['rectangle'] = bbox
                result_dict['confidence'] = prob
                result_dict['text'] = text.lower()
                result_list.append(result_dict)
        # for result_dict1 in result_list:
        #     if result_dict1['text'] == input_text:
        #         return result_dict1['result']
        # return False
        # 生成式等效于for循环
        log.info(f"匹配字符: {input_text.lower()}  本次匹配结果:  {result_list}")
        if match_type:
            coordinate = [r_dict for r_dict in result_list if input_text.lower() in r_dict.get('text').lower()]
        else:
            coordinate = [r_dict for r_dict in result_list if input_text.lower() == r_dict.get('text').lower()]
        if len(coordinate) == 1:
            return coordinate[0]
        else:
            return None
        # coordinate = next((r_dict for r_dict in result_list if r_dict.get('text').lower() == input_text.lower()),
        # None) return coordinate

    def ocr_find(self, img):
        # 读取图像

        result = self.reader.readtext(img)
        # 转为 {'result': (1606, 1116), 'rectangle': [(1271, 1046), (1271, 1187), (1941, 1187), (1941, 1046)],
        # 'confidence': 0.8403522074222565, 'time': 0.7186686992645264}
        result_list = []
        for res in result:
            result_dict = {}
            (bbox, text, prob) = res
            bbox = [(float(point[0]), float(point[1])) for point in bbox]
            (tl, tr, br, bl) = bbox
            center_x = (tl[0] + br[0]) / 2
            center_y = (tl[1] + br[1]) / 2
            result_dict['result'] = (center_x, center_y)
            result_dict['rectangle'] = bbox
            result_dict['confidence'] = prob
            result_dict['text'] = text.lower()
            result_list.append(result_dict)
        return result_list


class PpOcr:
    """
    :param language: 默认为双引擎，会比较慢，可以针对项目启用单引擎（Odin中英文都有很难受）
    """

    def __init__(self, language=None):

        if language is None:
            self.ppOcr_languages = ['ch']
        else:
            self.ppOcr_languages = [language_mapping[lang]["PaddleOCR"] for lang in language if
                                    lang in language_mapping]
        self.ocr_modules = [PaddleOCR(use_angle_cls=True, use_gpu=True, lang=lang) for lang in self.ppOcr_languages]

    def ocr_match(self, img, input_text, match_type=False):
        pp_results = {}
        for ocr_model in self.ocr_modules:
            result = ocr_model.ocr(img, cls=True)
            if result:
                for re in result:
                    if not re:
                        continue
                    for line in re:
                        text, coordinates, confidence = line[1][0], line[0], line[1][1]
                        coordinates_key = ''.join(map(str, coordinates))
                        # 如果文本在字典中且新的可信度不高于已存在的可信度，则跳过
                        if (text, coordinates_key) in pp_results and confidence <= pp_results[(text, coordinates_key)][0]:
                            continue
                        # 更新字典，包含新的或更高的可信度和坐标
                        pp_results[text, coordinates_key] = (confidence, coordinates)

        result_list = []
        for key, value in pp_results.items():
            result_dict = {}
            (prob, bbox) = value
            bbox = [(float(point[0]), float(point[1])) for point in bbox]
            (tl, tr, br, bl) = bbox
            center_x = (tl[0] + br[0]) / 2
            center_y = (tl[1] + br[1]) / 2
            result_dict['result'] = (center_x, center_y)
            result_dict['rectangle'] = bbox
            result_dict['confidence'] = prob
            result_dict['text'] = key[0].lower()
            result_list.append(result_dict)
        log.info(f"匹配字符: {input_text.lower()}  本次匹配结果:  {result_list}")
        if match_type:
            coordinate = [r_dict for r_dict in result_list if input_text.lower() in r_dict.get('text').lower()]
        else:
            coordinate = [r_dict for r_dict in result_list if input_text.lower() == r_dict.get('text').lower()]
        if len(coordinate) == 1:
            return coordinate[0]
        else:
            return None

    def ocr_find(self, img):
        pp_results = {}
        for ocr_model in self.ocr_modules:
            result = ocr_model.ocr(img, cls=True)
            for re in result:
                for line in re:
                    text, coordinates, confidence = line[1][0], line[0], line[1][1]
                    coordinates_key = ''.join(map(str, coordinates))
                    # 如果文本,还需要比对坐标是否相同不然会已经在字典中，比较可信度
                    # print((text, tuple(coordinates)) in pp_results)
                    if (text, coordinates_key) in pp_results and confidence <= pp_results[(text, coordinates_key)][0]:
                        continue
                    # 如果文本不在字典中，或者新的可信度更高，更新字典
                    pp_results[text, coordinates_key] = (confidence, coordinates)
        result_list = []
        for key, value in pp_results.items():
            result_dict = {}
            (prob, bbox) = value
            bbox = [(float(point[0]), float(point[1])) for point in bbox]
            (tl, tr, br, bl) = bbox
            center_x = (tl[0] + br[0]) / 2
            center_y = (tl[1] + br[1]) / 2
            result_dict['result'] = (center_x, center_y)
            result_dict['rectangle'] = bbox
            result_dict['confidence'] = prob
            result_dict['text'] = key[0].lower()
            result_list.append(result_dict)
        return result_list


METHOD_LIST = ['padd', 'easy']  # padd先识别一次看看速度会不会快一点


class OcrTemplate(Template):
    """
    ocr模版
        :param filename: 传入的文字
        :param ocrPlus: 是否启用二值化和高斯模糊
        :param
    """

    ocr_instances = {
        "default": {
            'easy': EasyOcr(),
            'padd': PpOcr()
        }
    }
    lock = threading.Lock()

    def __init__(self, filename=None, threshold=None, target_pos=TargetPos.MID, record_pos=None, resolution=(),
                 rgb=False,
                 scale_max=800, scale_step=0.005, ocrPlus=False, language=None, match_type=False):

        super().__init__(filename, threshold, target_pos, record_pos, resolution, rgb, scale_max, scale_step)
        self.ocrPlus = ocrPlus
        self.match_type = match_type
        if language is not None:
            self.language = tuple(language)
            with OcrTemplate.lock:
                if self.language not in OcrTemplate.ocr_instances:
                    OcrTemplate.ocr_instances[self.language] = {
                        'easy': EasyOcr(language=self.language),
                        'padd': PpOcr(language=self.language)
                    }
        else:
            self.language = language

    @property
    def filepath(self):
        return self.filename

    def match_in(self, screen):
        match_result = self._cv_match(screen)
        G.LOGGING.debug("match result: %s", match_result)
        if not match_result:
            return None
        focus_pos = TargetPos().getXY(match_result, self.target_pos)
        return focus_pos

    def match_in_nolog(self, screen):
        match_result = self._cv_match_nolog(screen)
        G.LOGGING.debug("match result: %s", match_result)
        if not match_result:
            return None
        focus_pos = TargetPos().getXY(match_result, self.target_pos)
        return focus_pos

    @logwrap
    def _cv_match(self, screen):
        return self._open_cv_match(screen)

    def _cv_match_nolog(self, screen):
        return self._open_cv_match(screen)

    def _open_cv_match(self, screen):

        img = screen

        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 增加对比度和亮度
        # contrast_img = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        # 创建一个空的数组，数据类型为float32
        img_float = np.float32(gray)
        # 缩放像素值到0-1之间
        img_norm = img_float / 255.0
        # 调整对比度
        contrast_img = np.power(img_norm, 2.3)
        # 将像素值缩放回0-255之间并转换为'uint8'
        contrast_img = np.uint8(contrast_img * 255)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(contrast_img)

        ret = None
        if self.ocrPlus is True:
            # osu
            _, binary_img = cv2.threshold(contrast_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # 应用高斯滤波
            clahe_img = cv2.GaussianBlur(binary_img, (5, 5), 0)

        for method in METHOD_LIST:
            # get function definition and execute:
            if self.language is not None:
                func = OcrTemplate.ocr_instances[self.language][method]
            else:
                func = OcrTemplate.ocr_instances["default"][method]
            if func is None:
                raise InvalidMatchingMethodError(
                    "Undefined method in OCR_METHOD: '%s'" % method)
            else:
                ret = self._try_match(func, language=self.language, img=clahe_img, input_text=self.filename,
                                      match_type=self.match_type)
            # 先用easyOCR方法失败则会用下一个
            if ret:
                break
        return ret

    @staticmethod
    def _try_match(func, *args, **kwargs):
        G.LOGGING.debug("try match with %s" % func)
        try:
            instance = func
            ret = instance.ocr_match(img=kwargs['img'], input_text=kwargs['input_text'],
                                     match_type=kwargs['match_type'])
        except aircv.NoModuleError as err:
            G.LOGGING.warning(
                "'Easy/ppd' initialization failed. Alternatively, reinstall easycr or PaddleOCR.")
            return None
        except aircv.BaseError as err:
            G.LOGGING.debug(repr(err))
            return None
        else:
            return ret

    @logwrap
    def find_text(self, screen):

        # 灰度化
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # 增加对比度和亮度
        # contrast_img = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        # 创建一个空的数组，数据类型为float32
        img_float = np.float32(gray)
        # 缩放像素值到0-1之间
        img_norm = img_float / 255.0
        # 调整对比度
        contrast_img = np.power(img_norm, 2.3)
        # 将像素值缩放回0-255之间并转换为'uint8'
        contrast_img = np.uint8(contrast_img * 255)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(contrast_img)

        ret = None
        if self.ocrPlus is True:
            # osu
            _, binary_img = cv2.threshold(contrast_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # 应用高斯滤波
            clahe_img = cv2.GaussianBlur(binary_img, (5, 5), 0)
        if self.language is not None:
            func = OcrTemplate.ocr_instances[self.language]["padd"]
        else:
            func = OcrTemplate.ocr_instances["default"]["padd"]
        if func is None:
            raise InvalidMatchingMethodError(
                "Undefined method in OCR_METHOD: '%s'" % "padd")
        ret = func.ocr_find(clahe_img)
        if ret:
            return ret
        return None

    @logwrap
    def find_region_text(self, screen, region=None):

        if region is not None:
            screen = screen[region[1]:region[1] + region[3], region[0]:region[0] + region[2]]
        # 灰度化
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # 增加对比度和亮度
        # contrast_img = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        # 创建一个空的数组，数据类型为float32
        img_float = np.float32(gray)
        # 缩放像素值到0-1之间
        img_norm = img_float / 255.0
        # 调整对比度
        contrast_img = np.power(img_norm, 2.3)
        # 将像素值缩放回0-255之间并转换为'uint8'
        contrast_img = np.uint8(contrast_img * 255)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(contrast_img)

        ret = None
        if self.ocrPlus is True:
            # osu
            _, binary_img = cv2.threshold(contrast_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # 应用高斯滤波
            clahe_img = cv2.GaussianBlur(binary_img, (5, 5), 0)
        if self.language is not None:
            func = OcrTemplate.ocr_instances[self.language]["padd"]
        else:
            func = OcrTemplate.ocr_instances["default"]["padd"]
        if func is None:
            raise InvalidMatchingMethodError(
                "Undefined method in OCR_METHOD: '%s'" % "padd")
        ret = func.ocr_find(clahe_img)
        if ret:
            return ret
        return None
