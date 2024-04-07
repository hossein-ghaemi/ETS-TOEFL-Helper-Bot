import PIL.Image
from PIL import Image
import pystray

from time import sleep
import subprocess
import os

dir_path = 'images'
connected_img = Image.open(dir_path + '/iconBase.png')  # the "connected" image path


def get_file_content():
    ## retrieves the content of /etc/resolv.conf
    output = subprocess.check_output(['cat', '/etc/resolv.conf']).decode('utf-8')
    return output


def change_img(ico,index):
    print(index)
    # checks if /etc/resolv.conf contains the string ProtonVpn, if true changes the visible icon
    ico.visible = False
    image = Image.open(f"images/Icon{index}.png")
    ico.icon = image
    ico.visible = True
    ico.run()

    # this is used for recursively call the change_img function

def test(ico):
    for x in [1,2,3,4,5]:
        change_img(ico,x)
        sleep(4)

def on_clicked(icon, item):
    # exits the application, this is used to stop the application from within a thread.
    os._exit(0)


exit_menu = pystray.MenuItem('exit vpn checker', on_clicked)

ico = pystray.Icon("vpn connection checker", icon=connected_img,
                   menu=pystray.Menu(exit_menu)
                   )

ico.run(setup=test)
