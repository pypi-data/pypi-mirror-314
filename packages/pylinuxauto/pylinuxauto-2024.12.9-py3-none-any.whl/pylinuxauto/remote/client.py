#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

from xmlrpc.client import ServerProxy
from xmlrpc.client import Fault

from funnylog2 import logger
from pylinuxauto.config import config
from pylinuxauto.remote.guard import guard_rpc


@guard_rpc
def client(
        user: str,
        ip: str,
        password: str,
        auto_restart: bool = False,
) -> ServerProxy:
    try:
        return ServerProxy(f"http://{ip}:{config.RPC_PORT}", allow_none=True)
    except Fault as e:
        logger.error(f"XML-RPC Fault: {e.faultString}")
        raise RuntimeError(f"XML-RPC Fault: {e.faultString}")
    except ConnectionError as e:
        logger.error(f"Connection Error: {e}")
        raise RuntimeError(f"Connection Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise RuntimeError(f"Unexpected Error: {e}")
