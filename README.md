# IMSA-3D-Printer-Management
Remote management and control of IMSA's 3D printers via OctoPrint and a webservice

There are two parts of this system: the server pi (only 1) and the printer pi's (1 pi per printer)
Server Pi:

* NOOBS (or any other Operating System like Raspbian) - NOOBS: https://www.raspberrypi.org/downloads/noobs/
  - Download the zip for the NOOBS 3.5.0 OS (not NOOBS Lite) from the link above
  - Format a micro SD card (~8GB) with FAT32 and empty memory
  - Copy NOOBS's zipped folder to micro SD card
* Connect Server Pi to WiFi network
* Install Node.js (tutorial: https://blog.xuan-nguyen.vn/install-node-js-and-npm-on-raspberry-pi/)
* Install Node'js packages: express, body-parser, ejs (e.g. npm install express/body-parser/ejs [run in the folder /home/pi/statusPage])
* Copy all files in server folder (index.ejs, index.js, openPage.sh) to /home/pi/statusPage
* Create a crontab (crontab -a) and paste this line: "@reboot /home/pi/statusPage/openPage.sh"
* 
Printer Pi:

* Install OctoPrint OS on each pi that you intend to connect to a printer (https://octoprint.org/download/) Download a stable version
* Follow this tutorial to install OctoPrint on a micro SD card: https://www.youtube.com/watch?v=mnN4HVmjafs (watch up to 3:51)
  - This includes setting up WiFi information on the OS and region information (UK/France/U.S/etc)
* 
