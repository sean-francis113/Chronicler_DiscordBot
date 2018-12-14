import discord
import lib.db
import lib.reaction

#Posts the message into the database
#message: The message to post
#client: The bot's client
async def postToDatabase(message, client):
	editted_content = message.content

	word_list = lib.keywords.getKeywords(message.channel)

	for word in word_list:
		editted_content = lib.keywords.replaceKeyword(editted_content, word['word'], word['replacement'])
		
	lib.db.queryDatabase("INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES ({type}, {char_count}, {word_count}, {entry_owner} {entry_editted}, {entry_original})".format(id=message.channel.id, type="In-Character", char_count=len(editted_content), word_count=len(editted_content.split(" ")), entry_owner=message.author.name, entry_editted=editted_content, entry_original=message.content), checkExists=True, tablename="{id}_contents", commit=True, closeConn=True)
	
	await lib.reaction.reactThumbsUp(message, client)  

async def startRewrite(message, client, finalString, lastMessageFound):
	messagesChecked = 0
	conn = lib.db.connectToDatabase()
	rowCount, result, exists = lib.db.queryDatabase("DELETE FROM {id}_contents".format(id=message.channel.id), connection=conn, checkExists=True, tablename="{id}_contents".format(id=message.channel.id), commit=False, closeConn=False)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler could not find this channel in it's database. Has this channel been Whitelisted? If so, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue while adding the following: 'ERROR 404: startRewrite() QUERY: DELETE FROM {id}_contents'".format(id=message.channel.id))
		return
	else:
		async for curMessage in client.logs_from(message.channel, after=lastMessageFound, limit=500):
			lib.db.queryDatabase("INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_content) VALUES ({type}, {char_count}, {word_count}, {entry_owner}, {entry_contents})".format(id=message.channel.id, type="In-Character", char_count=len(curMessage.content), word_count=len(curMessage.content.split(" ")), entry_owner=curMessage.author.name, entry_contents=curMessage.content), connection=conn, checkExists=False, commit=False, closeConn=False)
			
			if messagesChecked == 500:
				lastMessageFound = curMessage
				if client.logs_from(message.channel, after=curMessage, limit=500):
					await startRewrite(message, client, finalString, lastMessageFound)
		conn.cursor().commit()
		await lib.reaction.reactThumbsUp(message, client)
		conn.close()