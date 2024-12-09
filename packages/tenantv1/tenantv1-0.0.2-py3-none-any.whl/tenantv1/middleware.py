#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : tenant_middleware
# Author  : zhoubohan
# Date    : 2024/12/6
# Time    : 20:33
# Description :
"""
import logging
from typing import Callable

from bceidaas.middleware.auth import auth
from bceserver.auth.consts import (
    GLOBAL_AUTH_INFO_KEY,
    GLOBAL_CONFIG_KEY,
)
from bceserver.context.singleton_context import SingletonContext
from fastapi import Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from tenantv1.api import (
    ErrorResult,
    Message,
    IAMInfoRequest,
    UserDepartmentRequest,
    DEPARTMENT_NAME,
    DEPARTMENT_ID,
)
from tenantv1.client import TenantClient


class TenantMiddleware(BaseHTTPMiddleware):
    """
    TenantMiddleware
    """

    async def dispatch(self, request: Request, call_next: Callable):
        """
        dispatch
        :param request:
        :param call_next:
        :return:
        """
        context_manager = SingletonContext.instance()
        tenant_client: TenantClient = context_manager.get_var_value("tenant_client")
        global_config = context_manager.get_var_value(GLOBAL_CONFIG_KEY)
        err_result = ErrorResult(
            code="UserDepartmentFail",
            message=Message(redirect=global_config.tenant.redirect_login_url),
            success=False,
        )

        auth_info = request.state.auth_info
        org_id = auth_info.get(auth.ORG_ID, "")
        user_id = auth_info.get(auth.USER_ID, "")
        auth_mode = auth_info.get(auth.AUTH_MODE, "")

        if len(org_id) == 0 or len(user_id) == 0:
            logging.error("TenantMiddlewareError: org_id or user_id is empty.")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=err_result.model_dump(),
            )

        if auth_mode.startswith("IAM"):
            user_info = tenant_client.get_tenant_user_by_iam_info(
                IAMInfoRequest(iam_account_id=org_id, iam_user_id=user_id)
            )

            if (
                user_info.result is None
                or user_info.result.tenant_id is None
                or user_info.result.idaas_user_id is None
            ):
                logging.error(
                    "TenantMiddlewareError: get_tenant_user_by_iam_info failed."
                )
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=err_result.model_dump(),
                )

            org_id = user_info.result.tenant_id
            user_id = user_info.result.idaas_user_id
            auth_info[auth.ORG_ID] = org_id
            auth_info[auth.USER_ID] = user_id

        department_info = tenant_client.get_user_department(
            UserDepartmentRequest(user_id=user_id)
        )

        if (
            department_info.result is None
            or department_info.result.department_id is None
        ):
            logging.error(
                f"TenantMiddlewareError: get_user_department failed. user_id: {user_id}"
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=err_result.model_dump(),
            )

        auth_info[DEPARTMENT_ID] = department_info.result.department_id
        auth_info[DEPARTMENT_NAME] = department_info.result.department_name

        request.state.auth_info = auth_info

        SingletonContext.instance().set_var_value(GLOBAL_AUTH_INFO_KEY, auth_info)

        return await call_next(request)
