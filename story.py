import discord
import os
import mysql.connector

async def closeStory(message, client):
  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id = %s", (message.channel.id))

  await client.add_reaction(message, ":thumbup:")

async def openStory(message, client):
  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("UPDATE chronicles_info SET is_closed = FALSE WHERE channel_id = %s", (message.channel.id))

  await client.add_reaction(message, ":thumbup:")

#Gets the Contents of a Story from the Database
#channel: The Channel to pull the Story from
#Returns: The full string of the story
def getContents(channel):
  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM %s_contents", (channel.id))

  contentData = cursor.fetchone()

  return contentData['story_content']

#Edits the Current Chronicle
#database: The Database to find the Chronicle
#oldMessage: The Original Message Contents
#newMessage: The New Message Contents
def editChronicle(oldMessage, newMessage):
  #Connect to Database
  #Could Get Chronicle with getContent(), but I still need the connection afterward
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM %s_contents", (channel.id))

  contentData = cursor.fetchone()
  messageStr = contentData['story_content']

  messageStr.replace(oldMessage, newMessage)
  messageStr += '\n'

  cursor.execute("UPDATE %s_contents SET story_content = %s")