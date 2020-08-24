# ActionPi [WIP]

<p align="center">
  <img height="140" src="img/logo.png">
</p>

<p align="center">Action/Dash camera powered by Raspberry Pi Zero </p>

## Photos

This is the prototype I've built:

<p>
  <img height="140" src="img/photo5888543451971171517.jpg"/>
  <img height="140" src="img/photo5888543451971171516.jpg"/>
  <img height="140" src="img/photo5888543451971171515.jpg"/>
</p>

## Want build it your own and/or contribute?

I'm currently looking to someome interested in build a prototype for personal usage and also help me in the documentation phase of this project.

## ActionPi UI

There is also another (private) repository that olds the source code of a ReactJS webapp that should control the camera (it will replace the ugly UI proposed in this repo). If you are interested in contribute to it let me know!

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
