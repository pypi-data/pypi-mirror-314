import logging
import os

from nocmd import Cmd

from pylinuxauto.config import config


def _screenshot_cmd():
    return "dbus-send --session --print-reply=literal --dest=org.kde.KWin /Screenshot org.kde.kwin.Screenshot"


def insert_path():
    os.environ['XDG_RUNTIME_DIR'] = f'/run/user/{os.getuid()}'
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = f"unix:path={os.environ['XDG_RUNTIME_DIR']}/bus"


def install_pyscreenshot():
    _, exitcode = Cmd.run(
        "pip3 show pyscreenshot",
        return_code=True,
        command_log=False,
        print_log=False
    )
    if exitcode == 0:
        return
    os.system(f"pip3 install pyscreenshot -i {config.PYPI_MIRROR}")
    if config.SYS_ARCH in ["x86_64", "aarch64"]:
        os.system(f"pip3 install pillow -i {config.PYPI_MIRROR}")
    else:
        Cmd.sudo_run("apt install python3-pil -y")


def screenshot_full():
    insert_path()
    fullscreen_path, exitcode = Cmd.run(
        f"{_screenshot_cmd()}.screenshotFullscreen",
        return_code=True,
        command_log=False,
        print_log=False
    )
    if exitcode != 0:
        install_pyscreenshot()
        import pyscreenshot
        import easyprocess
        from pyscreenshot.loader import log
        from pylinuxauto.utils import TempLogLevel
        fullscreen_path = config.SCREEN_CACHE
        with TempLogLevel(log, logging.INFO):
            try:
                pyscreenshot.grab().save(os.path.expanduser(fullscreen_path))
            except easyprocess.EasyProcessError:
                ...
    return fullscreen_path.strip().strip("\n")


def screenshot_area(x, y, w, h):
    insert_path()
    screen_path, exitcode = Cmd.run(
        f"{_screenshot_cmd()}.screenshotArea int32:{x} int32:{y} int32:{w} int32:{h}",
        return_code=True,
        command_log=False,
        print_log=False
    )
    if exitcode != 0:
        install_pyscreenshot()
        import pyscreenshot
        import easyprocess
        from pyscreenshot.loader import log
        screen_path = config.SCREEN_CACHE
        with TempLogLevel(log, logging.INFO):
            try:
                pyscreenshot.grab(bbox=(x, y, x + w, h + y)).save(os.path.expanduser(screen_path))
            except easyprocess.EasyProcessError:
                ...
    return screen_path.strip().strip("\n")


if __name__ == '__main__':
    print(screenshot_full())
