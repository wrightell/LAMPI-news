### Step 1: Burning an SD card
This project uses a [Raspberry Pi 3b+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/). First, we need to install the [OS Image](https://downloads.raspberrypi.com/raspios_oldstable_lite_armhf/images/raspios_oldstable_lite_armhf-2023-05-03/2023-05-03-raspios-buster-armhf-lite.img.xz) Insert the Pi's microSD card into an SD card reader and insert into your comupter. Download and open up the [Raspberry Pi Imager](https://www.raspberrypi.org/software/). For Raspberry Pi Device, select our model, for Operating System, select the OS image we just downloaded, and for storage, select the microSD card you inserted. You don't need to change any settings, just press NEXT and accept any prompts. After installation, mount the card again nad find the `config.txt` file. At the end of the file, in some text editor, add:
```
enable_uart=1
```
Save and close the file. This is so we can access the Pi with USB. Then we need to enable SSH so just add a blank `ssh` file in the `boot` directory.

### Step 2: Getting internet
Now, we need to get the Lampi on our wifi. Using [Serial](https://www.decisivetactics.com/products/serial/), if on Mac like me, we can connect a USB device to the pi to access its terminal. Select the FT230X Basic UART and set Baud Rate: 115200, Data Bits: 8, Parity: None, Stop Bits: 1, select OK. Press enter a couple of times and then you will be prompted to log into the pi. The default username and password are `pi` and `raspberry`. Run `sudo raspi-config` to perform the initial setup. You should chnage the password, set your localization settings, and add a wifi network. After completing you can reboot the pi. Log in again, type `ifconfig` and copy down the `inet addr` in the wlan0 output. This is the ip you can use to ssh into it (ssh pi@<IP>). 

### Step 3: Get python
You should have python, but just in case you can run this to get python3 and pip3:
```
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
```

### Move on to [Setting Up EC2](./Setting%20Up%20EC2)
