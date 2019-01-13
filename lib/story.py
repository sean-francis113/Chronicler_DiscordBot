import lib.db
import lib.reaction

async def closeStory(message, client):
  #Connect to Database
  lib.db.queryDatabase("UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id = {id};".format(id=message.channel.id), client, message=message, checkExists=True, tablename="chronicles_info", commit=True, closeConn=True)

  await lib.reaction.reactThumbsUp(message, client)

async def openStory(message, client):
  #Connect to Database
  lib.db.queryDatabase("UPDATE chronicles_info SET is_closed = FALSE WHERE channel_id = {id};".format(id=message.channel.id), client, message=message, checkExists=True, tablename="chronicles_info", commit=True, closeConn=True)

  await lib.reaction.reactThumbsUp(message, client)

#Edits the Current Chronicle
#database: The Database to find the Chronicle
#oldMessage: The Original Message Contents
#newMessage: The New Message Contents
def editChronicle(client, oldMessage, newMessage):
  #Connect to Database
	connection = lib.db.connectToDatabase()
	
	rowCount, retval, exists = lib.db.queryDatabase("SELECT * FROM {id}_contents".format(newMessage.channel.id), client, message=oldMessage, connection=connection, checkExists=True, tablename="{id}_contents".format(id=oldMessage.channel.id), getResult=True, closeConn=False)
	
	for row in retval:
		if row['entry_original'] == newMessage.content:
			lib.db.queryDatabase("UPDATE {id}_contents SET entry_original = {new} WHERE entry_id = {entry_id}".format(id=newMessage.channel.id, new=newMessage.content, entry_id=row['entry_id']), client, message=oldMessage, connection=connection, commit=False, closeConn=False)

			editted_content = newMessage.content
			word_list = lib.keywords.getKeywords(newMessage.channel)

			for word in word_list:
				editted_content = lib.keywords.replaceKeyword(editted_content, word['word'], word['replacement'])

			lib.db.queryDatabase("UPDATE {id}_contents SET entry_editted = {new} WHERE entry_id = {entry_id}".format(id=newMessage.channel.id, new=editted_content, entry_id=row['entry_id']), client, message=oldMessage, connection=connection, commit=True)