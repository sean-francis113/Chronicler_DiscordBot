import discord
import lib.db

async def displayChannelStats(message, client):
  #Connect to Database
  cursor = lib.db.connectToDatabase()

  rowCount, retval = lib.db.queryDatabase(cursor, ("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id)), False, True)

  if rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")
  else:
    if retval['is_blacklisted'] == True:
      await client.send_message(message.channel, "This channel has been blacklisted. You can no longer get its stats.")
    else:
      rowCount, contentData = lib.db.queryDatabase(cursor, ("SELECT * FROM %s_contents", (message.channel.id)), False, True)

      messageStr = ('Stats for ' + message.channel.name + '/n/n'
      'Is Closed = ' + retval['is_closed'] + '\n'
      'Is Private = ' + retval['is_private'] + '\n'
      'Channel ID = ' + retval['channel_id'] + '\n'
      'Channel Creator = ' + retval['channel_owner'] + '\n'
      'Has Warnings = ' + retval['has_warnings'] + '\n'
      'Warning List = ' + retval['warning_list'] + '\n'
      'Date Last Modified = ' + retval['date_last_modified'] + '\n'
      'Character Count = ' + len(lib.story.getContents(message.channel)) + '/~16,777,215')

      await client.send_message(message.channel, messageStr)  