import subprocess
import time
import PIL.Image
import pystray, ping3


class etsIcon:
    icon = None
    image_path = "images/IconBase.png"
    image = PIL.Image.open(image_path)

    @staticmethod
    def create(image):
        etsIcon.icon = pystray.Icon("Nvidia Geforce", image,
                            menu=pystray.Menu(pystray.MenuItem("Exit", lambda icon, item: etsIcon.icon.stop())))
        etsIcon.icon.run(setup=image)

    @staticmethod
    def update_icon(flag=False, answer=''):
        # if answer == 'a':
        #     etsIcon.image_path = "images/Icon1.png"
        # if answer == 'b':
        #     etsIcon.image_path = "images/Icon2.png"
        # if answer == 'c':
        #     etsIcon.image_path = "images/Icon3.png"
        # if answer == 'd':
        #     etsIcon.image_path = "images/Icon4.png"

        for x in [1, 2, 3, 4]:
            print(f"images/Icon{x}.png")
            time.sleep(5)
            etsIcon.icon = f"images/Icon{x}.png"
            etsIcon.icon.run()

    def change_img(answer=''):
        # checks if /etc/resolv.conf contains the string ProtonVpn, if true changes the visible icon
        for x in [1, 2, 3, 4]:
            etsIcon.visible = False
            image = PIL.Image.open(f"images/Icon{x}.png")
            # etsIcon.icon = (connected_img if answer='' else disconnected_img)
            etsIcon.icon = image
            etsIcon.visible = True
            etsIcon.create(image)
            time.sleep(5)  # interval between checks if connected to vpn

    @staticmethod
    def on_clicked(icon, item):
        print("hello world")

    @staticmethod
    # def run():
    #     etsIcon.icon.run(setup=etsIcon.image_path)

    @staticmethod
    def stop():
        etsIcon.icon.stop()


if __name__ == "__main__":
    # Create an instance of etsIcon
    icon_instance = etsIcon()

    # Create a new Python process for etsIcon
    process = subprocess.Popen(["python", "icon.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # Give some time for the new process to initialize
    time.sleep(2)

    # Call the create method in the new process
    icon_instance.create(etsIcon.image)

    # Wait for the process to finish
    process.wait()
