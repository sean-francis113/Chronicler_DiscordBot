import lib.db
import lib.reaction
import lib.keywords
import lib.symbol

async def closeStory(client, message):
		"""
		Functions That Closes the Story in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""

		lib.db.queryDatabase(
        "UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id = {id};".
        format(id=str(message.channel.id)),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)
		
		await lib.reaction.reactThumbsUp(client, message)


async def openStory(client, message):
		"""
		Functions That Opens the Story in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""

		lib.db.queryDatabase(
        "UPDATE chronicles_info SET is_closed = FALSE WHERE channel_id = {id};"
        .format(id=str(message.channel.id)),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)

		await lib.reaction.reactThumbsUp(client, message)


def deleteChronicle(client, messageID, channelID):
		"""
		Functions That Deletes a Message From the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				messageID (integer)
						The ID Number of the Message to Delete
				channelID (integer)
						The ID Number of the Channel the Message is in
		"""

		conn = lib.db.connectToDatabase()
		cursor = conn.cursor()

		exists = lib.db.checkIfTableExists(cursor, "%s_contents" %(channelID))

		if exists == False:
				return

		cursor = conn.cursor()
		cursor.execute("DELETE FROM {channel_id}_contents WHERE message_id={message_id}".format(channel_id=str(channelID), message_id=str(messageID)))

		conn.commit()
		cursor.close()
		conn.close()


#Edits the Current Chronicle
#database: The Database to find the Chronicle
#message: The Original Message Contents
#message: The New Message Contents
def editChronicle(client, message):
		"""
		Functions That Edits a Message in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""

		#Connect to Database
		connection = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM {id}_contents".format(id=str(message.channel.id)),
        client,
        message.channel,
        connection=connection,
        checkExists=True,
        tablename="{id}_contents".format(id=str(message.channel.id)),
        getResult=True,
        closeConn=False)
		
		for row in retval:
        #0 = entry_id
        #1 = message_id
				if row[1] == str(message.id):
						original_content = message.content
						editted_content = message.content
						
						word_list = lib.keywords.getKeywords(client, message.channel)

						symbol_list = lib.symbol.getSymbols(client, message.channel)
						
						for word in word_list:
                #0 = word
                #1 = replacement
								editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])
								
						for symbol in symbol_list:
                #0 = start
                #1 = end
								editted_content = lib.symbol.pluckSymbol(editted_content, symbol[0], symbol[1])

						editted_content = lib.symbol.replaceMarkdown(editted_content)
						
						#Handle Curly Quotes
						original_content = original_content.replace('“','"').replace('”','"')
						original_content = original_content.replace("‘","'").replace("’","'")
						editted_content = editted_content.replace('“','"').replace('”','"')
						editted_content = editted_content.replace("‘","'").replace("’","'")
				
				    #Keep Any Quotes in the Message
						original_content = original_content.replace("'", "\\'")
						editted_content = editted_content.replace("'", "\\'")

						is_pinned = message.pinned

						lib.db.queryDatabase(
                "UPDATE {id}_contents SET entry_original=\"{original}\", entry_editted=\"{new}\", is_pinned={pinned} WHERE entry_id={entry_id};"
                .format(
                    id=str(message.channel.id),
										original=original_content,
                    new=editted_content,
										pinned=str(is_pinned).upper(),
                    entry_id=row[0]),
                client,
                message.channel,
                connection=connection,
                commit=True,
                closeConn=True)

						break

		lib.db.updateModifiedTime(client, message.channel)