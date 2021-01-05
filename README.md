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
* Install Node.js (Follow instructions below)
  - Use CygWin64 on Windows or terminal with Mac/Linux
  - run "ssh pi@ip_address"
  - Enter Server Pi Password
* Run the following commands in the home directory of the pi ("cd ~/")
  - curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
  - sudo apt-get install nodejs
  - curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
  - echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
  - sudo apt-get update && sudo apt-get install yarn
* Run "npm -v" to check if npm is installed (the version of npm will appear)
* Make a folder on the home directory called "statusPage" ("mkdir statusPage") and enter it ("cd ~/statusPage")
* Run "npm init" and set the main file to "index.js"
  - Continue until it says "Is this OK? (yes)" (You can also add a description)
  - The preview for what is about to write should say "main":"index.js"
* Run the following commands for the Node.js packages: 
  - npm install express
  - npm install body-parser
  - npm install ejs
* Go to the home directory ("cd ~/") and run "node" to check that it is working
  - If you get an error (i.e. /usr/local/bin/node: No such file or directory), run the following commands
    - sudo apt full-upgrade -y
    - curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -
    - sudo apt-get install -y nodejs
    - sudo ln -s /usr/bin/nodejs /usr/local/bin/node
* Copy all files in server folder (index.ejs, index.js, openPage.sh) to /home/pi/statusPage
  - Download the files to a computer, (Cygwin if Windows, terminal if Mac/Linux) cd to the directory they are stored in (i.e. "cd C:/Users/"), and run the following
  - scp index.ejs pi@ip_address:/home/pi/statusPage/
  - scp index.js pi@ip_address:/home/pi/statusPage/
  - scp openPage.sh pi@ip_address:/home/pi/statusPage/
* Create a crontab (crontab -e, then pick an editor (/bin/nano)) and paste this line: "@reboot /home/pi/statusPage/openPage.sh"
  - Ctrl+O and Enter to save, Ctrl+X to exit
* Run "sudo reboot"
Printer Pi:

* Install OctoPrint OS on each pi that you intend to connect to a printer (https://octoprint.org/download/) Download a stable version
* Follow this tutorial to install OctoPrint on a micro SD card: https://www.youtube.com/watch?v=mnN4HVmjafs (watch up to 3:51)
  - This includes setting up WiFi information on the OS and region information (UK/France/U.S/etc)
    - Set up the WiFi network on the same network as the Server Pi
* Copy everything in the printer folder (config, findPrinterStatus.py) to "/home/pi/.octoprint/plugins" on the printer pi (make sure you update the server pi's ip in: /home/pi/.octoprint/plugins/config/configuration.json)
