from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import octoprint.util

import socket
import os
#Arthur Wang & Andrew Wang 1/1/2021
import json
import datetime
from datetime import timezone
from datetime import timedelta
import pytz
import requests

from octoprint.events import Events

class FindPrinterStatus(octoprint.plugin.StartupPlugin, octoprint.plugin.EventHandlerPlugin):
	def on_event(self, event, payload):
		g_ip = ""
		config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
		url = config["server_url"]
		self._logger.info("URL<" + url + ">")
		currentStatus = ""
		startTime = ""
		
		if event == Events.PRINT_STARTED:
			currentStatus = "Printing..."
			naiveTime = datetime.datetime.now()
			timezone = pytz.timezone("America/Chicago")
			startTime = timezone.localize(naiveTime)
			self._logger.info("Event PrintStarted triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.PRINT_FAILED:
			currentStatus = "Available (Last Print Failed)"
			self._logger.info("Event PrintFailed triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.PRINT_DONE:
			currentStatus = "Available (Last Print Finished)"
			self._logger.info("Event PrintDone triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.PRINT_PAUSED:
			currentStatus = "Print Paused"
			self._logger.info("Event PrintPaused triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.PRINT_RESUMED:
			currentStatus = "Resumed Printing..."
			self._logger.info("Event PrintResumed triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.ERROR:
			currentStatus = "CRITICAL ERROR!"
			self._logger.info("CRITICAL ERROR TRIGGERED! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.CONNECTED:
			currentStatus = "Connected"
			self._logger.info("Event Connected triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			#os.system('python3 /home/pi/DiscordBot/bot.py')
		elif event == Events.DISCONNECTED:
			currentStatus = "Disconnected!"
			self._logger.info("Event Disconnected triggered! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		elif event == Events.UPDATED_FILES:
			self._logger.info("FILEs updated   ||||||||||||||||||||||||||||||||||||||||||||||||")
		if currentStatus != "":
			printerName = ""
			jsonSend = {}
			file1 = open('/home/pi/.octoprint/printerProfiles/_default.profile','r') # contains printer information like name
			Lines = file1.readlines()
			for line in Lines:
				tempLine = line.split(":") # line we are looking for is formatted 'model' : printer_name
				if tempLine[0] == 'name':
					printerName = tempLine[1][1:] # remove leading space
			if g_ip == "":
				sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				sock.connect(('88.88.88.88',80))
				g_ip = sock.getsockname()[0] # these three lines get the ip address
				#self._logger.info(str(g_ip) + " is the ip of this printer! >>>>>>>>>>>>>>>>")
			name = str(g_ip) + ":" + printerName ### IP AND NAME OF PRINTER ###
			jsonSend['name'] = name
			jsonSend['status'] = currentStatus
			if currentStatus == "Printing...":
				jobName = payload['name'] ### NAME OF PRINT JOB ###
				jsonSend['printJobStarted'] = startTime.strftime('%H:%M:%S %m/%d/%Y') ### STARTING TIME OF PRINT JOB ###
				printingJobFile = open(("/home/pi/.octoprint/uploads/" + jobName))
				content = printingJobFile = printingJobFile.readlines()
				printTimeLine = content[1]
				timeSeconds = int((printTimeLine.split(":"))[1]) ### ESTIMATED PRINT TIME IN SECONDS ###
				printTimeSeconds = datetime.timedelta(seconds = timeSeconds)
				jsonSend['estimatedPrintTime'] = str(printTimeSeconds)
				jsonSend['estimatedEndTime'] = (startTime + printTimeSeconds).strftime('%H:%M:%S %m/%d/%Y, ') ### END TIME BASED ON ESTIMATED PRINT TIME ###
			else:
				jsonSend['printJobStarted'] = ""
				jsonSend['estimatedPrintTime'] = ""
			jsonSend['job'] = payload
			s = requests.Session()
			r = requests.post(url, data=json.dumps(jsonSend, default=str), headers={'Content-type':'application/json','Accept':'text/plain'})
			outfile = open("/home/pi/DiscordBot/current_status.json","w")
			json_object = json.dumps(jsonSend,indent = 4)
			outfile.write(json_object)
			outfile.close()
			s.get(r.url)
		#self._logger.info("Hello World!")
		
__plugin_name__ = "Find Printer Status"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Sends information about itself to a webpage"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = FindPrinterStatus()
