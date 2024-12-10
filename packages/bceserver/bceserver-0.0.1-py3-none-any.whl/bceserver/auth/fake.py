#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : fake
# Author  : zhoubohan
# Date    : 2024/11/29
# Time    : 12:17
# Description :
"""
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from bceidaas.middleware.auth.const import (
    ORG_ID,
    USER_ID,
    USER_NAME,
    USER_ROLE,
)

from bceserver.auth.consts import GLOBAL_AUTH_INFO_KEY, DEPARTMENT_ID
from bceserver.conf.conf import Config, GLOBAL_CONFIG_KEY
from bceserver.context.singleton_context import SingletonContext


class FakeAuthMiddleware(BaseHTTPMiddleware):
    """
    FakeAuthMiddleware
    """

    async def dispatch(self, request: Request, call_next: Callable):
        """
        dispatch
        :param request:
        :param call_next:
        :return:
        """
        config: Config = SingletonContext.instance().get_var_value(GLOBAL_CONFIG_KEY)

        auth_info_context = fake_auth_with_id(config)

        request.state.auth_info = auth_info_context

        return await call_next(request)


def fake_auth_with_id(config: Config) -> dict:
    """
    Fake auth with id.
    """
    if config.fake_auth.org_id == "":
        config.fake_auth.org_id = "test-org-id"

    if config.fake_auth.user_id == "":
        config.fake_auth.user_id = "test-user-id"

    if config.fake_auth.user_name == "":
        config.fake_auth.user_name = "test-user-name"

    if config.fake_auth.user_role == "":
        config.fake_auth.user_role = "test-user-role"

    if config.fake_auth.department_id == "":
        config.fake_auth.department_id = "test-department-id"

    auth_info_context = {
        ORG_ID: config.fake_auth.org_id,
        USER_ID: config.fake_auth.user_id,
        USER_NAME: config.fake_auth.user_name,
        USER_ROLE: config.fake_auth.user_role,
        DEPARTMENT_ID: config.fake_auth.department_id,
    }

    SingletonContext.instance().set_var_value(GLOBAL_AUTH_INFO_KEY, auth_info_context)

    return auth_info_context
