import discord
import lib.db

async def getChronicle(message, client):
  rowCount, retval = lib.db.queryAndConnect(("SELECT is_blackmailed FROM chronicles_info WHERE channel_id=%s", (message.channel.id)), False, True)

  if rowCount == 1:
    if retval['is_blackmailed'] == False:
      await client.send_message(message.channel, ("Link to Your Chronicle: http://chronicler.seanmfrancis.net/chronicle.php?id=%s&page=1", (message.channel.id)))
    elif retval['is_blackmailed'] == True:
      await client.send_message(message.channel, "This Chronicle has been blacklisted. You cannot get its link ever again.")
  elif rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")