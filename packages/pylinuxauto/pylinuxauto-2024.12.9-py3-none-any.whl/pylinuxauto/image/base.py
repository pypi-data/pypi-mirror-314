#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License
import os
import time
from typing import List, Union
from urllib.parse import urljoin
from xmlrpc.client import Binary
from xmlrpc.client import ServerProxy

from funnylog2 import logger
from nocmd import Cmd

try:
    import cv2 as cv
    import numpy as np

    GET_IMAGE_FORM_RPC = False
except ModuleNotFoundError:
    GET_IMAGE_FORM_RPC = True

from pylinuxauto import exceptions
from pylinuxauto.config import config
from pylinuxauto.screenshot import screenshot_full
from pylinuxauto.screenshot import screenshot_area


class ImageBase:

    @classmethod
    def server_url(cls):
        return f"http://{config.IMAGE_SERVER_IP}:{config.IMAGE_PORT}"

    @classmethod
    def server(cls):
        return ServerProxy(cls.server_url(), allow_none=True)

    @classmethod
    def check_connected(cls):
        try:
            return cls.server().check_connected()
        except OSError:
            return False

    @classmethod
    def _match_image_by_opencv(
            cls,
            image_path: str,
            rate: float = None,
            multiple: bool = False,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            network_retry: int = 1,
            log_level: str = "info",
    ):
        """
         图像识别，匹配小图在屏幕中的坐标 x, y，当前仅支持1个主屏幕，如果存在多个屏幕只会截取主屏幕内容。
        :param image_path: 图像识别目标文件的存放路径,仅支持英文文件名，不支持中文文件名
        :param rate: 匹配度
        :param multiple: 是否返回匹配到的多个目标
        :param picture_abspath: 大图，默认大图是截取屏幕，否则使用传入的图片；
        :param screen_bbox: 截取屏幕上指定区域图片（仅支持X11下使用）；
            [x, y, w, h]
            x: 左上角横坐标；y: 左上角纵坐标；w: 宽度；h: 高度；根据匹配度返回坐标
        :param network_retry: 连接服务器重试次数
        """
        if rate is None:
            rate = float(config.IMAGE_RATE)

        if picture_abspath is None:
            if screen_bbox:
                screen_path = screenshot_area(*screen_bbox)
            else:
                screen_path = screenshot_full()
        else:
            screen_path = picture_abspath
        template_path = ""
        if image_path.startswith("@"):
            if not config.IMAGE_BASE_URL.endswith("/"):
                raise ValueError("config.IMAGE_BASE_URL must end with '/'")
            image_url = urljoin(config.IMAGE_BASE_URL, image_path.lstrip("@"))
            template_path = cls.download_image(image_url)
        elif image_path.startswith("http"):
            image_url = image_path
            template_path = cls.download_image(image_url)
        else:
            image_path = os.path.expanduser(image_path)
            # 如果传入的image_path参数不带文件后缀名，就根据文件类型判断文件是否存在，存在则将后缀类型（'.png','.jpg','.jpeg'）加上
            if not image_path.endswith(('.png', '.jpg', '.jpeg')):
                if os.path.exists(f"{image_path}.png"):
                    template_path = f"{image_path}.png"
                elif os.path.exists(f"{image_path}.jpg"):
                    template_path = f"{image_path}.jpg"
                elif os.path.exists(f"{image_path}.jpeg"):
                    template_path = f"{image_path}.jpeg"
                else:
                    logger.error(f"The image format is not supported. Please confirm your image_path again")
            else:
                # image_path参数带有后缀名，不做任何添加
                template_path = image_path
            if not template_path:
                raise ValueError
        if GET_IMAGE_FORM_RPC:
            screen_rb = open(screen_path, "rb")
            template_rb = open(template_path, "rb")
            for _ in range(network_retry + 1):
                try:
                    screen_path = cls.server().image_put(Binary(screen_rb.read()))
                    screen_rb.close()
                    tpl_path = cls.server().image_put(Binary(template_rb.read()))
                    template_rb.close()
                    logger.info(f"IMAGE SERVER http://{config.IMAGE_SERVER_IP}")
                    res =  cls.server().match_image_by_opencv(
                        tpl_path, screen_path, rate, multiple
                    )
                    if res and screen_bbox:
                        res = [res[0] + screen_bbox[0], res[1] + screen_bbox[1]]
                    return res
                except OSError:
                    continue
            raise EnvironmentError(
                f"IMAGE_SERVER访问失败 {cls.server_url()}"
            )
        else:
            from pylinuxauto.image.server import match_image_by_opencv
            return match_image_by_opencv(template_path, screen_path, rate, multiple)

    @classmethod
    def download_image(cls, image_url):
        image_name = image_url.split("/")[-1]
        template_path = f"/tmp/{image_name}"
        Cmd.run(
            f"rm -rf {template_path}",
            print_log=False,
            command_log=False
        )
        stdout, status_code = Cmd.run(
            f'curl -s -o {template_path} {image_url} -w “%{{http_code}}”',
            return_code=True,
            print_log=False,
        )
        if stdout != '“200”':
            raise RuntimeError(f"Download Error: {image_url}")
        return template_path

    @classmethod
    def find_element(
            cls,
            *eles,
            rate: Union[float, int] = None,
            multiple: bool = False,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None,
            **kwargs,
    ):
        """
         在屏幕中区寻找小图，返回坐标，
         如果找不到，根据配置重试次数，每次间隔1秒
        :param picture_abspath:
        :param eles: 模板图片路径
        :param rate: 相似度
        :param multiple: 是否返回匹配到的多个目标
        :param screen_bbox: 截取屏幕上指定区域图片（仅支持X11下使用）；
            [x, y, w, h]
            x: 左上角横坐标；y: 左上角纵坐标；w: 宽度；h: 高度；根据匹配度返回坐标
        :param log_level: 日志级别
        :param network_retry: 连接服务器重试次数
        :param pause: 图像识别重试的间隔时间
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :return: 坐标元组
        """
        network_retry = network_retry if network_retry else config.IMAGE_NETWORK_RETRY
        pause = pause if pause else config.IMAGE_PAUSE
        timeout = timeout if timeout else config.IMAGE_TIMEOUT
        max_match_number = max_match_number if max_match_number else config.IMAGE_MAX_MATCH_NUMBER

        retry_number = int(max_match_number)
        if retry_number < 0:
            raise ValueError("重试次数不能小于0")

        if rate is None:
            rate = float(config.IMAGE_RATE)
        try:
            for element in eles:
                start_time = time.time()
                for _ in range(retry_number + 1):
                    locate = cls._match_image_by_opencv(
                        element,
                        rate,
                        multiple=multiple,
                        picture_abspath=picture_abspath,
                        screen_bbox=screen_bbox,
                        network_retry=network_retry,
                    )
                    if not locate:
                        time.sleep(int(pause))
                    else:
                        return locate
                    end_time = time.time()
                    if end_time - start_time > timeout:
                        break
            raise exceptions.TemplateElementNotFound(*eles)
        except Exception as exc:
            raise exc

    @classmethod
    def get_during(
            cls,
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
        during_path = "/tmp/youqu_during"
        os.system(f"rm -rf {during_path}")
        os.makedirs(during_path)
        pics = []
        start_time = time.time()
        for i in range(max_range):
            pic_name = f"{during_path}/{time.time()}_{i}.png"
            pics.append(pic_name)
            if PYSCREENSHOT:
                try:
                    pyscreenshot.grab().save(pic_name)
                except easyprocess.EasyProcessError:
                    ...
            else:
                fullscreen_path = os.popen(cls.screenshot_fullscreen_dbus()).read().strip().strip("\n")
                os.system(f"cp -r {fullscreen_path} {pic_name}")
            if time.time() - start_time >= screen_time:
                break
            if pause:
                time.sleep(pause)
        if not pics:
            raise ValueError
        for pic_path in pics:
            res = cls._match_image_by_opencv(
                image_path, rate=rate, picture_abspath=pic_path
            )
            if res:
                return res
        raise exceptions.TemplateElementNotFound(image_path)
