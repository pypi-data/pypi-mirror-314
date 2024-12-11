# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
from pydantic import BaseModel
from typing import Optional, Any


class UpdateDeviceRequest(BaseModel):
    """
    Request for updating a device.
    """

    workspace_id: Optional[str] = None
    device_hub_name: Optional[str] = None
    device_name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[dict] = None
    status: Optional[str] = None
    device_group_name: Optional[str] = None
    category: Optional[str] = None
    dept_id: Optional[str] = None


class InvokeMethodHTTPRequest(BaseModel):
    """
    Request for invoking a method via HTTP.
    """

    workspace_id: Optional[str] = None
    device_hub_name: Optional[str] = None
    device_name: Optional[str] = None
    uri: Optional[str] = None
    body: Any = None
    params: Optional[dict] = None
    raw_query: Optional[str] = None
