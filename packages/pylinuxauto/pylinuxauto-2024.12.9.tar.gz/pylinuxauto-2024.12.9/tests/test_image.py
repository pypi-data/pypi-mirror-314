import pylinuxauto

from pylinuxauto.config import config

config.IMAGE_SERVER_IP = "10.8.15.13"

config.IMAGE_BASE_URL = "http://10.8.15.12/image_res/deepin-music/"


a = pylinuxauto.find_element_by_image("@1.png").result
print(a)


# a = pylinuxauto.find_element_by_image("http://10.8.12.24/image_res/deepin-music/1.png").result
# print(a)
#
#
# a = pylinuxauto.find_element_by_image("~/Desktop/1.png").result
# print(a)
