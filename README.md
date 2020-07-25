# actionpi [WIP]
Action/Dash camera powered by Raspberry Pi Zero 

## Pinout

![RPi Zero Pinout](img/rpi_zero_pinout.jpg)

### Serial access

UART0 is enabled on Raspbian image and so you can connect to RPi also with a Serial-to-USB cable (GPIO 14 & 15)

### Convert h264 video
In order to play the video you have to run: `mp4box -add video.h264:fps=<framerate>  -new video.mp4` 

### Enable WiFi Client
`sudo touch /boot/wifi_client`

### Enable WiFi hotspot
`sudo touch /boot/wifi_hotspot`

### Start Read/Write mode
`sudo touch /boot/rw` or place a jumper between GPIO 21 and GND
