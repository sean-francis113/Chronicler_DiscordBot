import discord
import os
import mysql.connector

async def getChronicle(message, client):
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT is_blackmailed FROM chronicles_info WHERE channel_id=" + message.channel.id)

  retval = cursor.fetchone()
  
  if retval['is_blackmailed'] == False:
    await client.send_message(message.channel, "Link to Your Chronicle: http://chronicler.seanmfrancis.net/chronicle.php?id=" + message.channel.id + "&page=1")
  else:
    await client.send_message(message.channel, "This Chronicle has been blacklisted. You cannot get its link ever again.")