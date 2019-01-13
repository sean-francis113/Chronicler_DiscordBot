import lib.db
import lib.reaction

async def setPrivacy(message, client):
  value = message.content.replace('!c set_private', '')
  lowerValue = value.lower()

  conn = lib.db.connectToDatabase()

  if lowerValue.strip() == "true":
    #Update Chronicle in Database
    lib.db.queryDatabase("UPDATE chronicles_info SET is_private = TRUE; WHERE channel_id={id}".format(id=message.channel.id), client, message=message, connection=conn, checkExists=True, tablename="chronicles_info", commit=True, closeConn=True)
  elif lowerValue.strip() == "false":
    #Update Chronicle in Database
    lib.db.queryDatabase("UPDATE chronicles_info SET is_private = FALSE; WHERE channel_id={id}".format(id=message.channel.id), client, message=message, connection=conn, checkExists=True, tablename="chronicles_info", commit=True, closeConn=True)
  
  await lib.reaction.reactThumbsUp(message, client)