import discord
import os
import mysql.connector

async def setPrivacy(message, client):
  value = message.content.replace('!c set_private', '')
  lowerValue = value.lower()

  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  if lowerValue.strip() == "true":
    #Update Chronicle in Database
    cursor.execute("UPDATE chronicles_info SET is_private = TRUE; WHERE channel_id=%s", (message.channel.id))
  elif lowerValue.strip() == "false":
    #Update Chronicle in Database
    cursor.execute("UPDATE chronicles_info SET is_private = FALSE; WHERE channel_id=%s", (message.channel.id))
  
  await client.add_reaction(message, ":thumbup:")