import pylinuxauto
from typing import List, Union


class Methods:

    # attr
    def click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).click()

    def double_click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).double_click()

    def right_click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).right_click()

    def element_center_by_attr_path(self, attr_path):
        return pylinuxauto.find_element_by_attr_path(attr_path).center()

    # image
    def click_element_by_image(self, image_path: str, image_server_ips: str, screen_bbox: List[int] = None, rate: Union[float, int] = None):
        pylinuxauto.find_element_by_image(image_path, image_server_ips=image_server_ips, screen_bbox=screen_bbox, rate=rate).click()

    def double_click_element_by_image(self, image_path: str, image_server_ips: str, screen_bbox: List[int] = None, rate: Union[float, int] = None):
        pylinuxauto.find_element_by_image(image_path, image_server_ips=image_server_ips, screen_bbox=screen_bbox, rate=rate).double_click()

    def right_click_element_by_image(self, image_path: str, image_server_ips: str, screen_bbox: List[int] = None, rate: Union[float, int] = None):
        pylinuxauto.find_element_by_image(image_path, image_server_ips=image_server_ips, screen_bbox=screen_bbox, rate=rate).right_click()

    def element_center_by_image(self, image_path: str, image_server_ips: str, screen_bbox: List[int] = None, rate: Union[float, int] = None):
        return pylinuxauto.find_element_by_image(image_path, image_server_ips=image_server_ips, screen_bbox=screen_bbox, rate=rate).center()

    # ocr
    def click_element_by_ocr(self, target, ocr_server_ips: str, bbox: dict = None):
        pylinuxauto.find_element_by_ocr(target, ocr_server_ips=ocr_server_ips, bbox=bbox).click()

    def double_click_element_by_ocr(self, target, ocr_server_ips: str, bbox: dict = None):
        pylinuxauto.find_element_by_ocr(target, ocr_server_ips=ocr_server_ips, bbox=bbox).double_click()

    def right_click_element_by_ocr(self, target, ocr_server_ips: str, bbox: dict = None):
        pylinuxauto.find_element_by_ocr(target, ocr_server_ips=ocr_server_ips, bbox=bbox).right_click()

    def element_center_by_ocr(self, target, ocr_server_ips: str, bbox: dict = None):
        return pylinuxauto.find_element_by_ocr(target, ocr_server_ips=ocr_server_ips, bbox=bbox).center()

    def element_result_by_ocr(self, target, ocr_server_ips: str, bbox: dict = None):
        return pylinuxauto.find_element_by_ocr(target, ocr_server_ips=ocr_server_ips, bbox=bbox).result

    # ui
    def click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).click()

    def double_click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).double_click()

    def right_click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).right_click()

    # new ui
    def click_element_by_ref(self, ele_dict):
        pylinuxauto.find_element_by_ref(ele=pylinuxauto.Ele.from_dict(ele_dict)).click()

    def double_click_element_by_ref(self, ele_dict):
        pylinuxauto.find_element_by_ref(ele=pylinuxauto.Ele.from_dict(ele_dict)).double_click()

    def right_click_element_by_ref(self, ele_dict):
        pylinuxauto.find_element_by_ref(ele=pylinuxauto.Ele.from_dict(ele_dict)).right_click()

    # mousekey
    def click(self, x=None, y=None):
        pylinuxauto.click(_x=x, _y=y)

    def double_click(self, x=None, y=None):
        pylinuxauto.double_click(_x=x, _y=y)

    def right_click(self, x=None, y=None):
        pylinuxauto.right_click(_x=x, _y=y)

    def move_to(self, x=None, y=None):
        pylinuxauto.move_to(_x=x, _y=y)

    def input(self, text: str):
        pylinuxauto.input(text)

    def hotkey(self, *key):
        pylinuxauto.hot_key(*key)
