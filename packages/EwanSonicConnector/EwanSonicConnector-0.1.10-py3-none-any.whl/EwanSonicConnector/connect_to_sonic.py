import subprocess
import redis
import requests
from contextlib import contextmanager
import functools
from airtest.core.api import *


class Remote(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __getattr__(self, item):
        return super().__getitem__(item)


remote = Remote()


class SonicApi:
    def __init__(self, host, user_name, password, redis_connection, **kwargs):
        self.redis = redis.from_url(redis_connection)
        self.host, self.user_name, self.password = host, user_name, password
        self.session = requests.session()
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def check_token(self):
        sonic_token = self.redis.get("sonic_token")
        return {"SonicToken": sonic_token} if sonic_token else self.get_token()

    def get_token(self):
        url = f"{self.host}/server/api/controller/users/login"
        json = {
            "userName": self.user_name,
            "password": self.password
        }
        try:
            res = self.session.post(url, json=json)
            self.check_response(res)
            sonic_token = res.json()["data"]
        except Exception as e:
            raise Exception("登录接口报错") from e
        else:
            self.redis.set("sonic_token", sonic_token)
            self.redis.expire("sonic_token", 60 * 60 * 24 - 10)
            return {"SonicToken": sonic_token}

    def get_all_devices(self, payload):
        url = f"{self.host}/server/api/controller/devices/list"
        res = self.session.get(url, params=payload, headers=self.check_token)
        self.check_response(res)
        return res.json().get('data').get('content')

    def occupy_device(self, udid):
        url = f"{self.host}/server/api/controller/devices/occupy"
        json = {
            "udId": udid,
            "sasRemotePort": 30000,
            "uia2RemotePort": 30001,
            "sibRemotePort": 30002,
            "wdaServerRemotePort": 30003,
            "wdaMjpegRemotePort": 30004
        }
        res = self.session.post(url, headers=self.check_token, json=json)
        self.check_response(res)
        return res.json().get('data')

    def release_device(self, udid):
        url = f"{self.host}/server/api/controller/devices/release"
        params = {
            "udId": udid
        }
        res = self.session.get(url, headers=self.check_token, params=params)
        self.check_response(res)
        return res.json()

    @staticmethod
    def check_response(response):
        """检查响应的通用方法"""
        if response.status_code != 200:
            raise Exception(f"请求失败，HTTP 状态码: {response.status_code}")
        if response.json().get('code') != 2000:
            raise Exception(f"请求失败，响应码: {response.json().get('code')}, 信息: {response.json().get('message')}")

    @contextmanager
    def device_session(self, udid):
        devices = self.get_all_devices({'page': 1, 'pageSize': 100})
        online_device = next((item for item in devices if item.get('udId') == udid), None)
        if not online_device or online_device['status'] != 'ONLINE':
            raise Exception("设备不在线或不存在。")

        try:
            print(f'开始连接设备:{udid}')
            subprocess.run(["adb", "start-server"], check=True)
            time.sleep(3)
            command = self.occupy_device(udid)
            for k, v in {**online_device, **command}.items():
                setattr(remote, k, v)
            yield remote
        finally:
            print(f'开始释放设备：{udid}')
            time.sleep(3)
            subprocess.run(["adb", "kill-server"], check=True)
            self.release_device(udid)

    @staticmethod
    def with_device_session(test_func):
        @functools.wraps(test_func)
        def wrapper(instance, *args, **kwargs):
            sonic_api = instance.sonic_api
            udid = instance.udid
            result = None
            with sonic_api.device_session(udid) as remote:
                if remote:
                    result = test_func(instance, remote, *args, **kwargs)
            return result

        return wrapper


class BaseDeviceTest:
    def __init__(self, sonic_api, udid):
        self.sonic_api = sonic_api
        self.udid = udid

    @classmethod
    def setup(cls):
        """用户可以在这里自定义前置操作"""
        print("默认前置操作")

    @classmethod
    def teardown(cls):
        """用户可以在这里自定义后置操作"""
        print("默认后置操作")

    def run_test(self):
        self.setup()
        try:
            self.ui_auto_test()
        finally:
            self.teardown()

    def ui_auto_test(self, remote):
        """用户需要实现的测试逻辑"""
        raise NotImplementedError("请实现测试逻辑")
