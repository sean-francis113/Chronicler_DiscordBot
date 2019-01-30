import datetime


def openLogFile(channel):
    filePath = ("logs/{channel_id}_{date}.txt".format(
        channel_id=channel.id,
        date=datetime.datetime.now().strftime("%Y-%m-%d")))

    logFile = open(filePath, "a+")

    return logFile, filePath


def closeLogFile(logFile):
    logFile.close()


def writeToLogFile(logFile, strToWrite):
    logFile.write(strToWrite)


def updateLogFile(channel, strToWrite):
    logFile, filePath = openLogFile(channel)

    writeToLogFile(logFile, strToWrite)

    closeLogFile(logFile)
