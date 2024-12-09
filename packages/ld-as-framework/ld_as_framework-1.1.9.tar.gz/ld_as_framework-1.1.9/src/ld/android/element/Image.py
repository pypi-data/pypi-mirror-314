# encoding:utf-8
from ...common.Logger import log_ld

from ..action.Actions import AndroidAScriptQueryElement

from ...common.CommonClass import CommonResult, Rect

from ascript.android.system import R

from ascript.android.screen import FindImages

class BaseImageQuery(AndroidAScriptQueryElement):

    def __init__(self):
        # 局部图片名称或路径 当只填写图片名称时,将在res/img下找到该名称的图片
        # 非必填，圈定屏幕范围
        # 图片结果的可信度0-1之间, 1为100%匹配,低于该可信度的结果将被过滤掉 默认:0.9
        pass

    def img(self, *images: str):
        return self

    def res(self, *images: str):
        return self

    def sd(self, *images: str):
        return self

    def rect(self, x, y, x1, y1):
        return self

    def confidence(self, confidence: float):
        return self

class ImageFindQuery(BaseImageQuery):

    def __init__(self):
        pass

class ImageFindTemplateQuery(BaseImageQuery):

    def __init__(self):
        # 参数为False: 使用灰度图匹配
        # 参数为True:使用原色图匹配.
        pass

    def rgb(self, rgb: bool = True):
        return self

class ImageFindSiftQuery(BaseImageQuery):

    def __init__(self):
        # 参数为False: 使用灰度图匹配
        # 参数为True:使用原色图匹配.
        pass

class ImageQuery:

    @staticmethod
    def find() -> ImageFindQuery:
        pass

    @staticmethod
    def find_template() -> ImageFindTemplateQuery:
        pass

    @staticmethod
    def find_sift() -> ImageFindSiftQuery:
        pass

