import datetime
import requests
import os


def openLogFile(channel):
    filePath = ("{url}/logs/{channel_id}_{date}.txt".format(
				url=os.environ.get("CHRONICLER_WEBSITE_URL"), 
        channel_id=channel.id,
        date=datetime.datetime.now().strftime("%Y-%m-%d")))

    logFile = requests.get(filePath)

    return logFile, filePath


def closeLogFile(logFile):
    logFile.close()


def writeToLogFile(logFile, strToWrite):
    logFile.write(strToWrite)


def updateLogFile(channel, strToWrite, closeFile=True):
    logFile, filePath = openLogFile(channel)

    writeToLogFile(logFile, strToWrite)

    if closeFile == True:
        closeLogFile(logFile)
        return
    else:
        return logFile
