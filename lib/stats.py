import discord
import mysql.connector
import lib.db

async def displayChannelStats(message, client):
  #Connect to Database
  cursor = lib.db.connectToDatabase()

  rowCount, retval = lib.db.queryDatabase(cursor, ("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id)), False, True)

  if rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")
  else:
    if channelData['is_blacklisted'] == True:
      await client.send_message(message.channel, "This channel has been blacklisted. You can no longer get its stats.")
    else:
      rowCount, contentData = lib.db.queryDatabase(cursor, ("SELECT * FROM %s_contents", (message.channel.id)), False, True)

      messageStr = ('Stats for ' + message.channel.name + '/n/n'
      'Is Closed = ' + channelData['is_closed'] + '\n'
      'Is Private = ' + channelData['is_private'] + '\n'
      'Channel ID = ' + channelData['channel_id'] + '\n'
      'Channel Creator = ' + channelData['channel_owner'] + '\n'
      'Has Warnings = ' + channelData['has_warnings'] + '\n'
      'Warning List = ' + channelData['warning_list'] + '\n'
      'Date Last Modified = ' + channelData['date_last_modified'] + '\n'
      'Character Count = ' + len(getContents(message.channel)) + '/~16,777,215')

      await client.send_message(message.channel, messageStr)  