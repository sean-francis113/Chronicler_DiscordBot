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

  cursor.execute("SELECT is_blackmailed FROM chronicles_info WHERE channel_id=%s", (message.channel.id))

  if cursor.rowcount == 1:
    retval = cursor.fetchone()
  
    if retval['is_blackmailed'] == False:
      await client.send_message(message.channel, ("Link to Your Chronicle: http://chronicler.seanmfrancis.net/chronicle.php?id=%s&page=1", (message.channel.id)))
    elif retval == True:
      await client.send_message(message.channel, "This Chronicle has been blacklisted. You cannot get its link ever again.")
  else:
    await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")