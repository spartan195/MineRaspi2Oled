# Raspberry Pi 2 Minecraft Server with Waveshare 1.3' Oled display
Setup Minecraft Server on a Raspberry pi 2 with a system monitor + current players info on a Waveshare Oled 1.3' display

## Acknowledgements

I've been trying so many configurations without lick with 1.19 version until I found this tutorial from [James A. Chambers](https://jamesachambers.com/raspberry-pi-minecraft-server-script-with-startup-service/)

With this script you can run your server with jre without headackes. I put my config server files here to help you speed up the optimization process.

Keep in mind this server only runs on Minecraft 1.17.1 , I did not tried on 1.17.2 or 1.18 vut I know for sure 1.19 does not work at all
## Minecraft Server Installation

Clone this repo & cd into it

```bash
  chmod +x SetupMinecraft.sh 
  ./SetupMinecraft.sh
```

- I modified the script to download the 1.17.1 version.
- I used 700mb for the server, you can input this when the script ask for it.
- Type Y or N if you want it to run on startup and restart every night

Now the server will start, you can stop the service with:

```bash
  sudo systemctl stop minecraft
```

Now copy the content of root git folder into minecraft.

- Copy plugins folder into minecraft folder
- Copy Server properties, spigot, bukkit & paper files into minecraft folder

Start the server again with:

```bash
  sudo systemctl start minecraft
```

To check the startup progress execute from repo folder:

```bash
tail -f minecraft/log/latest.log
```
Once it's done you can login from your minecraft client but I would recommend first to execute Chunky to pregenerate chunk before playing

To execute commands in your server:

```bash
  screen -ls 
  # Get the id number
  screen -r $number 
  # Here you can input commands, you can make your player admin with:
  op $PlayerName
  # Now you can execute commands in chat with / 
  # Run Chunky
  Chunky world world
  Chunky worldborder set 2000
  Chunky start
```
To exit screen program I just alt-F4 or close terminal don't Control+C in or you'll stop the server

You can check Chunky progress in the log file


## Waveshare Screen server monitor

I used this [project](https://github.com/pangduckwai/PiDisplay) where I collaborated as a base for this monitor screen

### Prepare raspbian
Install the following packages:
* `sudo apt-get update`
* `sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev`
* `sudo pip3 install --upgrade pip`
* `sudo apt-get purge python3-pip`
* `sudo pip3 install --upgrade luma.oled`
* `sudo pip3 install smbus`
* `sudo apt-get install python3-numpy`
* `sudo apt-get install libopenjp2-7`
* `sudo apt install libtiff5`
* `sudo apt-get install ifstat`

### Enable the SPI interface
* `sudo raspi-config`
* Go to '5 Interfacing Options'
* Go to 'P4 SPI'
* Choose 'Yes'

### Enable the I2C interface
* `sudo raspi-config`
* Go to '5 Interfacing Options'
* Go to 'P5 I2C'
* Choose 'Yes'

### Enable the display at startup
* `sudo vi /etc/rc.local`
  * Add the following line JUST ABOVE exit 0, assuming `mcstatus.py` is in /home/pi/Minecraft-Raspberryi-Pi-2-Oled/:
  * `python /home/pi/Minecraft-Raspberryi-Pi-2-Oled/mcstatus.py &`
  * _**IMPORTANT**_ Don't forget the `&` character at the end!
