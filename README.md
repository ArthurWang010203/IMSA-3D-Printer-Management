# IMSA-3D-Printer-Management
Remote management and control of IMSA's 3D printers via OctoPrint and a webservice

There are two parts of this system: the server pi (only 1) and the printer pi's (1 pi per printer)
Server Pi:

* NOOBS (or any other Operating System like Raspbian) - NOOBS: https://www.raspberrypi.org/downloads/noobs/
* Connect Server Pi to WiFi network
* Install Node.js (tutorial: https://blog.xuan-nguyen.vn/install-node-js-and-npm-on-raspberry-pi/)
* Install Node'js packages: express, body-parser, ejs (e.g. npm install express/body-parser/ejs [run in the folder /home/pi/statusPage])
* Copy both files in server folder (index.ejs and index.js) to /home/pi/statusPage
* Create a crontab (crontab -a) and paste this line: "@reboot /home/pi/statusPage/openPage.sh"
* 
Printer Pi:
