from pylinuxauto.remote import remote_pylinuxauto

rpl = remote_pylinuxauto(
    user="uos",
    ip="10.8.11.171",
    password="1",
    auto_restart=False
)

# rpl.click_element_by_attr_path("/dde-dock/Btn_文件管理器")

a = rpl.click_element_by_ocr("计算机", "10.8.15.2", {"start_x": 412, "start_y": 169, "w": 1100, "h": 700})
print(a)