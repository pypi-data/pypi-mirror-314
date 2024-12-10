import os
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from funnylog2 import logger

from pylinuxauto import exceptions
from pylinuxauto.config import config
from pylinuxauto.ref.wayland_wininfo import WaylandWindowInfo


class Ref(Enum):
    RIGHT_TOP = "right_top"
    RIGHT_BOTTOM = "right_bottom"
    LEFT_TOP = "left_top"
    LEFT_BOTTOM = "left_bottom"


@dataclass
class Ele:
    appname: Optional[str]
    xy: tuple
    ref: Ref
    alias: Optional[str] = None

    def to_dict(self):
        return {
            'appname': self.appname,
            'xy': list(self.xy),
            'ref': self.ref.value,
            'alias': self.alias
        }

    @staticmethod
    def from_dict(d):
        return Ele(
            appname=d['appname'],
            xy=tuple(d['xy']),
            ref=Ref(d['ref']),
            alias=d.get('alias')
        )


class RefCenter:

    def __init__(
            self,
            appname: str,
            number: int = -1,
            pause: int = 1,
            retry: int = 1
    ):

        self.appname = appname
        self.number = number
        self.pause = pause
        self.retry = retry

    def window_info(self):
        if config.IS_X11:
            try:
                app_ids = os.popen(
                    f"xdotool search --classname --onlyvisible {self.appname}"
                ).read().strip().split("\n")
                app_id_list = [int(_id) for _id in app_ids if _id]
                app_id_list.sort()
                app_id = app_id_list[self.number]
                logger.debug(f"{self.appname}:{app_id_list} -> {app_id}")
                return os.popen(
                    f"xwininfo -id {app_id}",
                ).read().strip()
            except IndexError as exc:
                raise exceptions.ApplicationStartError(f"{self.appname, exc}") from exc

        elif config.IS_WAYLAND:
            self.wwininfo = WaylandWindowInfo()
            if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                for _ in range(self.retry + 1):
                    info = self.wwininfo.window_info().get(self.appname)
                    if info is None:
                        time.sleep(1)
                    else:
                        break
                else:
                    raise exceptions.ApplicationStartError(self.appname)

                if isinstance(info, dict):
                    return info
                elif isinstance(info, list):
                    return info[self.number]
                else:
                    raise ValueError
            else:
                raise EnvironmentError("Unsupported platform")
        return None

    def window_location_and_sizes(self):
        app_window_info = self.window_info()
        try:
            if config.IS_X11:
                pattern = r"""
                  Absolute\s+upper-left\s+X:\s+(\d+)\s*
                  .*?
                  Absolute\s+upper-left\s+Y:\s+(\d+)\s*
                  .*?
                  Width:\s+(\d+)\s*
                  .*?
                  Height:\s+(\d+)
                """
                for _ in range(self.retry + 1):

                    match = re.search(pattern, app_window_info, re.VERBOSE | re.DOTALL)

                    if match:
                        window_x = int(match.group(1))
                        window_y = int(match.group(2))
                        window_width = int(match.group(3))
                        window_height = int(match.group(4))
                        break
                    else:
                        time.sleep(1)
                else:
                    raise exceptions.ApplicationStartError(self.appname)
            else:
                window_x, window_y, window_width, window_height = app_window_info.get("location")
            logger.debug(
                f"{self.appname}:窗口左上角坐标 {window_x, window_y},获取窗口大小 {window_width}*{window_height}"
            )
            return (
                int(window_x),
                int(window_y),
                int(window_width),
                int(window_height)
            )
        except (IndexError, KeyError) as exc:
            raise exceptions.GetWindowInformation(f"获取窗口大小错误 {exc}") from exc

    def window_left_bottom_position(self) -> tuple:
        (
            window_x,
            window_y,
            _window_width,
            window_height,
        ) = self.window_location_and_sizes()
        return int(window_x), int(window_y + window_height)

    def window_right_top_position(self) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        return int(window_x + window_width), int(window_y)

    def window_right_bottom_position(self) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        return int(window_x + window_width), int(window_y + window_height)

    def window_left_center_position(self) -> tuple:
        (
            window_x,
            window_y,
            _window_width,
            window_height,
        ) = self.window_location_and_sizes()
        return int(window_x), int(window_y + window_height / 2)

    def window_top_center_position(self) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        return int(window_x + window_width / 2), int(window_y)

    def window_right_center_position(self) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        return int(window_x + window_width), int(window_y + window_height / 2)

    def window_bottom_center_position(self) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        return int(window_x + window_width / 2), int(window_y + window_height)

    def window_center(self) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        return window_x + window_width / 2, window_y + window_height / 2

    def ref_by_left_top(self, button_x, button_y) -> tuple:
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        return window_x + button_x, window_y + button_y

    def ref_by_right_top(self, button_x, button_y) -> tuple:
        window_x, window_y = self.window_right_top_position()
        return window_x - button_x, window_y + button_y

    def ref_by_left_bottom(self, button_x, button_y) -> tuple:
        window_x, window_y = self.window_left_bottom_position()
        return window_x + button_x, window_y - button_y

    def ref_by_right_bottom(self, button_x, button_y) -> tuple:
        window_x, window_y = self.window_right_bottom_position()
        return window_x - button_x, window_y - button_y

    def ele_center(self, ref: Ref, xy: Tuple[int, int]):
        time.sleep(self.pause)
        return getattr(self, f"ref_by_{ref.value}")(*xy)
