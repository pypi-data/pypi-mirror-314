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
from .device_api import UpdateDeviceRequest, InvokeMethodHTTPRequest


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
        body = {
            "workspaceID": request.workspace_id,
            "deviceHubName": request.device_hub_name,
            "deviceName": request.device_name,
            "displayName": request.display_name,
            "description": request.description,
            "tags": request.tags,
            "status": request.status,
            "category": request.category,
            "deptID": request.dept_id,
            "deviceGroupName": request.device_group_name
        }
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
            body=json.dumps(body),
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

        body = {
            "workspaceID": request.workspace_id,
            "deviceHubName": request.device_hub_name,
            "deviceName": request.device_name,
            "uri": request.uri,
            "params": request.params,
            "rawQuery": request.raw_query,
            "body": request.body
        }
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
            body=json.dumps(body),
        )
