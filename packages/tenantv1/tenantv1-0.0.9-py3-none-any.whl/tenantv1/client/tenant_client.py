#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : client
# Author  : zhoubohan
# Date    : 2024/12/6
# Time    : 17:23
# Description :
"""
from typing import Optional

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.http import http_methods, http_content_types
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from tenantv1.client.tenant_api import (
    IAMInfoRequest,
    TenantUserResponse,
    UserDepartmentRequest,
    UserDepartmentResponse,
)


class TenantClient(BceInternalClient):
    """
    Tenant Client
    """

    def __init__(
        self,
        config: Optional[BceClientConfiguration] = None,
        ak: Optional[str] = "",
        sk: Optional[str] = "",
        endpoint: Optional[str] = "",
        context: Optional[dict] = None,
    ):
        """
        Init
        :param config:
        :param ak:
        :param sk:
        :param endpoint:
        :param context:
        """

        self._base_uri = "/api/org/v1/org/sdk/"
        self._headers = {
            b"Content-Type": http_content_types.JSON,
            b"iipI5j87cJ#nMoFl&HyU$OX1manage":
            "key@NX9e4#G(3ClY@&hsjyLx22s2@key",
        }

        super(TenantClient, self).__init__(config=config,
                                           ak=ak,
                                           sk=sk,
                                           endpoint=endpoint,
                                           context=context)

    def _build_path(self, path: str):
        return bytes(
            f"{self._base_uri}/{path}",
            encoding="utf-8",
        )

    def get_tenant_user_by_iam_info(
            self, request: IAMInfoRequest) -> TenantUserResponse:
        """
        Get tenant user by iam info
        :param request:
        :return:
        """
        response = self._send_request(
            http_method=http_methods.POST,
            path=self._build_path("getTenantUserByIamInfo"),
            headers=self._headers,
            body=request.json(),
        )

        return TenantUserResponse.from_response(response)

    def get_user_department(
            self, request: UserDepartmentRequest) -> UserDepartmentResponse:
        """
        Get user department
        :param request:
        :return:
        """
        response = self._send_request(
            http_method=http_methods.POST,
            path=self._build_path("getDepartmentByUserId"),
            params=request.model_dump(by_alias=True),
            headers=self._headers,
            body=request.json(),
        )

        return UserDepartmentResponse.from_response(response)
