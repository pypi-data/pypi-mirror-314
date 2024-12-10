#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from pylinuxauto.remote.client import client
from pylinuxauto.remote.methods import Methods


def remote_pylinuxauto(
        user: str,
        ip: str,
        password: str,
        auto_restart: bool = False,

) -> Methods:
    return client(
        user=user,
        ip=ip,
        password=password,
        auto_restart=auto_restart,
    )
