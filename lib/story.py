import discord
import lib.db

async def closeStory(message, client):
  #Connect to Database
  lib.db.connectAndQuery(("UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id = %s", (message.channel.id)), True, False)

  await client.add_reaction(message, ":thumbup:")

async def openStory(message, client):
  #Connect to Database
  lib.db.connectAndQuery(("UPDATE chronicles_info SET is_closed = FALSE WHERE channel_id = %s", (message.channel.id)), True, False)

  await client.add_reaction(message, ":thumbup:")

#Gets the Contents of a Story from the Database
#channel: The Channel to pull the Story from
#Returns: The full string of the story
def getContents(channel):
  #Connect to Database
  rowCount, retval = lib.db.connectAndQuery(("SELECT * FROM %s_contents", (channel.id)), False, True)
  
  return retval['story_content']

#Edits the Current Chronicle
#database: The Database to find the Chronicle
#oldMessage: The Original Message Contents
#newMessage: The New Message Contents
def editChronicle(client, oldMessage, newMessage):
  #Connect to Database
  cursor = lib.db.connectToDatabase()

  rowCount, retval = lib.db.queryDatabase(cursor, ("SELECT * FROM %s_contents", (newMessage.channel.id)), False, True)

  messageStr = retval['story_content']

  messageStr.replace(oldMessage, newMessage)

  lib.db.queryDatabase(cursor, ("UPDATE %s_contents SET story_content = %s", (newMessage.channel.id, messageStr)), True, False)

  client.add_reaction(newMessage, ":thumbup:")