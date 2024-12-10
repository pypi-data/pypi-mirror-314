import os

os.environ["DISPLAY"] = ":0"
from pylinuxauto.mousekey import *
from pylinuxauto.screenshot import screenshot_full
from pylinuxauto.screenshot import screenshot_area
from pylinuxauto.file import File
from pylinuxauto.sleepx import sleep
from pylinuxauto.ref.base import Ref
from pylinuxauto.ref.base import Ele
from pylinuxauto.ref import find_element_by_ref
from pylinuxauto.ui import find_element_by_ui
from pylinuxauto.ocr import find_element_by_ocr
from pylinuxauto.image import find_element_by_image
from pylinuxauto.image import get_during
from pylinuxauto.attr import find_element_by_attr_path
from pylinuxauto.attr import find_elements_to_the_end_by_attr
from pylinuxauto.attr import find_element_by_attr_name
from pylinuxauto.attr import find_element_children_by_attr
from pylinuxauto.attr import is_child_find_element_by_attr
from pylinuxauto.remote import remote_pylinuxauto
