#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : api
# Author  : light
# Date    : 2024/12/6
# Time    : 17:46
# Description :
"""
from typing import Optional, Any

from bceinternalsdk.client.base_model import BaseModel

DEPARTMENT_ID = "DepartmentId"
DEPARTMENT_NAME = "DepartmentName"


class Message(BaseModel):
    """
    Message
    """

    redirect: Optional[str] = None


class ErrorResult(BaseModel):
    """
    ErrorResult
    """

    code: Optional[str] = None
    message: Optional[Message] = None
    success: Optional[bool] = None


class TenantUserId(BaseModel):
    """
    TenantUserId
    """

    tenant_id: Optional[str] = None
    idaas_user_id: Optional[str] = None


class IAMInfoRequest(BaseModel):
    """
    IAMInfoRequest
    """

    iam_account_id: str
    iam_user_id: str


class TenantUserResponse(BaseModel):
    """
    TenantUserResponse
    """

    success: bool
    message: Any
    result: Optional[TenantUserId] = None


class UserDepartmentRequest(BaseModel):
    """
    UserDepartmentRequest
    """

    user_id: str


class UserDepartment(BaseModel):
    """
    UserDepartment
    """

    department_id: Optional[str] = None
    department_name: Optional[str] = None


class UserDepartmentResponse(BaseModel):
    """
    UserDepartmentResponse
    """

    success: bool
    message: Any
    result: Optional[UserDepartment] = None
