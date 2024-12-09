# encoding:utf-8
from ascript.android.system import Device as AsDevice

from typing import TypeVar

class DeviceDisplayInfo:
    def __init__(self, width: int, height: int, density: int):
        """
        设备屏幕信息
        :param width: 屏幕宽度
        :param height: 屏幕高度
        :param density: 屏幕密度
        """
        self.width = width
        self.height = height
        self.density = density
        pass

    def __str__(self) -> str:
        pass


class RunningAppInfo:
    def __init__(self, name, packageName, activity):
        """
        当前运行APP信息
        :param name: 当前运行的APP名称
        :param packageName: 当前运行APP的包名称
        :param activity: 当前运行APP的Activity
        """
        self.name = name
        self.packageName = packageName
        self.activity = activity
        pass

    def __str__(self) -> str:
        pass


class AppInfo:
    def __init__(self, appName, appSize, isSd, isSystem, appPackageName, apkPath):
        """
        APP信息
        :param appName: APP名称
        :param appSize: app 大小
        :param isSd: 是否在SD卡中
        :param isSystem: 是否为系统应用
        :param appPackageName: app包名
        :param apkPath: 安装路径
        """
        self.appName = appName
        self.appSize = appSize
        self.isSd = isSd
        self.isSystem = isSystem
        self.appPackageName = appPackageName
        self.apkPath = apkPath
        pass

    def __str__(self) -> str:
        pass


ListAppInfo = TypeVar('ListAppInfo', bound='list[AppInfo]')


class MemoryInfo:

    def __init__(self, free, used, total):
        """
        内存信息
        :param free: 空闲内存
        :param used: 已使用内存
        :param total: 总内存
        """
        self.free = free
        self.used = used
        self.total = total
        pass

    def __str__(self) -> str:
        pass


class Device:

    @staticmethod
    def get_device_id() -> str:
        """
        获取设备ID
        """
        pass

    @staticmethod
    def get_device_name() -> str:
        """
        获取设备名称
        """
        pass

    @staticmethod
    def get_device_display() -> DeviceDisplayInfo:
        """
        获取设备屏幕信息
        """
        pass

    @staticmethod
    def get_device_brand() -> str:
        """
        获取设备品牌
        """
        pass

    @staticmethod
    def get_device_model() -> str:
        """
        获取设备型号
        """
        pass

    @staticmethod
    def get_device_sdk() -> str:
        """
        获取设备sdk
        """
        pass

    @staticmethod
    def get_device_version() -> str:
        """
        获取设备Android版本
        """
        pass

    @staticmethod
    def get_device_ip() -> str:
        """
        获取设备IP地址
        """
        pass

    @staticmethod
    def get_current_appinfo() -> RunningAppInfo:
        """
        获取当前设备运行的APP信息
        """
        pass

    @staticmethod
    def get_all_install_app() -> ListAppInfo:
        """
        获取所有已安装APP的信息
        """
        pass

    @staticmethod
    def get_current_battery() -> int:
        """
        获取当前电量
        """
        pass

    @staticmethod
    def get_device_memory() -> MemoryInfo:
        """
        获取内存信息
        """
        pass


class 设备:

    @staticmethod
    def 获取_设备ID() -> str:
        """
        获取设备ID
        """
        pass

    @staticmethod
    def 获取_设备名称() -> str:
        """
        获取设备ID
        """
        pass

    @staticmethod
    def 获取_设备屏幕信息() -> DeviceDisplayInfo:
        """
        获取设备屏幕信息
        """
        pass

    @staticmethod
    def 获取_设备品牌() -> str:
        """
        获取设备品牌
        """
        pass

    @staticmethod
    def 获取_设备型号() -> str:
        """
        获取设备型号
        """
        pass

    @staticmethod
    def 获取_设备SDK() -> str:
        """
        获取设备SDK
        """
        pass

    @staticmethod
    def 获取_设备版本() -> str:
        """
        获取设备Android版本
        """
        pass

    @staticmethod
    def 获取_设备IP() -> str:
        """
        获取设备Android版本
        """
        pass

    @staticmethod
    def 获取_当前运行APP信息() -> RunningAppInfo:
        """
        获取设备Android版本
        """
        pass

    @staticmethod
    def 获取_所有安装APP() -> ListAppInfo:
        """
        获取设备Android版本
        """
        pass

    @staticmethod
    def 获取_当前电量() -> int:
        """
        获取设备Android版本
        """
        pass

    @staticmethod
    def 获取_设备内存() -> MemoryInfo:
        """
        获取设备Android版本
        """
        pass


__all__ = ['Device', '设备']
