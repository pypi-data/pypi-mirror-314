#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : conf
# Author  : zhoubohan
# Date    : 2024/11/28
# Time    : 20:51
# Description :
"""
import os
from typing import Any, List, Dict, Optional, Type

from baidubce.auth.bce_credentials import BceCredentials
from bceidaas.auth.iam_credentials import IAMCredentials
from bceidaas.auth.idaas_credentials import IDaaSCredentials
from bceidaas.bce_client_configuration import BceClientConfiguration
from pydantic import BaseModel

from bceserver.context.singleton_context import SingletonContext

ENV_SERVER_CONFIG_PATH = "SERVER_CONFIG_PATH"
DEFAULT_CONFIG_FILE_PATH = "conf/server/config.toml"

GLOBAL_CONFIG_KEY = "config"


class DBConfig(BaseModel):
    """
    DBConfig
    """

    driver: str
    host: str
    port: int
    user: str
    password: str
    db: str
    dsn_params: Optional[str]
    conn_max_idle_time: int
    conn_max_life_time: int
    max_idle_conns: int
    max_open_conns: int
    auto_migrate: bool


class FakeAuthConfig(BaseModel):
    """
    FakeAuthConfig
    """

    enable: bool
    org_id: str
    user_id: str
    user_name: str
    user_role: str
    department_id: str


class HTTPServerTraceConfig(BaseModel):
    """
    HTTPServerTraceConfig
    """

    prefix_filters: List[str]
    suffix_filters: List[str]


class HTTPServerConfig(BaseModel):
    """
    HTTPServerConfig
    """

    listen: Optional[str] = None
    auth_plugins: List[str] = None


class TenantConfig(BaseModel):
    """
    TenantConfig
    """

    endpoint: str
    permission_service_endpoint: Optional[str] = None
    permission_service_switch: Optional[str] = None
    redirect_login_url: Optional[str] = None


class PermissionConfig(BaseModel):
    """
    PermissionConfig
    """

    endpoint: str
    app_id: str
    switch: bool
    check_type: str


class RedisConfig(BaseModel):
    """
    RedisConfig
    """

    host: str
    port: int
    conn_timeout: int
    write_timeout: int
    read_timeout: int
    retry: int
    password: str
    db: int
    pool_size_per_ip: int
    min_idle_conns_per_ip: int


class Config(object):
    """
    Config class.
    """

    def __init__(
        self,
        app_name: str = "",
        run_mode: str = "",
        feature: Dict[str, Any] = None,
        db: DBConfig = None,
        tenant: TenantConfig = None,
        permission: PermissionConfig = None,
        redis: RedisConfig = None,
        fake_auth: FakeAuthConfig = None,
        http_server: HTTPServerConfig = None,
        iam: BceClientConfiguration = None,
        idaas: BceClientConfiguration = None,
    ):
        """
        Init config.
        """
        self.app_name = app_name
        self.run_mode = run_mode
        self.feature = feature
        self.db = db
        self.permission = permission
        self.redis = redis

        if http_server is not None:
            self.http_server = http_server
            if isinstance(http_server, HTTPServerConfig) is False:
                self.http_server = HTTPServerConfig(**http_server)

        if fake_auth is not None:
            self.fake_auth = fake_auth
            if isinstance(fake_auth, FakeAuthConfig) is False:
                self.fake_auth = FakeAuthConfig(**fake_auth)

        if tenant is not None:
            self.tenant = tenant
            if isinstance(tenant, TenantConfig) is False:
                self.tenant = TenantConfig(**tenant)

        if iam is not None:
            self.iam = iam
            if isinstance(iam, BceClientConfiguration) is False:
                iam = type("Object", (), iam)
                self.iam = BceClientConfiguration(
                    bce_credentials=BceCredentials(iam.ak, iam.sk),
                    iam_credentials=IAMCredentials(iam.user_name, iam.password),
                    endpoint=iam.endpoint,
                )

        if idaas is not None:
            self.idaas = idaas
            if isinstance(idaas, BceClientConfiguration) is False:
                idaas = type("Object", (), idaas)
                self.idaas = BceClientConfiguration(
                    idaas_credentials=IDaaSCredentials(
                        idaas.app_id,
                        idaas.client_id,
                        idaas.client_secret,
                    ),
                    endpoint=idaas.endpoint,
                )


def new_config() -> Config:
    """
    New config.
    """
    from toml import load

    config_file_path = DEFAULT_CONFIG_FILE_PATH
    if (
        os.environ.get(ENV_SERVER_CONFIG_PATH) is not None
        and os.environ.get(ENV_SERVER_CONFIG_PATH) != ""
    ):
        config_file_path = os.environ.get(ENV_SERVER_CONFIG_PATH)

    config_data = load(config_file_path)

    config = Config(**config_data)

    SingletonContext.instance().set_var_value(GLOBAL_CONFIG_KEY, config)

    return config
