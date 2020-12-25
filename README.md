# ActionPi [WIP]

<p align="center">
  <img height="140" src="img/logo.png">
</p>

<p align="center">Action/Dash camera powered by Raspberry Pi Zero </p>

# Features ✨

 - 📽 FullHD video recordings
 - 📥 Download video from WiFi or USB cable
 - 💡 Rolling video appenders: record video in a circular buffer, never overwrite on reboot

# Index
 
 - [Introduction]()
 - [Getting Started]()
    - [Bill of Materials]()
    - [Write SD Card Image]()
    - [Print 3D Case]()
    - [Wrap Up]()
 - [WiFi Setup]()
    - [Hotspot]()
    - [Client]()
 - [Advanced]()
    - [Serial Access]()
 - [F.A.Q.]()
    
## Introduction
ActionPi is a DIY project that I've decided to share.

## Getting Started
Follow the next steps in order to setup a new ActionPi board.

### Bill of Material

 1. 1x RaspberryPi Zero/Zero W
 1. 1x SD Card (at least 4 GB)
 1. 1x RaspberryPi Camera Module
 1. 1x Heatsink (1,5x1,5x0,5)cm
 1. 8x Screw
 1. 1x Nut
 1. 1x 3D-printed case
 
### Write SD Card Image

Althought there is the opportunity to setup an ActionPi starting from a pure Raspbian image I've uploaded an handy prebuild image:
 - [ActionPi-Raspbian](?)

As stated before this is a standard Raspbian image that comes with all the requried ActionPi configurations and could be written following the official Raspberry Pi guide from [here](?).

### Print 3D Case

You'll find all the required STL files on [Thingiverse](?).

## Advanced

### Serial Access

UART0 is enabled on ActionPi prebuilt image and so you can access RPi even with a Serial-to-USB cable (GPIO 14 & 15)

![RPi Zero Pinout](img/rpi_zero_pinout.jpg)

## Photos

This is the prototype I've built:

<p>
  <img height="140" src="img/photo5888543451971171517.jpg"/>
  <img height="140" src="img/photo5888543451971171516.jpg"/>
  <img height="140" src="img/photo5888543451971171515.jpg"/>
</p>

## Do you want to build it on your own and/or contribute?

I'm currently looking for someome interested in build a prototype for personal usage and also help me in the documentation phase of this project.

## ActionPi UI

I'm moving to a newly UI in order to have a more user friendly product. Take a look at [ActionPi-UI](https://github.com/andreacioni/actionpi-ui/) repository for updates.

### Convert h264 video
In order to play the video you have to run: `mp4box -add video.h264:fps=<framerate>  -new video.mp4` 

### Enable WiFi Client
`sudo touch /boot/wifi_client`

### Enable WiFi hotspot
`sudo touch /boot/wifi_hotspot`

### Start Read/Write mode
`sudo touch /boot/rw` or place a jumper between GPIO 21 and GND
