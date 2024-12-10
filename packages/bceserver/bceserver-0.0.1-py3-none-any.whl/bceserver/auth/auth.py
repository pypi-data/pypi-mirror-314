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
from bceidaas.middleware.auth.iam_session import (
    IAMSessionMiddleware,
    iam_session_handler,
)
from bceidaas.middleware.auth.idaas_session import (
    IDaasSessionMiddleware,
    idaas_session_handler,
)
from fastapi import FastAPI

from bceserver.auth.fake import FakeAuthMiddleware, fake_auth_with_id
from bceserver.auth.plugins import Plugins
from bceserver.conf.conf import Config
from bceserver.auth.consts import (
    GLOBAL_CONFIG_KEY,
    GLOBAL_IAM_CLIENT_KEY,
    GLOBAL_IDAAS_CLIENT_KEY,
    GLOBAL_TENANT_CLIENT_KEY,
    FAKE,
)
from bceserver.context.singleton_context import SingletonContext
from tenantv1.middleware.middleware import TenantMiddleware, tenant_handler


def use(app: FastAPI, config: Config):
    """
    Use auth middleware.
    """
    context_manager = SingletonContext.instance()
    context_manager.set_var_value(GLOBAL_CONFIG_KEY, config)

    auth_plugins = Plugins(config)
    context_manager.set_var_value(GLOBAL_IAM_CLIENT_KEY, auth_plugins.iam_client)
    context_manager.set_var_value(GLOBAL_IDAAS_CLIENT_KEY, auth_plugins.idaas_client)
    context_manager.set_var_value(GLOBAL_TENANT_CLIENT_KEY, auth_plugins.tenant_client)

    if auth_plugins.tenant_client is not None:
        app.add_middleware(TenantMiddleware)

    if auth_plugins.contains(auth.IDAAS_SESSION):
        app.add_middleware(IDaasSessionMiddleware)

    if auth_plugins.contains(auth.IAM_SESSION):
        app.add_middleware(IAMSessionMiddleware)

    if auth_plugins.contains(FAKE):
        app.add_middleware(FakeAuthMiddleware)


def handle(cookies: str, config: Config):
    context_manager = SingletonContext.instance()
    context_manager.set_var_value(GLOBAL_CONFIG_KEY, config)

    auth_plugins = Plugins(config)
    context_manager.set_var_value(GLOBAL_IAM_CLIENT_KEY, auth_plugins.iam_client)
    context_manager.set_var_value(GLOBAL_IDAAS_CLIENT_KEY, auth_plugins.idaas_client)
    context_manager.set_var_value(GLOBAL_TENANT_CLIENT_KEY, auth_plugins.tenant_client)

    auth_info = {}
    # 优先级：Fake > IAMAuthorization > IDaaSAuthorization > IAMSession > IDaaSSession
    if auth_plugins.contains(FAKE):
        auth_info = fake_auth_with_id(config)
    if auth_plugins.contains(auth.IAM_AUTH):
        pass
    if auth_plugins.contains(auth.IDAAS_AUTH):
        pass
    if auth_plugins.contains(auth.IAM_SESSION):
        auth_info = iam_session_handler(cookies, auth_plugins.iam_client)
    if auth_plugins.contains(auth.IDAAS_SESSION):
        auth_info = idaas_session_handler(cookies, auth_plugins.idaas_client)

    if auth_plugins.tenant_client is not None:
        auth_info = tenant_handler(auth_info, auth_plugins.tenant_client)

    return auth_info
