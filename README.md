# Micro Flipper
My Flipper Zero SD Card Tools & Layout

# DISCLAIMER
## This repository is not affiliated with Flipper Devices Inc., and is for educational purposes only.
## The developer is not responsible for any damage you cause to your devices.
## Please read everything carefully.

---

## Getting Started
Format your micro sd card as FAT32 and label it `FLIPPER`; this will make it easier to find in your file manager. After formatting, insert the card into your Flipper Zero and power it on.

We will be using the [Unleashed](https://github.com/DarkFlippers/unleashed-firmware) firmware for this project.

Plug your Flipper Zero into your computer and open the [releases](https://github.com/DarkFlippers/unleashed-firmware/releases/tag/unlshd-054) page. Next `ctrl + f` "Install via Web Updater". Click the link and follow the instructions to install the firmware. **Note**, *Firefox will not work for this, you must use Chrome or Chromium.*

At this point you can confirm the prompts and turn off the Flipper Zero; if you are highspeed you can also unmount it via the settings menu. Remove the micro sd card and plug it into your computer.

Next `cd` into the root directory of the micro sd card and run:

```bash
curl -s https://raw.githubusercontent.com/christopherwoodall/micro-flipper/main/tools/installer.sh | bash
```

If you are using **WSL** you may need to run the following command to mount the sd card:
```bash
sudo mount -t drvfs 'F:' /mnt/f
```

---

## Resources

- https://github.com/djsime1/awesome-flipperzero
- https://github.com/RogueMaster/flipperzero-firmware-wPlugins
- https://github.com/logickworkshop/Flipper-IRDB
- https://github.com/evilpete/flipper_toolbox
- https://github.com/I-Am-Jakoby/Flipper-Zero-BadUSB
- https://github.com/FalsePhilosopher/badusb

---
