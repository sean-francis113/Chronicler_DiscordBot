import discord
import os
import mysql.connector

from story import getContents

async def displayChannelStats(message, client):
  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  rowCount = cursor.execute("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id))

  if rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")
  else:
    channelData = cursor.fetchone()
    if channelData['is_blacklisted'] == True:
      await client.send_message(message.channel, "This channel has been blacklisted. You can no longer get its stats.")
    else:
      cursor.execute("SELECT * FROM %s_contents")
      contentData = cursor.fetchone()

      messageStr = ('Stats for ' + message.channel.name + '/n/n'
      'Is Closed = ' + channelData['is_closed'] + '\n'
      'Is Private = ' + channelData['is_private'] + '\n'
      'Channel ID = ' + channelData['channel_id'] + '\n'
      'Channel Creator = ' + channelData['channel_owner'] + '\n'
      'Has Warnings = ' + channelData['has_warnings'] + '\n'
      'Warning List = ' + channelData['warning_list'] + '\n'
      'Date Last Modified = ' + channelData['date_last_modified'] + '\n'
      'Word Count = ' + len(getContents(message.channel)) + '/~16,777,215')

      await client.send_message(message.channel, messageStr)  