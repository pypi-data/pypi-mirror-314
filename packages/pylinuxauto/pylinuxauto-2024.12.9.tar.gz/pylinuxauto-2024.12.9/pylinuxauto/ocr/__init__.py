#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License
import random
import copy
from typing import List

try:
    from paddleocr import PaddleOCR

    GET_OCR_FORM_RPC = False
except ModuleNotFoundError:
    GET_OCR_FORM_RPC = True

from pylinuxauto.mousekey.mkmixin import MouseKeyChainMixin
from pylinuxauto.config import config
from pylinuxauto.ocr.base import OCRBase


class OCR(MouseKeyChainMixin):

    def _ocr_servers(self, server_str: str) -> List[str]:
        return [i.strip() for i in server_str.split("/") if i]

    def find_element_by_ocr(
            self,
            *target_strings,
            picture_abspath: str = None,
            similarity: [int, float] = 0.6,
            return_default: bool = False,
            return_first: bool = False,
            lang: str = "ch",
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None,
            bbox: dict = None,
            ocr_server_ips: str = None,
    ):
        if GET_OCR_FORM_RPC:
            if ocr_server_ips is None:
                servers = self._ocr_servers(config.OCR_SERVER_IP)
            else:
                servers = self._ocr_servers(ocr_server_ips)
            self.target_strings = target_strings
            log_server = copy.deepcopy(servers)
            while servers:
                config.OCR_SERVER_IP = random.choice(servers)
                if OCRBase.check_connected() is False:
                    servers.remove(config.OCR_SERVER_IP)
                    config.OCR_SERVER_IP = None
                else:
                    break
            if config.OCR_SERVER_IP is None:
                raise EnvironmentError(f"所有OCR服务器不可用: {log_server}")

        self.result = OCRBase.ocr(
            *target_strings,
            picture_abspath=picture_abspath,
            similarity=similarity,
            return_default=return_default,
            return_first=return_first,
            lang=lang,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
            bbox=bbox,
        )

        if isinstance(self.result, tuple):
            self.x, self.y = self.result

        return self


def find_element_by_ocr(
        *target_strings,
        picture_abspath: str = None,
        similarity: [int, float] = 0.6,
        return_default: bool = False,
        return_first: bool = False,
        lang: str = "ch",
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        max_match_number: int = None,
        bbox: dict = None,
        ocr_server_ips: str = None,
) -> MouseKeyChainMixin:
    return OCR().find_element_by_ocr(
        *target_strings,
        picture_abspath=picture_abspath,
        similarity=similarity,
        return_default=return_default,
        return_first=return_first,
        lang=lang,
        network_retry=network_retry,
        pause=pause,
        timeout=timeout,
        max_match_number=max_match_number,
        bbox=bbox,
        ocr_server_ips=ocr_server_ips
    )