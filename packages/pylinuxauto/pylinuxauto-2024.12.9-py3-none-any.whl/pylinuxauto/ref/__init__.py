from pylinuxauto.mousekey.mkmixin import MouseKeyChainMixin
from pylinuxauto.ref.base import *

class RefElement(MouseKeyChainMixin):
    
    def find_element_by_ref(self, ele: Ele):
        self.result = RefCenter(appname=ele.appname).ele_center(ref=ele.ref, xy=ele.xy)
        if isinstance(self.result, tuple):
            self.x, self.y = self.result
        return self



def find_element_by_ref(ele: Ele) -> MouseKeyChainMixin:
    return RefElement().find_element_by_ref(ele)
