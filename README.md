# IMSA-3D-Printer-Management
Remote management and control of IMSA's 3D printers via OctoPrint and a webservice

There are two parts of this system: the server pi (only 1) and the printer pi's (1 pi per printer)

Server Pi:

* NOOBS (Raspbian) - NOOBS: https://www.raspberrypi.org/downloads/noobs/
  - Download the zip for the NOOBS 3.5.0 OS (not NOOBS Lite) from the link above
  - Format a micro SD card (at least 16GB) with FAT32 and empty memory
  - Extract NOOBS's zipped folder to a micro SD card (tutorial: https://thepi.io/how-to-install-noobs-on-the-raspberry-pi/)
  - Using an HDMI cable and adapter to project the pi to a monitor, boot it up and select Raspbian/Raspberry Pi Operating System
  - Set up WiFi
* Connect Server Pi to WiFi network (Can be done with a monitor, keyboard, and mouse)
* On the Pi's Desktop, select the upper left button->Preferences->Raspberry Pi Configuration->Interfaces
  - Find the "SSH" option and set it to enabled
* Install Node.js (Follow instructions below)
  - Use CygWin64 on Windows (https://www.cygwin.com/) or terminal with Mac/Linux
  - run "ssh pi@ip_address"
  - Enter Server Pi Password
* Run the following commands in the home directory of the pi ("cd ~/")
  - "curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -"
  - "sudo apt-get install nodejs"
  - "curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -"
  - "echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list"
  - "sudo apt-get update && sudo apt-get install yarn"
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
  - If you get an error (i.e. "/usr/local/bin/node: No such file or directory"), run the following commands
    - "sudo apt full-upgrade -y"
    - "curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -"
    - "sudo apt-get install -y nodejs"
    - "sudo ln -s /usr/bin/nodejs /usr/local/bin/node"
* Copy all files in server folder (index.ejs, index.js, openPage.sh) to /home/pi/statusPage
  - Download the files to a computer, (Cygwin if Windows, terminal if Mac/Linux) cd to the directory they are stored in (i.e. "cd C:/Users/user_name/Desktop"), and run the following
  - "scp index.ejs pi@ip_address:/home/pi/statusPage/"
  - "scp index.js pi@ip_address:/home/pi/statusPage/"
  - "scp openPage.sh pi@ip_address:/home/pi/statusPage/"
  - On the pi, we have to make openPage.sh executable; run "chmod +x openPage.sh" in /home/pi/statusPage/
* Create a crontab (crontab -e, then pick an editor (/bin/nano)) and paste this line: "@reboot /home/pi/statusPage/openPage.sh"
  - Ctrl+O and Enter to save, Ctrl+X to exit
* Run "sudo reboot"
* To check the webpage is up, type "server_pi_ip_address:3000" in the url bar (i.e. 10.0.0.114:3000)

Printer Pi:

* Install OctoPrint OS on each pi that you intend to connect to a printer (https://octoprint.org/download/) Download a stable version
* Follow this tutorial to install OctoPrint on a micro SD card: https://www.youtube.com/watch?v=xzY2lkOR29c (watch from 2:45 to 6:40)
  - In my experience using Balena Etcher to write the image file, Etcher will say "Flash failed" or something like that, but it doesn't appear to cause any noticeable problems, so just ignore it
  - Also make sure to set up WiFi information on the OS and region information (UK/France/U.S/etc)
    - Set up the WiFi network on the same network as the Server Pi
* Head to the printer pi's ip and set up OctoPrint accounts
  - When setting up the accounts, you will be able to provide each printer's name and model
  - Whatever is entered into the name field will appear on the server webpage, so if you have multiple printers, you should probably name them differently
* Copy everything in the printer folder (config, findPrinterStatus.py) to "/home/pi/.octoprint/plugins" on the printer pi
  - This can be done using ssh (CygWin for Windows, Terminal for Mac/Linux):
    - "ssh pi@ip_address" (unlike with the server pi, ssh is automatically enabled)
    - Enter pi's password (default is "raspberry", you can change it by running command "passwd")
    - "cd ~/.octoprint/plugins/"
    - "mkdir config"
    - Open another CygWin/Terminal on a computer, download both findPrinterStatus.py and configuration.json (save both to desktop), and perform the next 3 lines on the computer:
    - Run "cd C:/file_location/" (Enter "ls" to list files and check that you can see findPrinterStatus.py and configuration.json)
    - "scp findPrinterStatus.py pi@ip_address:/home/pi/.octoprint/plugins/" (This copies the plugin file)
    - "scp configuration.json pi@ip_address:/home/pi/.octoprint/plugins/config/" (This copies the configuration file into the config folder)
    - Back on the CygWin/Terminal that is ssh'd to the printer pi, run the following:
    - "nano ~/.octoprint/plugins/config/configuration.json"
    - You will see this line: "{ "server_url":"http://10.0.0.114:3000", "comments":"replace 10.0.0.114 with the ip of your server pi (you should only have 1 server pi)" }"
    - Change the "10.0.0.114" to the ip of your server Pi, then save (Ctrl+O) and exit (Ctrl+X)
    - Reboot the printer pi for the changes to take effect
