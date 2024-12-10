import pylinuxauto
from pylinuxauto.config import config
from funnylog2 import logger

logger("DEBUG")

config.OCR_SERVER_IP = "10.8.15.2"
import time
start_time = time.time()
a = pylinuxauto.find_element_by_ocr("主目录").result
print(a)
print(time.time() - start_time)