#!/usr/bin/env python3
# bot.py
import os
import random

import requests
import json

from selenium import webdriver
from time import sleep

import discord

#from dotenv import load_dotenv

from discord.ext import commands

TOKEN = 'GUILD_TOKEN'
GUILD = "GUILD_NAME"

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

file_types = ["gcode"]

def login_session():
    config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
    url = config['post_url']
    login_payload = {'user' : config['user'], 'pass' : config['pass']}
    login_header = {'Content-Type' : 'application/json', 'Content-Encoding' : 'utf-8'}
    uri = '/api/login'
    login_r = requests.post(url+uri,json=login_payload,headers=login_header)
    if(str(login_r.status_code) != "200"):
        print(str(login_r.status_code) + " was not expected (200) from login response!")
    return login_r
def logout_session():
    config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
    url = config['post_url']
    uri = '/api/logout'
    logout_r = requests.post(url+uri)
    if(str(logout_r.status_code) != "200"):
        print(str(logout_r.status_code) + " was not expected (200) from login response!")
    return logout_r

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user.name} is connected to the following guild: {guild.name}\n')
    channel = bot.get_channel(903416462130151469)
    #print(channel)
    await channel.send("Free Trial has expired :book:")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if(message.content.startswith(prefix)):
        await bot.process_commands(message)
    elif message.attachments:
        for attachment in message.attachments:
            #print(str(attachment))
            for file_type in file_types:
                if str(attachment).endswith(file_type):
                    print("Good file sent")
                    await message.channel.send("File uploaded!")
                    url = str(attachment)
                    r = requests.get(url)
                    split = url.split("/")
                    file_name = split[len(split)-1]
                    with open("/home/pi/.octoprint/uploads/"+file_name, 'wb') as f:
                        f.write(r.content)
    #for attachment in message.attachments:
        #if any(attachment.filename.lower().endswith(model) for model in file_types):
            #print("attached file sent!")
@bot.command(name='print',help='Starts a print command [usage: !print "file_path/file_name.gcode"]')
async def select_and_print(ctx,arg):
    #print("arg = " + str(arg))
    login_session()
    config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
    url = config['post_url']
    file_name = str(arg)
    
    print_payload = {'command' : 'select', 'print' : 'true'}
    print_header = {'Content-Type' : 'application/json', 'Content-Encoding' : 'utf-8', 'X-Api-Key' : str(config['api-key'])}
    uri = '/api/files/local/' + file_name
    print_r = requests.post(url+uri,json=print_payload,headers=print_header)
    if(str(print_r.status_code) != "204"):
        print(str(print_r.status_code) + " was not expected (204) response from select and print payload!")
    else:
        await ctx.send(file_name + " print job was started!")
    logout_session()

@bot.command(name='cancel', help='Cancels current print job, if there is one [usage: !cancel]')
async def cancel_print(ctx):
    login_session()
    config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
    url = config['post_url']
    cancel_payload = {'command' : 'cancel'}
    cancel_header = {'Content-Type' : 'application/json', 'Content-Encoding' : 'utf-8', 'X-Api-Key' : str(config['api-key'])}
    uri = '/api/job'
    cancel_r = requests.post(url+uri,json=cancel_payload,headers=cancel_header)
    if(str(cancel_r.status_code) == "409"):
        await ctx.send("Printer does not have an active print job to cancel.")
    elif(str(cancel_r.status_code) == "204"):
        await ctx.send("Cancelled current print job!")
    elif(str(cancel_r.status_code) != "204"):
        print(str(cancel_r.status_code) + " was not expected (204 or 409) response from cancel command!")

    logout_session()
@bot.command(name='files',help='Returns a list of all available gcode files [usage:!files]')
async def get_files(ctx):
    login_session()
    config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
    url = config['post_url']
    uri = '/api/files'
    files_r = requests.get(url+uri,params=None)
    print(str(files_r.status_code)+"\n")
    print(files_r.json())
    logout_session()
