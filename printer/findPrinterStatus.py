from __future__ import absolute_import, unicode_literals
from datetime import datetime
import datetime
from pytz import timezone
import time
import socket
import os
#Arthur Wang & Andrew Wang 1/1/2021
import requests
import json

import octoprint.plugin
import octoprint.util
import traceback
from octoprint.events import Events

g_ip = ""
class GetStatus(octoprint.plugin.EventHandlerPlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.StartupPlugin):
        def on_event(self,event,payload):
                global g_ip
                config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
                url = config["server_url"]
                self._logger.info("URL<" + url + ">")
                currentStatus = ""
                startTime = ""
                if event == Events.PRINT_STARTED:
                        currentStatus = "Printing..."
                        central = timezone('America/Chicago')
                        startTime = datetime.datetime.now(central)
                elif event == Events.PRINT_FAILED:
                        currentStatus = "Available (Last Print Failed)"
                elif event == Events.PRINT_DONE:
                        currentStatus = "Available (Last Print Finished)"
                elif event == Events.PRINT_PAUSED:
                        currentStatus = "Print Paused"
                elif event == Events.PRINT_RESUMED:
                        currentStatus = "Printing..."
                elif event == Events.ERROR:
                        currentStatus = "Error!"
                elif event == Events.CONNECTED:
                        currentStatus = "Connected"
                elif event == Events.DISCONNECTED:
                        currentStatus = "Disconnected"
                if currentStatus != "":
                        printerName = ""
                        jsonSend = {}
                        file1 = open('/home/pi/.octoprint/printerProfiles/_default.profile', 'r') #open _data.profile file which contains printer profile name
                        Lines = file1.readlines()
                        #connectionInfo = os.system("ip -o -4 addr show wlan0 | awk '{ split($4, ip_addr, "/"); print ip_addr[1] }'") #str(os.system('hostname -I')).split(" ")
                        for line in Lines:
                                tempLine = line.split(':') #the line we want in _data.profile starts with 'model': printer_name
                                if(tempLine[0]=='name'):
                                        printerName = tempLine[1][1:] #remove space in front of printer_name
                        if g_ip=="":
                                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                sock.connect(('88.88.88.88', 80))
                                g_ip = sock.getsockname()[0]
                                self._logger.info(str(g_ip)+"----------------------------------------------------------")
                        #the previous three lines plus "import socket" get the ip address of this pi
                        job = self._printer.get_current_data()["job".encode("utf-8")]
                        name = str(g_ip)+":"+printerName ### NAME ###
                        self._logger.info(str(job).encode("utf-8"))
                        jsonSend['name'] = name
                        jsonSend['status'] = currentStatus ### CURRENT STATUS ###
                        if(currentStatus=="Printing..."):
                                jobName = str(job['file']['name'])
                                jsonSend['printJobStarted'] = startTime.strftime('%H:%M:%S %m/%d/%Y') ### START TIME ###
                                printingJobFile = open(("/home/pi/.octoprint/uploads/"+jobName))
                                content = printingJobFile = printingJobFile.readlines()
                                printTimeLine = content[1]
                                timeSeconds = int((printTimeLine.split(":"))[1]) ### PRINT TIME ###
                                jsonSend['estimatedPrintTime'] = str(datetime.timedelta(seconds=timeSeconds))
                        else:
                                jsonSend['printJobStarted'] = ""
                                jsonSend['estimatedPrintTime'] = ""
                        jsonSend['job'] = job
                        r = requests.post(url, data=json.dumps(jsonSend), headers={'Content-type':'application/json','Accept':'text/plain'})


__plugin_implementation__ = GetStatus()

