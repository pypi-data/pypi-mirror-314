#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : auth
# Author  : zhoubohan
# Date    : 2024/11/27
# Time    : 23:39
# Description :
"""
import bceidaas.middleware.auth.const as auth
from bceidaas.middleware.auth.utils import convert_cookie_to_dict
from bceidaas.middleware.auth.iam_session import (
    IAMSessionMiddleware,
    iam_session_handler,
)
from bceidaas.middleware.auth.idaas_session import (
    IDaasSessionMiddleware,
    idaas_session_handler,
)
from bceserver.auth.consts import (
    GLOBAL_CONFIG_KEY,
    GLOBAL_IAM_CLIENT_KEY,
    GLOBAL_IDAAS_CLIENT_KEY,
    GLOBAL_TENANT_CLIENT_KEY,
    FAKE,
    GLOBAL_AUTH_INFO_KEY,
)
from bceserver.auth.fake import FakeAuthMiddleware, fake_auth_with_id
from bceserver.auth.plugins import Plugins
from bceserver.conf.conf import Config
from bceserver.context.singleton_context import SingletonContext
from fastapi import FastAPI, Request, HTTPException
from ray.air.examples.custom_trainer import result
from starlette import status
from tenantv1.middleware.middleware import TenantMiddleware, tenant_handler


def use(app: FastAPI, config: Config):
    """Use auth middleware."""
    context = SingletonContext.instance()
    context.set_var_value(GLOBAL_CONFIG_KEY, config)

    plugins = Plugins(config)
    _set_clients(context, plugins)
    _add_middlewares(app, plugins)


def auth_handle(cookies: str, config: Config):
    """Handle auth without fastapi"""
    context = SingletonContext.instance()
    context.set_var_value(GLOBAL_CONFIG_KEY, config)

    plugins = Plugins(config)
    _set_clients(context, plugins)

    return _process_auth(cookies, plugins)


def get_authenticate_dependency(config: Config):
    """Get authenticate dependency."""
    context = SingletonContext.instance()
    context.set_var_value(GLOBAL_CONFIG_KEY, config)

    plugins = Plugins(config)
    _set_clients(context, plugins)

    async def authenticate(request: Request):
        result = _process_auth(request.cookies, plugins)
        if isinstance(result, Exception):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "Unauthorized",
                    "message": str(result),
                },
            )

        setattr(request.state, GLOBAL_AUTH_INFO_KEY, result)
        context.set_var_value(GLOBAL_AUTH_INFO_KEY, result)

    return authenticate


def _set_clients(context, plugins):
    """Set authentication clients in context."""
    context.set_var_value(GLOBAL_IAM_CLIENT_KEY, plugins.iam_client)
    context.set_var_value(GLOBAL_IDAAS_CLIENT_KEY, plugins.idaas_client)
    context.set_var_value(GLOBAL_TENANT_CLIENT_KEY, plugins.tenant_client)


def _add_middlewares(app, plugins):
    """Add authentication middlewares to app."""
    if plugins.tenant_client:
        app.add_middleware(TenantMiddleware)
    if plugins.contains(auth.IDAAS_SESSION):
        app.add_middleware(IDaasSessionMiddleware)
    if plugins.contains(auth.IAM_SESSION):
        app.add_middleware(IAMSessionMiddleware)
    if plugins.contains(FAKE):
        app.add_middleware(FakeAuthMiddleware)


def _process_auth(cookies, plugins):
    """Process authentication based on plugins."""
    if plugins.contains(FAKE):
        return fake_auth_with_id(plugins.config)

    result = {}
    if plugins.contains(auth.IAM_SESSION):
        result = iam_session_handler(cookies, plugins.iam_client)
        if isinstance(result, Exception):
            return result

    if plugins.contains(auth.IDAAS_SESSION):
        result = idaas_session_handler(cookies, plugins.idaas_client)
        if isinstance(result, Exception):
            return result

    if plugins.tenant_client:
        result = tenant_handler(result, plugins.tenant_client)
        if isinstance(result, Exception):
            return result

    if isinstance(cookies, dict):
        cookie_dict = cookies
    else:
        cookie_dict = convert_cookie_to_dict(cookies)

    result["project_name"] = cookie_dict.get("projectId")

    return result