@bot.command(name='status',help='Gets information about the current print job [usage:!status]')
async def get_status(ctx):
    #login_session()
    #config = json.load(open('/home/pi/.octoprint/plugins/config/configuration.json'))
    #url = config['server_url']
    #driver = webdriver.Firefox()
    #driver.get(server_url)
    #sleep(1)
    infile = open('/home/pi/DiscordBot/current_status.json')
    data = json.load(infile)
    str_to_print = data['name']
    str_to_print += "Status: " + data['status'] + "\n"
    if data['printJobStarted'] != "":
        str_to_print += "Print Started at " + data['printJobStarted']
    #driver.get_screenshot_as_file("current.png")
    #with open("/home/pi/DiscordBot/current.png","rb") as fh:
        #f = discord.File(fh,filename="/home/pi/DiscordBot/current.png")
    infile.close()
    await ctx.send(str_to_print)
    '''
    uri = '/api/job'
    status_r = requests.get(url+uri,params=None)
    print(status_r.status_code)
    if(str(status_r.status_code) == "403"):
        await ctx.send("Printing has not started yet!")
        logout_session()
    elif(str(status_r.status_code) != "200"):
        print(str(status_r.status_code) + " was not expected (200) response from status command")
        status_str = "Print job: " + status_r.json()['file']['name'] + "\n"
        status_str += "Estimated Print Time: " + str(status_r.json()['estimatedPrintTime']) + "\n"
        status_str += "Current Progress: " + str(float(status_r.json()['progress']['completion'])*100) + "%\n"
        status_str += "Current Print Time: " + str(status_r.json()['progress']['printTime']) + " with Print Time Left: " + str(status_r.json()['progress']['printTimeLeft'])
        status_str += "\nCurrent Status: " + status_r.json()['state']
        await ctx.send(status_str)
    logout_session()
    '''
#@bot.command(name='print', help='Selects and prints given file name')
#async def print(ctx, arg):
    #print(str(arg))
    #await ctx.send("Got it")
@bot.command(name='files',help='Lists all available files [usage:!files]')
async def get_files(ctx):
    file_path = "/home/pi/.octoprint/uploads"
    dir_list = os.listdir(file_path)
    str_to_print = "Available Files:"
    for file_name in dir_list:
        if "gcode" not in str(file_name):
            continue
        str_to_print += "\n" + str(file_name)
    await ctx.send(str_to_print)
#@commands.has_any_role("Incarnation","Outer God")
@bot.command(name='delete',help='Deletes the given file name [usage:!delete "file_name"]')
async def delete_file(ctx,arg):
    file_name = str(arg)
    file_path = "/home/pi/.octoprint/uploads/"
    if(file_name == '' or file_name == "/"):
        await ctx.send("No file specified to delete.")
        return
    try:
        os.remove(file_path + file_name)
        await ctx.send(file_name + " removed successfully.")
        return
    except OSError as error:
        print(error)
        await ctx.send(file_name + " cannot be removed.")
@bot.command(name='stopFeed',help='Stops the Webcam feed')
async def stop_feed(ctx):
    #await ctx.send("Stopping Webcam Feed")
    os.system("/home/pi/Webcam/stopFeed.sh")
    await ctx.send("Stopping Webcam Feed")
@bot.command(name='startFeed',help='Starts the Webcam feed')
async def start_feed(ctx):
    os.system("/home/pi/Webcam/startFeed.sh")
    await ctx.send("Starting Webcam Feed")
@bot.command(name='picture',help='Orders the webcam to take a screenshot and send it to the Discord Server [usage:!picture]')
async def take_picture(ctx):
    await ctx.send("Playing Advertisement...")
    #execfile("/home/pi/Webcam/test_ss.py")
    #sleep(7)
    os.system("/home/pi/Webcam/stopFeed.sh")
    await ctx.send("Stream Paused")
    os.system("/home/pi/Webcam/screenshot.sh")
    await ctx.send("State Captured")
    #sleep(5)
    os.system("/home/pi/Webcam/startFeed.sh")
    await ctx.send("Stream Resumed.")
    await ctx.send(file=discord.File('/home/pi/DiscordBot/ss.jpg'))
@bot.command(name='email', help='Selects the email to notify')
async def print(ctx, arg):
    #print(str(arg))
    email = str(arg)
    file_path = '/home/pi/.octoprint/plugins/config/email_adr.txt'
    infile = open(file_path,"w")
    infile.write(email)
    await ctx.send(arg, " Email selected for notification!")

bot.run(TOKEN)
