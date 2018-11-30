# -*- encoding=utf8 -*-
__author__ = "ake"


from airtest.core.api import *
import os

auto_setup(__file__)

package_name = "com.netease.poco.u3d.tutorial"

if package_name not in device().list_app():
    print("应用没有安装，请先安装应用" + package_name)
    
stop_app(package_name)
wake()
start_app(package_name)
sleep(2)    

touch(Template(r"tpl1539238558313.png", record_pos=(0.002, -0.08), resolution=(1280, 720)))

touch(Template(r"tpl1539238573262.png", record_pos=(-0.345, -0.087), resolution=(1280, 720)))


from poco.drivers.unity3d import UnityPoco
poco = UnityPoco()

# poco('btn_start').click()
# #time.sleep(1)
# poco("drag_and_drop").click()
# #time.sleep(1)

star_pos = [] #获取名个星星的坐标
shell = poco("shell")

for star in poco('star'):
    star_pos.append(star.get_position())
    star.drag_to(shell)
time.sleep(1)
print(star_pos)


assert poco('scoreVal').get_text() == "100", "score correct."
# poco('btn_back', type='Button').click()
# poco("drag_and_drop").click()
touch(Template(r"tpl1539238611022.png", record_pos=(-0.417, 0.203), resolution=(1280, 720)))
touch(Template(r"tpl1539238623055.png", record_pos=(-0.345, -0.085), resolution=(1280, 720)))

#星星还原效果
i=0
for star in poco('star'):
    star.drag_to(star_pos[i])
    i=i+1

time.sleep(1)
log("Test OK")

sleep(2)
stop_app(package_name)
