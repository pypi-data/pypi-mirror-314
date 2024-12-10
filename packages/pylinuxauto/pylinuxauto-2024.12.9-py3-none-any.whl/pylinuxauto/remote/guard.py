#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import functools
import os.path
import shutil
import time

from funnylog2 import logger
from nocmd import Cmd
from nocmd import RemoteCmd

from pylinuxauto.config import config


class RemotePyLinuxAutoManager:
    def __init__(self, user, ip, password, service_name, client_rootdir, tmp_service_file, tmp_server_py):
        self.user = user
        self.ip = ip
        self.password = password
        self.service_name = service_name
        self.client_rootdir = client_rootdir
        self.tmp_service_file = tmp_service_file
        self.tmp_server_py = tmp_server_py

    def transfer_to_client(self):
        rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
        remote_cmd = RemoteCmd(self.user, self.ip, self.password)
        stdout, return_code = remote_cmd.remote_run(f"ls {self.client_rootdir} > /dev/null 2>&1", return_code=True)
        if return_code != 0:
            remote_cmd.remote_run(f"mkdir -p {self.client_rootdir}")
        # 执行文件传输
        for i in [self.tmp_service_file, self.tmp_server_py]:
            remote_cmd.remote_run(f"rm -rf {i}")
            Cmd.expect_run(
                f"/bin/bash -c '{rsync} {i} {self.user}@{self.ip}:{self.client_rootdir}/'",
                events={'password': f'{self.password}\n'},
            )
        remote_cmd.remote_sudo_run(f"rm -rf /lib/systemd/system/{self.service_name}.service")
        remote_cmd.remote_sudo_run(f"mv {self.client_rootdir}/{self.service_name}.service /lib/systemd/system")
        remote_cmd.remote_sudo_run(f"chmod 644 /lib/systemd/system/{self.service_name}.service")
        remote_cmd.remote_sudo_run(f"systemctl daemon-reload")

    def ensure_pip_and_pipenv_installed(self, remote_cmd):
        _, return_code = remote_cmd.remote_run("pip3 --version", return_code=True)
        if return_code != 0:
            remote_cmd.remote_sudo_run("apt update")
            stdout, return_code = remote_cmd.remote_sudo_run("apt install python3-pip -y", return_code=True)
            if return_code != 0:
                raise EnvironmentError("install python3-pip failed")
            stdout, return_code = remote_cmd.remote_sudo_run(f"pip3 install -U pip -i {config.PYPI_MIRROR}",
                                                             return_code=True)
            if return_code != 0:
                raise EnvironmentError(f"pip failed")

        _, return_code = remote_cmd.remote_run("export PATH=$PATH:$HOME/.local/bin;pipenv --version", return_code=True)
        if return_code != 0:
            _, return_code = remote_cmd.remote_run(
                f"pip3 install pipenv -i {config.PYPI_MIRROR}",
                return_code=True
            )
            if return_code != 0:
                raise EnvironmentError(f"pipenv failed")

    def install_project_dependencies(self):
        remote_cmd = RemoteCmd(self.user, self.ip, self.password)
        self.ensure_pip_and_pipenv_installed(remote_cmd)
        remote_cmd.remote_run(f"rm -rf {self.client_rootdir}/Pipfile")
        stdout, return_code = remote_cmd.remote_run(
            "export PATH=$PATH:$HOME/.local/bin;"
            "export PIPENV_VENV_IN_PROJECT=true;"
            f"cd {self.client_rootdir} && "
            f"pipenv --python 3 && "
            f"pipenv run pip install pylinuxauto -i {config.PYPI_MIRROR}",
            return_code=True
        )
        logger.info(f"环境安装{'成功' if return_code == 0 else '失败'} - < {self.user}@{self.ip} >")

    def restart_client_service(self):
        remote_cmd = RemoteCmd(self.user, self.ip, self.password)
        remote_cmd.remote_sudo_run(f"systemctl restart {self.service_name}.service")
        for i in range(10):
            time.sleep(5)
            stdout, return_code = remote_cmd.remote_run(f"lsof -i:{config.RPC_PORT}", return_code=True)
            if return_code == 0:
                break
        self.check_service_running()

    def gen_service_file(self):
        shutil.copyfile(os.path.join(config.REMOTE_PATH, "server.py"), os.path.expanduser(self.tmp_server_py))
        with open(os.path.join(config.REMOTE_PATH, "tpl.service"), "r", encoding="utf-8") as sf:
            service = sf.read()
        with open(os.path.expanduser(self.tmp_service_file), "w", encoding="utf-8") as sf:
            sf.write(
                service.format(
                    user=self.user,
                    client_rootdir=f"/home/{self.user}/{os.path.basename(self.client_rootdir)}",
                    start_service=f"/home/{self.user}/.local/bin/pipenv run python server.py"
                )
            )

    def check_service_running(self, interrupt: bool = False):
        remote_cmd = RemoteCmd(self.user, self.ip, self.password)
        stdout, return_code = remote_cmd.remote_run(
            f"systemctl status {self.service_name}.service -q > /dev/null",
            return_code=True
        )
        if return_code != 0 and interrupt is True:
            raise RuntimeError("service not running")


def guard_rpc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user")
        ip = kwargs.get("ip")
        password = kwargs.get("password")
        auto_restart = kwargs.get("auto_restart", False)

        service_name = "pylinuxauto_server"
        client_rootdir = "~/pylinuxauto_server"
        tmp_service_file = f"~/{service_name}.service"
        tmp_server_py = "~/server.py"

        if not user or not ip or not password:
            raise ValueError("user, ip and password are required")

        manager = RemotePyLinuxAutoManager(
            user,
            ip,
            password,
            service_name,
            client_rootdir,
            tmp_service_file,
            tmp_server_py
        )
        Cmd.run(f"rm -rf ~/.ssh/known_hosts", command_log=False)
        _, return_code = RemoteCmd(user, ip, password).remote_sudo_run(
            f"systemctl status {service_name}.service -q > /dev/null",
            return_code=True,
            log_cmd=False,
        )
        if return_code != 0:
            manager.gen_service_file()
            manager.transfer_to_client()
            manager.install_project_dependencies()
            manager.restart_client_service()
        else:
            if os.path.exists(tmp_service_file):
                Cmd.run(f"rm -f {tmp_service_file}", command_log=False)
            if os.path.exists(tmp_server_py):
                Cmd.run(f"rm -f {tmp_server_py}", command_log=False)

        if auto_restart:
            manager.restart_client_service()

        res = func(*args, **kwargs)
        return res

    return wrapper
