import lib.keywords
import lib.symbol
import lib.db
import lib.reaction

#Posts the message into the database
#message: The message to post
#client: The bot's client
async def postToDatabase(message, client):
	editted_content = message.content
	
	word_list = lib.keywords.getKeywords(client, message.channel)
	symbol_list = lib.symbol.getSymbols(client, message.channel)

	for word in word_list:
		editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])

	for symbol in symbol_list:
		print("Start: " + symbol[0])
		print("End: " + symbol[1])
		print("String to Edit: " + editted_content)
		editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0], symbol[1])
		print("After A Symbol Replacement: " + editted_content)

	lib.db.queryDatabase("INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{type}\', {char_count}, {word_count}, \"{entry_owner}\", \"{entry_editted}\", \"{entry_original}\")".format(id=message.channel.id, type="In-Character", char_count=len(editted_content), word_count=len(editted_content.split(" ")), entry_owner=message.author.name, entry_editted=editted_content, entry_original=message.content), client, channel=message.channel, checkExists=True, tablename="{id}_contents".format(id=message.channel.id), commit=True, closeConn=True)
	
	await lib.reaction.reactThumbsUp(message, client)  

#Rewrite the Whole Chronicle Frm the Beginning
async def startRewrite(message, client, finalString, lastMessageFound):
	messagesChecked = 0
	conn = lib.db.connectToDatabase()
	rowCount, result, exists = lib.db.queryDatabase("DELETE FROM {id}_contents".format(id=message.channel.id), client, channel=message.channel, connection=conn, checkExists=True, tablename="{id}_contents".format(id=message.channel.id), commit=False, closeConn=False)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler could not find this channel in it's database. Has this channel been Whitelisted? If so, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue while adding the following: 'ERROR 404: startRewrite() QUERY: DELETE FROM {id}_contents'".format(id=message.channel.id))
		return
	else:
		async for curMessage in client.logs_from(message.channel, after=lastMessageFound, limit=500):
			editted_content = message.content

			word_list = lib.keywords.getKeywords(client, message.channel)
			symbol_list = lib.symbol.getSymbols(client, message.channel)

			for word in word_list:
				editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])

			for symbol in symbol_list:
				editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0], symbol[1])

			lib.db.queryDatabase("INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\"{type}\", {char_count}, {word_count}, \"{entry_owner}\", \"{entry_editted}\", \"{entry_original}\")".format(id=message.channel.id, type="In-Character", char_count=len(editted_content), word_count=len(editted_content.split(" ")), entry_owner=message.author.name, entry_editted=editted_content, entry_original=message.content), client, channel=message.channel, connection=conn, checkExists=False, commit=False, closeConn=False)
			
			if messagesChecked == 500:
				lastMessageFound = curMessage
				if client.logs_from(message.channel, after=curMessage, limit=500):
					await startRewrite(message, client, finalString, lastMessageFound)

		rowCount, retval, exists = lib.db.queryDatabase("SELECT * FROM {id}_contents")
		
		if(rowCount > 0):
			conn.commit()
			await lib.reaction.reactThumbsUp(message, client)
		else:
			await lib.reaction.reactThumbsDown(message, client)
		conn.close()