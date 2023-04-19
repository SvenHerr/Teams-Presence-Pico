##!/usr/bin/env python
# Python script to show Teams presence status on led
# Author: Sven Herrmann
# Date 08.04.2023


# Define Error Logging
def printerror(ex):
    print('\033[31m' + str(ex) + '\033[0m')


def printwarning(warn):
    print('\033[33m' + str(warn) + '\033[0m')


# #############
# Define Var
global name
status = ""
sleepValue = 3  # seconds
version = 1.0
global loopRun
loopRun = True

print("Welcome to Microsoft Teams presence for Pi!")
print("Loading modules...")

try:
    from time import sleep
    from datetime import datetime, time
    from types import SimpleNamespace
    from signal import signal, SIGINT
    import os
    import os.path
    import json
    import re
    import serial
    import configparser
    import requests
except ModuleNotFoundError as ex:
    printerror("The app could not be started. Some modules are missing")
    printerror(ex)
    exit(2)
except:
    printerror("An unknown error occured while loading modules.")
    exit(2)
sleep(2)

config = configparser.ConfigParser()
test = str(os.getcwd())
if os.path.isfile(str("D:/TFS/Scripte/pc-pi_config.ini")):
    print("Reading config...")
    config.read("pc-pi_config.ini")
    path = config["Setting"]["path"]
    fileName = config["Setting"]["filename"]
    sleepValue = config["Setting"]["sleepvalue"]
else:
    printwarning("Config does not exist, creating new file.")
    path = "C:/Users/YourUser/AppData/Roaming/Microsoft/Teams/"
    fileName = "logs.txt"
    while not path:
        path = input("Please enter your location path: ")
    while not fileName:
        fileName = input("Please enter your file name: ")
    config["Setting"] = {"path": path, "fileName": fileName, "sleepValue": 5}
    with open("pc-pi_config.ini", "w") as configfile:
        config.write(configfile)

# Checks for updates
def checkUpdate():
    updateUrl = "https://raw.githubusercontent.com/SvenHerr/Teams-Presence-Pico/master/doc/version"
    try:
        f = requests.get(updateUrl, timeout=10)
        latestVersion = float(f.text)
        if latestVersion > version:
            printwarning("There is an update available.")
            printwarning(
                "Head over to https://github.com/SvenHerr/Teams-Presence-Pico to get the latest features.")
        else:
            print("Application is running latest version.")
    except Exception as e:
        printerror("An error occured while searching for updates.")
        printerror(e)


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Time until next run: " + timer, end="\r")
        sleep(1)
        t -= 1
    print("                                      ", end="\r")

# Handles Ctrl+C
def handler(signal_received, frame):
    # Handle any cleanup here
    printwarning(
        'SIGINT or CTRL-C detected. Please wait until the service has stopped.')
    status = getStatusbyte('Offline')
    s.write(status)
    print()
    exit(0)

def setUserName():
    for line1 in reversed(list(open(path + fileName))):
        if 'CREATE_USER' in line1:
            # Parse JSON into an object with attributes corresponding to dict keys.
            x = json.loads(line1, object_hook=lambda d: SimpleNamespace(**d))
            global name
            name = x.user.profile.name
            break

def connect():
    try:
       global s
       s = serial.Serial("COM6", 9600, timeout=3)
    except Exception as err:
        print()
        print('Error: Connection not possible!')
        print('Please connect device and try again!')
        exit(1)

def getStatusbyte(status):
    return bytes(status + "\n", encoding='utf-8')

def getStatusFromFile():
    word = 'Added'
    startIndex = re.search(r'\b({})\b'.format(word), line).start()
    endIndex = startIndex + word.__len__()

    # start from status until whitespace
    statusLine = line[endIndex+1:]
    whitespace = statusLine.find(' ')

    # retracts status
    status = statusLine[:whitespace] 
    return status  

# Main
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    
    try:
        checkUpdate()
    except Exception as err:
        print()
        print('Error: Cant check for updates!')
        print('Nothing happened, script is still running!')

    setUserName()
    connect()
        
    while loopRun:
        for line in reversed(list(open(path + fileName))):
            if 'StatusIndicatorStateService: Added' in line:
                # on windows
                os.system('cls')
                
                status = getStatusFromFile()
                statusbyte = getStatusbyte(status)
                if 'NewActivity' not in status:
                    s.write(statusbyte)

                print("============================================")
                print("            MSFT Teams Presence")
                print("============================================")
                print()
                print('Hi ' + name + ','+' your currrent state is => ' + status + '')
                now = datetime.now()
                print("Last File call:\t\t" + now.strftime("%Y-%m-%d %H:%M:%S"))

                break
        countdown(int(sleepValue))
