import lib.db
import lib.reaction

async def closeStory(message, client):
  #Connect to Database
  lib.db.queryDatabase("UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id = {id};".format(id=message.channel.id), client, channel=message.channel, checkExists=True, tablename="chronicles_info", commit=True, closeConn=True)

  await lib.reaction.reactThumbsUp(message, client)

async def openStory(message, client):
  #Connect to Database
  lib.db.queryDatabase("UPDATE chronicles_info SET is_closed = FALSE WHERE channel_id = {id};".format(id=message.channel.id), client, channel=message.channel, checkExists=True, tablename="chronicles_info", commit=True, closeConn=True)

  await lib.reaction.reactThumbsUp(message, client)

#Edits the Current Chronicle
#database: The Database to find the Chronicle
#oldMessage: The Original Message Contents
#newMessage: The New Message Contents
def editChronicle(client, oldMessage, newMessage):
  #Connect to Database
	connection = lib.db.connectToDatabase()
	
	rowCount, retval, exists = lib.db.queryDatabase("SELECT * FROM {id}_contents".format(id=newMessage.channel.id), client, channel=oldMessage.channel, connection=connection, checkExists=True, tablename="{id}_contents".format(id=oldMessage.channel.id), getResult=True, closeConn=False)
	
	for row in retval:
		print(row[5])
		#0 = entry_id
		#5 = entry_original
		if row[5] == oldMessage.content:
			print("Found Row")
			lib.db.queryDatabase("UPDATE {id}_contents SET entry_original=\"{new}\" WHERE entry_id={entry_id};".format(id=newMessage.channel.id, new=newMessage.content, entry_id=row[0]), client, channel=oldMessage.channel, connection=connection, commit=False, closeConn=False)

			editted_content = newMessage.content
			word_list = lib.keywords.getKeywords(client, newMessage.channel)
			print("Getting Symbols")
			symbol_list = lib.symbol.getSymbols(client, oldMessage.channel)

			for word in word_list:
				#0 = word
				#1 = replacement
				print("Checking " + word[0])
				editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])

			for symbol in symbol_list:
				#0 = start
				#1 = end
				print("Checking " + symbol[0])
				editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0], symbol[1])

			lib.db.queryDatabase("UPDATE {id}_contents SET entry_editted=\"{new}\" WHERE entry_id={entry_id};".format(id=newMessage.channel.id, new=editted_content, entry_id=row[0]), client, channel=oldMessage.channel, connection=connection, commit=True, closeConn=True)