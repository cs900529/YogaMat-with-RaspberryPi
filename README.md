# YogaMat-with-RaspberryPi
Connect the Raspberry Pi to a yoga mat via USB and communicate with a smartphone using Bluetooth.

## step 1. Install OS

Download and install Raspberry Pi OS (Legacy, 64-bit) FULL using *["Raspberry Pi Imager"](https://www.raspberrypi.com/software/)*.

## step 2. Enable VNC and Download VNC Viewer

Use `$ sudo raspi-config` and select "3 Interface Options" to enable VNC.  
Now you can use VNC Viewer to connect to your Raspberry Pi desktop.

## step 3. Install necessary packages on your Raspberry Pi

```
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install bluetooth libbluetooth-dev -y
$ sudo pip install pybluez
$ sudo apt install snapd
$ sudo snap install usb-reset
```

## step 4. Fix bluetooth.service

```
$ sudo vim /lib/systemd/system/bluetooth.service

fix : ExecStart=/usr/libexec/bluetooth/bluetoothd -E -C

$ sudo sdptool add SP
$ sudo systemctl daemon-reload
$ sudo systemctl restart bluetooth
$ sudo sdptool browse local
$ sudo reboot
```

## step 5. Connect to the Raspberry Pi via Bluetooth on your mobile device.

Remember to click on the Bluetooth icon and select "Make Discoverable."
![discoverable](https://github.com/cs900529/YogaMat-with-RaspberryPi/assets/100250385/ac6aa485-5ef2-4d0f-a980-7216c4423cae)

Pair the Device
![圖片1](https://github.com/cs900529/YogaMat-with-RaspberryPi/assets/100250385/b3e01f92-b46f-4b3e-87e7-3dc56ab2be75)
(This is why VNC is needed instead of directly using SSH for control - Raspberry Pi's Bluetooth connection cannot pair automatically, and this aspect is still being addressed. Or just use mini-HDMI cable)

## step 6. Run  yogaMat.py
Now you can run the yogaMat.py (must use sudo)
`sudo python yogaMat.py`
