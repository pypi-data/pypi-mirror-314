# encoding:utf-8
from ascript.android.screen import Ocr

from ...common.Logger import log_ld

from ..action.Actions import AndroidAScriptQueryElement

from ...common.CommonClass import CommonResult, Rect

class PaddleocrV2(AndroidAScriptQueryElement):

    def __init__(self, rect=None, pattern=None, confidence=0.6, max_side_len=1200, precision=16, bitmap=None,
                 file=None):
        # 圈定屏幕中识别的范围
        # 匹配的正则表达式 如保留字符串中包含IT的识别结果:.*IT.*
        # 识别可信度:默认0.6
        # 如果指定最大边时,如1200,那么所有输入资源都会同比缩放最大边至1200px,再传入引擎识别
        # 从指定的图片中识别 该Bitmap 可以从Screen.capture()获取
        # 从指定的文件中识别
        pass

    def rect(self, x, y, x1, y1):
        return self

    def text(self, text: str):
        return self

    def pattern(self, pattern: str):
        return self

    def confidence(self, confidence: float):
        return self

    def max_side_len(self, max_side_len: int):
        return self

    def precision(self, precision: int):
        return self

    def bitmap(self, bitmap: str):
        return self

    def file(self, file: str):
        return self

class PaddleocrV3(PaddleocrV2):

class Tesseract(AndroidAScriptQueryElement):

    def __init__(self, rect=None, pattern=None, data_file=Ocr.Tess_CHI, split_level=Ocr.RIL_AUTO, white_list=None,
                 black_list=None):
        # 圈定屏幕中识别的范围
        # 匹配的正则表达式 如保留字符串中包含IT的识别结果:.*IT.*
        # 字库,可传入字库文件路径,或
        # Ocr.Tess_CHI:已训练的中文字库
        # Ocr.Tess_EN:英文字库
        # 识别结果的,分割等级:
        # RIL_AUTO:自动分割(默认)
        # RIL_BLOCK:块分割
        # RIL_PARA:页分割
        # RIL_TEXTLINE:行分割
        # RIL_WORD:单词分割
        # RIL_SYMBOL:符号分割
        # 识别白名单
        # 识别黑名单
        pass

    def data_file(self, data_file: str = Ocr.Tess_CHI):
        return self

    def rect(self, x, y, x1, y1):
        return self

    def text(self, text: str):
        return self

    def pattern(self, pattern: str):
        return self

    def split_level(self, split_level: int = Ocr.RIL_AUTO):
        return self

    def white_list(self, white_list: str = None):
        return self

    def black_list(self, black_list: str = None):
        return self

class MlkitOcrV2(AndroidAScriptQueryElement):

    def __init__(self, rect=None, pattern=None, bitmap=None):
        # 圈定屏幕中识别的范围
        # 匹配的正则表达式 如保留字符串中包含IT的识别结果:.*IT.*
        # 要识别的图片,默认为当前屏幕,如需传入指定图片,请传入Bitmap格式
        pass

    def rect(self, x, y, x1, y1):
        return self

    def text(self, text: str):
        return self

    def pattern(self, pattern: str):
        return self

    def bitmap(self, bitmap: str):
        return self

class OcrQuery:

    @staticmethod
    def paddleocr_v2() -> PaddleocrV2:
        pass

    @staticmethod
    def paddleocr_v3() -> PaddleocrV3:
        pass

    @staticmethod
    def tesseract() -> Tesseract:
        pass

    @staticmethod
    def mlkitocr_v2() -> MlkitOcrV2:
        pass

