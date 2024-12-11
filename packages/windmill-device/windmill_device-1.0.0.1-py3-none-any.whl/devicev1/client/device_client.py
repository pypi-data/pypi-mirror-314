# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import json
from baidubce.http import http_methods
from baidubce.http import http_content_types
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from device_api import UpdateDeviceRequest, InvokeMethodHTTPRequest


class DeviceClient(BceInternalClient):
    """
    A client class for interacting with the windmill device service. 
    """

    def update_device(
            self,
            request: UpdateDeviceRequest):
        """
        Update a device.

        Args:
            request (UpdateDeviceRequest): 更新设备请求
        Returns:
             HTTP request response
        """

        return self._send_request(
            http_method=http_methods.PUT,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + request.workspace_id
                + "/devicehubs/"
                + request.device_hub_name
                + "/devices/"
                + request.device_name,
                encoding="utf-8",
            ),
            body=request.model_dump_json(by_alias=True).encode("utf-8"),
        )

    def invoke_method_http(
            self,
            request: InvokeMethodHTTPRequest):
        """
        Invoke a method via HTTP.
        Args:
            request (InvokeMethodHTTPRequest): 调用方法HTTP请求
        Returns:
            HTTP request response
        """

        return self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + request.workspace_id
                + "/devicehubs/"
                + request.device_hub_name
                + "/devices/"
                + request.device_name
                + "/invokemethods/http/"
                + request.uri,
                encoding="utf-8",
            ),
            body=request.model_dump_json(by_alias=True).encode("utf-8"),
        )
