import os
import re

import pytest

from pylinuxauto.config import config


def pytest_addoption(parser):
    parser.addoption("--slaves", action="store", default="", help="")


@pytest.fixture(scope="session")
def slaves(pytestconfig):
    _slaves = pytestconfig.getoption("slaves") or os.getenv("YOUQU_SLAVES")
    if not _slaves:
        raise EnvironmentError("No slaves found, check -s/--slaves value")

    s = []
    for slave in _slaves.split("/"):
        slave_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", slave)
        if slave_info and slave_info[0]:
            user, ip, password = slave_info[0]
            s.append(
                {
                    "user": user,
                    "ip": ip,
                    "password": password or config.PASSWORD,
                }
            )
        else:
            raise ValueError(f"Invalid slave info: {slave}")
    return s


@pytest.fixture(scope="session")
def pylinuxauto():
    import pylinuxauto as pla
    return pla


@pytest.fixture(scope="session")
def sleep():
    from pylinuxauto.sleepx import sleep as slp
    return slp
