import discord
import os
import mysql.connector

async def setWarnings(message, client):
  value = message.content.replace("!c set_warnings", '')

  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  if value == '':
    cursor.execute("UPDATE chronicles_info SET has_warning = FALSE")
  else:
    cursor.execute("UPDATE chronicles_info SET has_warning = TRUE")

  cursor.execute("UPDATE chronicles_info SET warning_list = %s", (value.strip()))

  await client.add_reaction(message, ":thumbup:")

async def addWarning(message, client):
  value = message.content.replace("!c add_warning", '')

  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id))

  contentData = cursor.fetchone()

  addition = ''

  if contentData['warning_list'].endswith(','):
    addition = contentData['warning_list'] + value.strip()
  else:
    addition = contentData['warning_list'] + ',' + value.strip()

  cursor.execute("UPDATE chronicles_info SET has_warning = TRUE WHERE channel_id = %s", (message.channel.id))
  cursor.execute("UPDATE chronicles_info SET warning_list = %s", (addition.strip()))

  await client.add_reaction(message, ":thumbup:")

async def removeWarning(message, client):
  value = message.content.replace("!c remove_warning", '')

  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id))

  contentData = cursor.fetchone()

  warningList = contentData['warning_list']
  index = warningList.find(value)

  if index != -1:
    #Need to Check for Comma
    endOfWord = index + len(value.strip())
    finalList = ''
    if value[endOfWord] == ',':
      finalList = warningList.replace((value + ', '), '')
    else:
      finalList = warningList.replace(value, '')

    if finalList == '':
      cursor.execute("UPDATE chronicles_info SET has_warning = FALSE WHERE channel_id = %s", (message.channel.id))
    else:
      cursor.execute("UPDATE chronicles_info SET has_warning = TRUE WHERE channel_id = %s", (message.channel.id))

    cursor.execute("UPDATE chronicles_info SET warning_list = %s", (finalList.strip()))

    await client.add_reaction(message, ":thumbup:")
  else:
    await client.sendMessage(message.channel, "The Chronicler did not find the warning you wish to remove. Are you sure you spelled it right?")