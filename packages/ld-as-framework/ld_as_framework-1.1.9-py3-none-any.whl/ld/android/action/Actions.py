# encoding:utf-8
from typing import TypeVar, Union

from ..environment.Device import Device

from ...common.CommonClass import AScriptQueryElement, CommonResult

from ..element.Node import NodeQuery

from ...common.Logger import log_ld

from ...common.CommonClass import CommonAction, Method

import re

class Point:
    def __init__(self, x: Union[str, int], y: Union[str, int]):
        self.x = x
        self.y = y
        pass

        screen_info = Device.get_device_display()

        if type(x) is str:
            self.x = screen_info.width * tmp_percentage

        if type(y) is str:
            self.y = screen_info.height * tmp_percentage

    @staticmethod
    def get_point(self):
        pass


class AndroidAScriptQueryElement(AScriptQueryElement):
    """
    AS元素查询父类，所有的元素查询都需要继承该类
    """

    def __init__(self):
        pass

    def rect_left_top(self):
        """
        获取左上角范围
        :return:
        """
        return self

    def rect_right_top(self):
        """
        获取右上角范围
        :return:
        """
        return self

    def rect_left_bottom(self):
        """
        获取左下角范围
        :return:
        """
        return self

    def rect_right_bottom(self):
        """
        获取右下角范围
        :return:
        """
        return self

    def rect_half_top(self):
        """
        获取上半屏范围
        :return:
        """
        return self

    def rect_half_bottom(self):
        """
        获取下半屏范围
        :return:
        """
        return self

    def rect_half_left(self):
        """
        获取左半屏范围
        :return:
        """
        return self

    def rect_half_right(self):
        """
        获取右半屏范围
        :return:
        """
        return self

    def rect_center(self):
        """
        获取中间范围
        :return:
        """
        return self


class AndroidCommonAction(CommonAction):
    """
    安卓的通用特征链式操作体，需要重新百分比点击方法，滑动方法
    """

    def __init__(self, selector: AScriptQueryElement, eleName, framework):
        pass

        rx, ry = Point(rx, ry).get_point()
        if x is not None and y is not None:
            x, y = Point(x, y).get_point()
            return
            return False
        else:
        return self


class NodeActionStrategy(AndroidCommonAction):
    """
    节点操作策略对象
    """

    def __init__(self, selector: NodeQuery, eleName, framework):
        pass

    def long_click(self):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        return self

    def 长按_节点(self):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        pass

    def input(self, msg: str):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        return self

    def 输入_文本(self, msg: str):
        """
        对查询到的节点信息输入文本
        """
        pass

