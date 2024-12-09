# encoding:utf-8
import time

from typing import TypeVar, Union

from .Logger import log_ld

class Rect:
    """
    获取控件在屏幕中的位置

    left x坐标

    top y坐标

    width 控件的宽度

    height 控件的高度

    centerX 控件的中心坐标X

    centerY 控件的中心坐标Y
    """

    def __init__(self, left=None, top=None, width=None, height=None, centerX=None, centerY=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        pass


class CommonResult:
    """
    查询元素的公共返回体
    """

    def __init__(self, source_target, rect: Rect):
        """
        调用获取元素方法后拿到的返回结果，经过统一包装
        :param source_target: 查询后的源对象
        :param rect: 查询后得到的坐标信息对象，要自行包装
        """
        self.target = source_target
        self.rect: Rect = rect
        pass


class AScriptQueryElement:
    """
    AS元素查询父类，所有的元素查询都需要继承该类
    """

    def rect_left_top(self):
        """
        获取左上角范围
        :return:
        """
        pass

    def rect_right_top(self):
        """
        获取右上角范围
        :return:
        """
        pass

    def rect_left_bottom(self):
        """
        获取左下角范围
        :return:
        """
        pass

    def rect_right_bottom(self):
        """
        获取右下角范围
        :return:
        """
        pass

    def rect_half_top(self):
        """
        获取上半屏范围
        :return:
        """
        pass

    def rect_half_bottom(self):
        """
        获取下半屏范围
        :return:
        """
        pass

    def rect_half_left(self):
        """
        获取左半屏范围
        :return:
        """
        pass

    def rect_half_right(self):
        """
        获取右半屏范围
        :return:
        """
        pass

    def rect_center(self):
        """
        获取中间范围
        :return:
        """
        pass


class Method:
    def __init__(self, target, *args, **kwargs):
        self.ref = None
        self.target = target
        self.args = args
        self.kwargs = kwargs
        pass

    def execute(self):
        pass


CommonActionType = TypeVar('CommonActionType', bound='CommonAction | None')


class CommonAction:

    def __init__(self, selector: AScriptQueryElement, eleName, framework):
        # 查询对象
        # 对框架本身的引用，只要被实例化就绝对不可能为空
        # 当前查询元素的特征信息
        # 用来存放操作的链
        # 查询元素以后的返回值
        pass

    def execute(self, sleep=0.5, loop=1):
        """
        执行动作链
        :param sleep: 执行一次延迟时间，单位（秒）
        :param loop:执行次数
        """
                        # 如果是等待元素之类的任务，需要有元素才可以继续
            # 执行完了以后要清空链，以防重复调用的时候出问题
        pass

    def 执行(self, sleep=0.5, loop=1):
        pass

    def element(self, *args: str) -> CommonActionType:
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        return self

    def 元素_操作(self, *args: str) -> CommonActionType:
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        pass

    def sleep(self, second) -> CommonActionType:
        """
        延迟
        :param second:延迟时间，单位秒
        """
        return self

    def 延迟(self, second) -> CommonActionType:
        """
        延迟
        :param second:延迟时间，单位秒
        """
        pass

    def ramdom_sleep(self, second, float_tame=0.3) -> CommonActionType:
        """
        随机延迟时间范围，从(second - float_tame) ~ (second + float_tame)范围内随机延迟
        :param second:延迟时间，单位秒
        :param float_tame:浮动时间
        """
        return self

    def 随机_延迟(self, second, float_tame=0.3) -> CommonActionType:
        """
        随机延迟时间范围，从(second - float_tame) ~ (second + float_tame)范围内随机延迟

        :param second:延迟时间，单位秒
        :param float_tame:浮动时间
        """
        pass

    def assert_element(self, condition) -> CommonActionType:
        """
        断言
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda，如果返回False，则不执行后面的链
        """
        return self

    def 断言_元素(self, condition) -> CommonActionType:
        """
        断言
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda，如果返回False，则不执行后面的链
        """
        pass

    def execute_method(self, method) -> CommonActionType:
        """
        执行一个方法，如果方法返回False，则不继续执行后面的链
        :param method:需要执行的方法
        """
        return self

    def 执行_方法(self, method) -> CommonActionType:
        """
        执行一个方法，如果方法返回False，则不继续执行后面的链
        :param method:需要执行的方法
        """
        pass

    @staticmethod
    def click(self, x=None, y=None, r=5, rx: int = 0, ry: int = 0, dur: float = 20) -> CommonActionType:
        """
        点击某个坐标，如果不穿参数，则是点击找到元素的位置
        :param x:屏幕的绝对x坐标，和y一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param y:屏幕的绝对y坐标，和x一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param r:随机偏移坐标，以x,y为中心，点击的时候偏移r个像素
        :param rx:相对坐标x，以x（不管是元素的还是传入的）为中心加上rx作为点击的偏移像素
        :param ry:相对坐标y，以y（不管是元素的还是传入的）为中心加上ry作为点击的偏移像素
        :param dur:点击持续时间,默认20毫秒
        """
        return self

    def 点击_坐标(self, x=None, y=None, r=5, rx: int = 0, ry: int = 0, dur: float = 20) -> CommonActionType:
        """
        点击某个坐标，如果不穿参数，则是点击找到元素的位置
        :param x:屏幕的绝对x坐标，和y一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param y:屏幕的绝对y坐标，和x一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param r:随机偏移坐标，以x,y为中心，点击的时候偏移r个像素
        :param rx:相对坐标x，以x（不管是元素的还是传入的）为中心加上rx作为点击的偏移像素
        :param ry:相对坐标y，以y（不管是元素的还是传入的）为中心加上ry作为点击的偏移像素
        :param dur:点击持续时间,默认20毫秒
        """
        pass

        if x is not None and y is not None:
            return
            return False
        else:
        return self

    def click_element(self, r=5) -> CommonActionType:
        """
        如果是节点，该方法是点击节点，如果是其他元素，则是坐标，偏移参数对点击节点无效
        :param r: 偏移像素
        """
        return self

    def 点击_元素(self, r=5) -> CommonActionType:
        """
        如果是节点，该方法是点击节点，如果是其他元素，则是坐标，偏移参数对点击节点无效
        :param r: 偏移像素
        """
        pass

    def wait_element(self, element: list, timeout=3) -> CommonActionType:
            # 如果是元素等待开头，则说明一开始不用查找
        return self

    def 元素_等待(self, element: list, timeout=3) -> CommonActionType:
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

        def tmp():
            pass

        if ele is None:
            return False
        return ele

    def swipe(self, from_point: [Union[str, int], Union[str, int]], to_point: [Union[str, int], Union[str, int]],
              timeout=0.2, will_continue=False) -> CommonActionType:
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间，单位(秒)
        :param will_continue: 结束时候是否抬起手指
        """
        return self

    def 滑动(self, from_point: [Union[str, int], Union[str, int]], to_point: [Union[str, int], Union[str, int]],
             timeout=0.2, will_continue=False) -> CommonActionType:
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间
        :param will_continue: 结束时候是否抬起手指
        """
        return self.swipe(from_point, to_point, timeout, will_continue)

    def compare_color(self, *args) -> CommonActionType:
        return self

    def 比色(self, *args) -> CommonActionType:
        return self.compare_color(*args)
