import lib.db
import lib.reaction
import lib.keywords
import lib.symbol

async def closeStory(client, message):
		#Connect to Database
		lib.db.queryDatabase(
        "UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id = {id};".
        format(id=message.channel.id),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)
		
		await lib.db.updateModifiedTime(client, message.channel)
		await lib.reaction.reactThumbsUp(message, client)


async def openStory(client, message):
		#Connect to Database
		lib.db.queryDatabase(
        "UPDATE chronicles_info SET is_closed = FALSE WHERE channel_id = {id};"
        .format(id=message.channel.id),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)

		await lib.db.updateModifiedTime(client, message.channel)
		await lib.reaction.reactThumbsUp(message, client)


#Edits the Current Chronicle
#database: The Database to find the Chronicle
#oldMessage: The Original Message Contents
#newMessage: The New Message Contents
def editChronicle(client, oldMessage, newMessage):
		#Connect to Database
		connection = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM {id}_contents".format(id=newMessage.channel.id),
        client,
        oldMessage.channel,
        connection=connection,
        checkExists=True,
        tablename="{id}_contents".format(id=oldMessage.channel.id),
        getResult=True,
        closeConn=False)
				
		for row in retval:
        #0 = entry_id
        #5 = entry_original
				if row[5] == oldMessage.content:
						lib.db.queryDatabase(
                "UPDATE {id}_contents SET entry_original=\"{new}\" WHERE entry_id={entry_id};"
                .format(
                    id=newMessage.channel.id,
                    new=newMessage.content,
                    entry_id=row[0]),
                client,
                oldMessage.channel,
                connection=connection,
                commit=False,
                closeConn=False)
								
								
						editted_content = newMessage.content
						
						editted_content = lib.symbol.replaceMarkdown(editted_content)
						
						word_list = lib.keywords.getKeywords(client, newMessage.channel)
						
						symbol_list = lib.symbol.getSymbols(client, oldMessage.channel)
						
						for word in word_list:
                #0 = word
                #1 = replacement
								editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])
								
						for symbol in symbol_list:
                #0 = start
                #1 = end
								editted_content = lib.symbol.pluckSymbol(editted_content, symbol[0], symbol[1])
										
						lib.db.queryDatabase(
                "UPDATE {id}_contents SET entry_editted=\"{new}\" WHERE entry_id={entry_id};"
                .format(
                    id=newMessage.channel.id,
                    new=editted_content,
                    entry_id=row[0]),
                client,
                oldMessage.channel,
                connection=connection,
                commit=True,
                closeConn=True)
								
		lib.db.updateModifiedTime(client, oldMessage.channel)