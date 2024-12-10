#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : plugins
# Author  : zhoubohan
# Date    : 2024/11/29
# Time    : 11:56
# Description :
"""
from tenantv1.client.tenant_client import TenantClient
from bceidaas.services.iam.iam_client import IAMClient
from bceidaas.services.idaas.idaas_client import IDaaSClient
from bceidaas.middleware.auth.const import (
    IAM_AUTH,
    IAM_SESSION,
    IDAAS_AUTH,
    IDAAS_SESSION,
)

from bceserver.conf.conf import Config
from bceserver.auth.consts import FAKE


class Plugins(object):
    """
    Plugins
    """

    def __init__(self, config: Config):
        """
        init
        :param config:
        """
        try:
            self.plugins = config.http_server.auth_plugins
            self.set_default()

            if config.iam is not None:
                self.iam_client = IAMClient(config.iam)

            if config.idaas is not None:
                self.idaas_client = IDaaSClient(config.idaas)

            if config.tenant is not None:
                self.tenant_client = TenantClient(endpoint=config.tenant.endpoint)

            self.check()
        except Exception as e:
            raise ValueError("Plugins init failure. " + str(e))

    def set_default(self):
        """
        set_default
        """
        if self.plugins is None or len(self.plugins) == 0:
            self.plugins = [FAKE]

    def check(self):
        """
        check
        """
        if FAKE in self.plugins:
            for plugin in self.plugins:
                if plugin != FAKE:
                    return ValueError(
                        "Plugins check failure. Fake and other plugins can't exist at the same time."
                    )

        contains_iam = IAM_AUTH in self.plugins or IAM_SESSION in self.plugins
        if contains_iam and not self.iam_client:
            raise ValueError(
                "Plugins check failure. IAM client wasn't initialized, "
                "can't use IAMAuthorization or IAMSession plugin."
            )

        contains_idaas = IDAAS_AUTH in self.plugins or IDAAS_SESSION in self.plugins
        if contains_idaas and not self.idaas_client:
            raise ValueError(
                "Plugins check failure. IDaaS client wasn't initialized,"
                " can't use IDaaSAuthorization or IDaaSSession plugin."
            )

    def contains(self, plugin: str) -> bool:
        """
        contains
        :param plugin:
        :return:
        """
        return plugin in self.plugins
