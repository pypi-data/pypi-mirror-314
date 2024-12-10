import pylinuxauto
from pylinuxauto import Ele, Ref

close_btn = Ele(xy=(25, 25), ref=Ref.RIGHT_TOP, appname="dde-file-manager", alias="关闭按钮")

pylinuxauto.find_element_by_ref(close_btn).click()
pylinuxauto.find_element_by_ref(close_btn).right_click()

