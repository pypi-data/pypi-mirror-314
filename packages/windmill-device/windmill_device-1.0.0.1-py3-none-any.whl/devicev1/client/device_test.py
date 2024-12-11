# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import unittest
import json
from device_api import InvokeMethodHTTPRequest, UpdateDeviceRequest


class TestDevice(unittest.TestCase):
    """
    Test Device
    """

    def test_device_invoke_request(self):
        """
        Test invoke request
        """
        req = InvokeMethodHTTPRequest(
            workspaceID="ws01",
            deviceHubName="dh01",
            deviceName="dev01",
            uri="/test",
            body={"hello": "world"})
        print(req.model_dump_json(by_alias=True).encode("utf-8"))

    def test_device_request(self):
        """
        Test update request
        """
        req = UpdateDeviceRequest(
            workspaceID="ws01",
            deviceHubName="dh01",
            deviceName="dev01",
            properties={"key": "value"},
            tags={"tag1": 12},
            metadata={},
            attributes={})
        print(req.model_dump_json(by_alias=True).encode("utf-8"))


if __name__ == '__main__':
    unittest.main()
