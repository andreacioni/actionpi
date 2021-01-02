# ActionPi [WIP]

<p align="center">
  <img height="140" src="img/logo.png">
</p>

<p align="center">Action/Dash camera powered by Raspberry Pi Zero </p>

# ✨ Features 

 - 📽 **FullHD** video recordings
 - 📥 **Download video** easily using USB cable or WiFi connection
 - 💡 **Rolling video appenders**: record video in a circular buffer, never overwrite on reboot
 - 🔨 **Robust design**: temperature control, OS read-only partition & low latency write-to-disk (never miss a single frame on power loss)
 - 🕹 **3D Printable case**: it's avaialble on Thingiverse
 
 # 🚧 Working on documentation, please bear with me 🚧

# Index
 
 - [Introduction]()
 - [Getting Started]()
    - [Bill of Materials]()
    - [Write SD Card Image]()
    - [Print 3D Case]()
    - [Put Things Togheter]()
 - [WiFi Setup]()
    - [Hotspot]()
    - [Client]()
 - [Web Interface]()
 - [Advanced]()
    - [Serial Access]()
    - [Postman API]()
 - [Known Issues/Limitations]()
 - [Pinout]()
 - [F.A.Q.]()
    
## Introduction
ActionPi is a DIY project that gives everyone the opportunity to build an action/dash camera with a _20$_ budget.

## Getting Started
Follow the next steps in order to setup a new ActionPi board.

### Bill of Material

 1. 1x RaspberryPi Zero/Zero W
 1. 1x SD Card (at least 8 GB)
 1. 1x RaspberryPi Camera Module + Camera flat connector for RPi Zero.
 1. 1x Heatsink (1,5x1,5x0,5)cm
 1. 8x Screw
 1. 1x Nut
 1. 1x Switch Button
 1. 1x 3D-printed case
 
### Write SD Card Image

Although there is the opportunity to setup an ActionPi starting from a pure Raspbian image I've uploaded an handy prebuilt image:
 - [ActionPi-Raspbian](?)

As stated before this is a standard Raspbian image that comes with all the required ActionPi configurations and could be written following the official Raspberry Pi guide from [here](?).

**Note**: prebuilt image has three partitions already configured and mounted by default in the following directories:

  - `/` (EXT3): this is the read-only partition that contains the Raspbian OS data
  - `boot` (FAT-32): contains the boot files needed to launch Raspbian
  - `/media/recordings` (FAT-32): is the partition where the recordings will be written

last directory point to a partition that **must** be extended in order to contain as much recordings as possible. We will see how to do that in the next sections.

### Print 3D Case

You'll find all the required STL files on [Thingiverse](https://www.thingiverse.com/thing:4703198).

### Put Things Together

Once you have done all the steps before you are ready to assemble everything.

#### First Boot

The first thing to do is plug the micro SD card inside Raspberry Pi Zero and power it. RPi green led will start blinking and after 1-2 minutes you will be able to access it. The best way to access ActionPi is by using the default access point (a.k.a._hotspot_) that it's enabled by default (you can read more on how to access ActionPi shell on [Advanced]() section).

Access Point has name: `ActionPi` and default password is: `actionpi` (of course you could change it).

#### Expand Recordings Partition

Once you connected you'll be able to start an SSH session: `ssh pi@actionpi.local` (default password `raspberry`) and run `?` to expand the 'recordings' partition to fill all the available space left on SD card.

#### Adjust configuration

Almost everything of ActionPi is configurable through `actionpi.cfg` file.

##### Recording Settings

By default **recordings are performed in a circular way** and this means that there well be a fixed number of files, each one with a fixed max length, that will be circularly used to optimize the available space and discard only the less recent video.

For instance this is my setup:

   - Available space in `recordings`: 5 GB
   - Rolling video files number: 9
   - Rolling video files size: 500 MB
   - _Total_: (500 MB) * 9 = 4.5 GB (I left some extra space just to be safe)

This parameters have to be adjusted according to your SD card space and personal needs:

```python
ROTATING_VIDEO_COUNT=9
ROTATING_VIDEO_SIZE=500000000 #Bytes
```

