from airtestProject.abstractBase.operate_base import OperateABC
from airtestProject.commons.utils.logger import log
from airtestProject.airtest.core import api as air
from airtestProject.commons.utils.ocr_template import OcrTemplate

class OcrOperate(OperateABC):
    def __init__(self, language):
        super().__init__()
        self.language = language

    def set_language(self, language):
        self.language = language

    def snapshot(self):
        pass

    def return_ocr(self, val, ocrPlus=False, ocr_match_type=False):
        return OcrTemplate(val, language=self.language, ocrPlus=ocrPlus, match_type=ocr_match_type)

    def click(self, pos, times=1, ocrPlus=False, ocr_match_type=False, **kwargs):
        try:
            log.info(f"perform the touch action on the device screen, pos: {pos}")
            kwargs.pop('focus', None)
            kwargs.pop('sleep_interval', None)
            value = self.return_ocr(pos, ocr_match_type)
            return air.touch(value, times, **kwargs)
        except Exception as e:
            log.error(f"failed to perform the touch action on the device screen, pos: {pos}")
            raise e

    def swipe(self, value, v2=None, vector_direction=None, ocrPlus=False, rgb=False, translucent=False, **kwargs):
        kwargs.pop('duration', None)
        kwargs.pop('focus', None)
        if vector_direction is None:
            vector_direction = [0, -3.0]
        log.info("Perform the swipe action on the device screen.")
        value = self.return_ocr(value, ocrPlus=ocrPlus)
        if v2 is not None:
            v2 = self.return_ocr(v2, ocrPlus=ocrPlus)
        return air.swipe(value, v2, vector=vector_direction, **kwargs)

