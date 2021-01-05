# IMSA-3D-Printer-Management
Remote management and control of IMSA's 3D printers via OctoPrint and a webservice

There are two parts of this system: the server pi (only 1) and the printer pi's (1 pi per printer)

Server Pi:

* NOOBS (or any other Operating System like Raspbian) - NOOBS: https://www.raspberrypi.org/downloads/noobs/
  - Download the zip for the NOOBS 3.5.0 OS (not NOOBS Lite) from the link above
  - Format a micro SD card ( at least 16GB) with FAT32 and empty memory
  - Extract NOOBS's zipped folder to a micro SD card (tutorial: https://thepi.io/how-to-install-noobs-on-the-raspberry-pi/)
  - Using an HDMI cable and adapter to project the pi to a monitor, boot it up and select Raspbian/Raspberry Pi Operating System
  - Set up WiFi
* Connect Server Pi to WiFi network (Can be done with a monitor, keyboard, and mouse)
* On the Pi's Desktop, select the upper left button->Preferences->Raspberry Pi Configuration->Interfaces
  - Find the "SSH" option and set it to enabled
* Install Node.js (tutorial: https://blog.xuan-nguyen.vn/install-node-js-and-npm-on-raspberry-pi/)
  - Use CygWin64 on Windows or terminal with Mac/Linux
  - run "ssh pi@ip_address"
  - Enter Server Pi Password
* Install Node'js packages: express, body-parser, ejs (e.g. npm install express/body-parser/ejs [run in the folder /home/pi/statusPage])
* Copy all files in server folder (index.ejs, index.js, openPage.sh) to /home/pi/statusPage
* Create a crontab (crontab -a) and paste this line: "@reboot /home/pi/statusPage/openPage.sh"
* 
Printer Pi:

* Install OctoPrint OS on each pi that you intend to connect to a printer (https://octoprint.org/download/) Download a stable version
* Follow this tutorial to install OctoPrint on a micro SD card: https://www.youtube.com/watch?v=mnN4HVmjafs (watch up to 3:51)
  - This includes setting up WiFi information on the OS and region information (UK/France/U.S/etc)
    - Set up the WiFi network on the same network as the Server Pi
* Copy everything in the printer folder (config, findPrinterStatus.py) to "/home/pi/.octoprint/plugins" on the printer pi (make sure you update the server pi's ip in: /home/pi/.octoprint/plugins/config/configuration.json)