##### Camera Settings
```python
WIDTH=1920
HEIGHT=1080
ROTATION=0 #Valid values are 0, 90, 180, and 270.
FRAMERATE=20
BITRATE=1200000
```


## WiFi Setup
For Raspberry Pi Zero W, WiFi could operate in **Client** or **Hotspot** mode.

> ⚠️ even if you`ll use hotspot or client mode the password **must contains at least 8 characters**.

### Hotspot
Hotspot mode enables ActionPi to act as an Access Point (AP) and allows devices to connect directly to it. In this mode **no Internet connection is available** but you can access the web interface here: `http://192.168.4.1` or `http://actionpi.local`. The AP will spawn with following parameters:

 - **SSID**: _ActionPi_
 - **Password**: _actionpi_ (default)
 
 If you want to switch to _Hotspot_ mode you could enable it from web interface or by running: 
  - `sudo echo "SuperSecretPasswordHere" > /boot/wifi_hotspot` if you want to **change password**, or
  - `touch /boot/wifi_hotspot` if you just want to enable hotspot and **use the old password.**

### Client

> ⚠️ avoid using `sudo raspi-config` to connect to a wireless network.

On _Client_ mode ActionPi will try to connect to a predefined network.

Client mode could enabled from web interface or by running following command: `touch /boot/wifi_hotspot`

>⚠️ **only the first time** or **whenever you have to switch** to different wireless network you have to place an additional file inside `/boot` folder called `wpa_supplicant.conf` that contains Access Point name, password and country code.

*wpa_supplicant.conf*
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="MyNetworkName"
    psk="SuperSecretPassword"
    scan_ssid=1
}
```

You must consider using this method to setup a WiFi connection that requires advanced configuration.

You could read more about **wpa_suppllicant.conf** file [here](?).

>⚠️ currently if Raspberry fails to connect to AP hotspot **will not be activated** as a fallback access point. You could use USB cable connection to access the board and adjust settings.

## Web Interface

[ActionPi-UI](https://github.com/andreacioni/actionpi-ui) is the web interface packed inside ActionPi. With this simple UI built using _React.js_ and _React Material_. It provide some useful actions like: 

  - **Download recordings**
  - **WiFi settings**
  - View **live recording preview**
  - **Monitor** board status

Here some screenshots:

<p>
  <img height="240" src="img/ui/home.png"/>
  <img height="240" src="img/ui/settings.png"/>
  <img height="240" src="img/ui/recordings.png"/>
</p>

## Advanced

### How to access ActionPi system
There are many ways available, by default, to get access to ActionPi through command line interface.

 - **SSH**: Secure Shell is available on every network interface, here below the most common and ready-to-use
    - **USB**: USB Host port expose a network interface that allows to connect ActionPi directly using only a simple USB Micro cable
    - **WiFi**: Either if you are using Hotspot or Client mode
 - **Serial**: UART0 (GPIO 14 & 15) is enabled on ActionPi prebuilt image. In order to access serial port you need a Serial-to-USB cable. Serial _boud rate_ is: `115200`.
 - **HDMI + USB Keyboard**: plug a keyboard and the HDMI cable and you can gain the access to the ActionPi CLI. _Desktop NOT available_

## Photos

This is the prototype I've built:

<p>
  <img height="140" src="img/photo5888543451971171517.jpg"/>
  <img height="140" src="img/photo5888543451971171516.jpg"/>
  <img height="140" src="img/photo5888543451971171515.jpg"/>
</p>

## Do you want to build it on your own and/or contribute?

I'm currently looking for someone interested in build a prototype for personal usage and also help me in the documentation phase of this project.

### Convert h264 video
In order to play the video you have to run: `mp4box -add video.h264:fps=<framerate>  -new video.mp4` 

### Enable WiFi Client
`sudo touch /boot/wifi_client`

### Enable WiFi hotspot
`sudo touch /boot/wifi_hotspot`

### Start Read/Write mode
`sudo touch /boot/rw` or place a jumper between GPIO 21 and GND

## RPi Zero Pinout

![RPi Zero Pinout](img/rpi_zero_pinout.jpg)
