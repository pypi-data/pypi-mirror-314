#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import inspect
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def server(obj, port):
    server = ThreadXMLRPCServer(("0.0.0.0", port), allow_none=True)
    methods = inspect.getmembers(obj, predicate=inspect.isfunction)
    for func_name, _ in methods:
        if not func_name.startswith("_"):
            server.register_function(getattr(obj(), func_name), func_name)
    print(f"Server listening on port {port}")
    server.serve_forever()


if __name__ == '__main__':
    from pylinuxauto.remote.methods import Methods
    from pylinuxauto.config import config

    server(Methods, config.RPC_PORT)
