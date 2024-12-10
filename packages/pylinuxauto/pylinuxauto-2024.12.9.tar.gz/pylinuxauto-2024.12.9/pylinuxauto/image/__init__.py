#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License
import copy
import random
from typing import List, Union

try:
    import cv2 as cv
    import numpy as np

    GET_IMAGE_FORM_RPC = False
except ModuleNotFoundError:
    GET_IMAGE_FORM_RPC = True

from pylinuxauto.config import config
from pylinuxauto.image.base import ImageBase
from pylinuxauto.mousekey.mkmixin import MouseKeyChainMixin


class Image(MouseKeyChainMixin):

    def _image_servers(self, server_str: str) -> List[str]:
        return [i.strip() for i in server_str.split("/") if i]

    def find_element_by_image(self, *args, **kwargs):
        if GET_IMAGE_FORM_RPC:
            image_server_ips = kwargs.get("image_server_ips")
            if image_server_ips is None:
                servers = self._image_servers(config.IMAGE_SERVER_IP)
            else:
                servers = self._image_servers(image_server_ips)
            log_server = copy.deepcopy(servers)
            while servers:
                config.IMAGE_SERVER_IP = random.choice(servers)
                if ImageBase.check_connected() is False:
                    servers.remove(config.IMAGE_SERVER_IP)
                    config.IMAGE_SERVER_IP = None
                else:
                    break
            if config.IMAGE_SERVER_IP is None:
                raise EnvironmentError(f"所有IMAGE服务器不可用: {log_server}")

        self.result = ImageBase.find_element(*args, **kwargs)
        if isinstance(self.result, list):
            self.x, self.y = self.result

        return self

def find_element_by_image(
        *images,
        rate: Union[float, int] = None,
        multiple: bool = False,
        picture_abspath: str = None,
        screen_bbox: List[int] = None,
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        max_match_number: int = None,
        image_server_ips: str = None
) -> MouseKeyChainMixin:
    return Image().find_element_by_image(
        *images,
        rate=rate,
        multiple=multiple,
        picture_abspath=picture_abspath,
        screen_bbox=screen_bbox,
        network_retry=network_retry,
        pause=pause,
        timeout=timeout,
        max_match_number=max_match_number,
        image_server_ips=image_server_ips,
    )


def get_during(
        image_path: str,
        screen_time: Union[float, int],
        rate: float = None,
        pause: Union[int, float] = None,
        max_range: int = 10000,
):
    """
    在一段时间内截图多张图片进行识别，其中有一张图片识别成功即返回结果;
    适用于气泡类的断言，比如气泡在1秒内消失，如果用常规的图像识别则有可能无法识别到；
    :param image_path: 要识别的模板图片；
    :param screen_time: 截取屏幕图片的时间，单位秒；
    :param rate: 识别率；
    :param pause: 截取屏幕图片的间隔时间，默认不间隔；
    """
    return ImageBase().get_during(
        image_path=image_path,
        screen_time=screen_time,
        rate=rate,
        pause=pause,
        max_range=max_range
    )