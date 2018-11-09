import discord
import lib.db

async def setPrivacy(message, client):
  value = message.content.replace('!c set_private', '')
  lowerValue = value.lower()

  cursor = lib.db.connectToDatabase()

  if lowerValue.strip() == "true":
    #Update Chronicle in Database
    lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET is_private = TRUE; WHERE channel_id=%s", (message.channel.id)), True, False)
  elif lowerValue.strip() == "false":
    #Update Chronicle in Database
    lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET is_private = FALSE; WHERE channel_id=%s", (message.channel.id)), True, False)
  
  await client.add_reaction(message, ":thumbup:")