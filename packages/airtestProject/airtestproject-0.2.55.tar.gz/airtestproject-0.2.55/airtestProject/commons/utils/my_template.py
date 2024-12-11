from airtestProject.airtest.core.cv import Template
from airtestProject.airtest.core.helper import logwrap, G

from airtestProject.airtest.core.settings import Settings as ST  # noqa
import cv2
from airtestProject.airtest.core.error import InvalidMatchingMethodError
from airtestProject.airtest.utils.transform import TargetPos
from distutils.version import LooseVersion

from airtestProject.airtest.aircv.template_matching import TemplateMatching
from airtestProject.airtest.aircv.multiscale_template_matching import MultiScaleTemplateMatching, \
    MultiScaleTemplateMatchingPre
from airtestProject.airtest.aircv.keypoint_matching import KAZEMatching, BRISKMatching, AKAZEMatching, ORBMatching
from airtestProject.airtest.aircv.keypoint_matching_contrib import SIFTMatching, SURFMatching, BRIEFMatching

MATCHING_METHODS = {
    "sift": SIFTMatching,
    "surf": SURFMatching,
    "brisk": BRISKMatching,
    "akaze": AKAZEMatching,
    "kaze": KAZEMatching,
    "tpl": TemplateMatching,
    "mstpl": MultiScaleTemplateMatchingPre,
    "gmstpl": MultiScaleTemplateMatching,
    "orb": ORBMatching,
    "brief": BRIEFMatching,
}


class MyTemplate(Template):
    CVSTRATEGY = ["surf", "sift", "gmstpl"]
    if LooseVersion('3.4.2') < LooseVersion(cv2.__version__) < LooseVersion('4.4.0'):
        CVSTRATEGY = ["mstpl", "tpl", "brisk"]

    def __init__(self, filename, threshold=None, target_pos=TargetPos.MID, record_pos=None, resolution=(), rgb=False,
                 scale_max=800, scale_step=0.005, translucent=False):
        super().__init__(filename, threshold, target_pos, record_pos, resolution, rgb, scale_max, scale_step)
        self.translucent = translucent

    def match_in_nolog(self, screen):
        match_result = self._cv_match_nolog(screen)
        G.LOGGING.debug("match result: %s", match_result)
        if not match_result:
            return None
        focus_pos = TargetPos().getXY(match_result, self.target_pos)
        return focus_pos

    @logwrap
    def _cv_match(self, screen):
        # in case image file not exist in current directory:
        ori_image = self._imread()
        image = self._resize_image(ori_image, screen, ST.RESIZE_METHOD)
        ret = None
        for method in MyTemplate.CVSTRATEGY:
            # get function definition and execute:
            func = MATCHING_METHODS.get(method, None)
            if func is None:
                raise InvalidMatchingMethodError("Undefined method in CVSTRATEGY: '%s', try "
                                                 "'kaze'/'brisk'/'akaze'/'orb'/'surf'/'sift'/'brief' instead." % method)
            else:
                if method in ["mstpl", "gmstpl"]:
                    ret = self._try_match(func, ori_image, screen, threshold=self.threshold, rgb=self.rgb,
                                          record_pos=self.record_pos,
                                          resolution=self.resolution, scale_max=self.scale_max,
                                          scale_step=self.scale_step)
                else:
                    ret = self._try_match(func, image, screen, threshold=self.threshold, rgb=self.rgb)
            if ret:
                break
        return ret

    def _cv_match_nolog(self, screen):
        # in case image file not exist in current directory:
        ori_image = self._imread()
        image = self._resize_image(ori_image, screen, ST.RESIZE_METHOD)
        ret = None
        for method in MyTemplate.CVSTRATEGY:
            # get function definition and execute:
            func = MATCHING_METHODS.get(method, None)
            if func is None:
                raise InvalidMatchingMethodError("Undefined method in CVSTRATEGY: '%s', try "
                                                 "'kaze'/'brisk'/'akaze'/'orb'/'surf'/'sift'/'brief' instead." % method)
            else:
                if method in ["mstpl", "gmstpl"]:
                    ret = self._try_match(func, ori_image, screen, threshold=self.threshold, rgb=self.rgb,
                                          record_pos=self.record_pos,
                                          resolution=self.resolution, scale_max=self.scale_max,
                                          scale_step=self.scale_step)
                else:
                    ret = self._try_match(func, image, screen, threshold=self.threshold, rgb=self.rgb)
            if ret:
                break
        return ret
