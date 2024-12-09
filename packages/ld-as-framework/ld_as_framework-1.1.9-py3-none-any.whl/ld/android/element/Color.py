# encoding:utf-8
from ascript.android.screen import FindColors

from ...common.Logger import log_ld

from ...common.CommonClass import Rect, CommonResult

from ..action.Actions import AndroidAScriptQueryElement

class ColorQuery(AndroidAScriptQueryElement):

    def __init__(self, colors: str):
        # 必填，颜色特征点, 通常用图色助手获取
        # 非必填，圈定屏幕范围
        # 必填，找色结果间距 默认:5像素 ,如果返回的结果,多个点位的像素值 在5像素内重合.则只保留一个
        # 非必填，找色方向 1-8 个方向 ,2(默认):左上角到右下角，横向开始找色
        # 偏色rgb颜色值
        pass

    def rect(self, x, y, x1, y1):
        """
        找色范围
        :param x: 左上角x
        :param y: 左上角y
        :param x1: 右下角x
        :param y1: 右下角y
        """
        return self

    def space(self, space: int = 5):
        """
        找色结果间距,如果返回的结果,多个点位的像素值 在5像素内重合.则只保留一个
        :param space:找色结果间距 默认:5像素
        :return:
        """
        return self

    def ori(self, ori: int = 2):
        """
        找色方向2(默认):左上角到右下角，横向开始找色
        :param ori: 找色方向 1-8 个方向
        """
        return self

    def diff(self, diff: float = 0.9):
        """
        相似度, 取值范围0-1，1为100%匹配 默认:0.9
        :param diff: 相似度，取值范围0-1
        :return:
        """
        return self

