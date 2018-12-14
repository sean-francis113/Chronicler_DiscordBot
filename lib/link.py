import discord
import lib.db
import lib.reaction

async def getChronicle(message, client):
  rowCount, retval, exists = lib.db.queryDatabase("SELECT is_blackmailed FROM chronicles_info WHERE channel_id={id}".format(id=message.channel.id), checkExists=True, tablename="chronicles_info", commit=False, closeConn=True)

  if rowCount == 1:
    if retval['is_blackmailed'] == False:
      await client.send_message(message.channel, ("Link to Your Chronicle: http://chronicler.seanmfrancis.net/chronicle.php?id={id}&page=1".format(id=message.channel.id)))
    elif retval['is_blackmailed'] == True:
      await client.send_message(message.channel, "This Chronicle has been blacklisted. You cannot get its link ever again.")
  elif rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")