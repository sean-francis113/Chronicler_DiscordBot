import lib.db
import lib.reaction

async def addKeyword(message, client):
	value = message.content.replace('!c add_keyword', '')
	keywordValues = value.split('|')
	
	conn = lib.db.connectToDatabase()
	
	rowCount, result, exists = lib.db.queryDatabase("SELECT keyword FROM {id}_keywords WHERE keyword=\"{word}\"".format(id=message.channel.id, word=keywordValues[0].strip()), connection=conn, checkExists=True, tablename="{id}_keywords".format(id=message.channel.id), getResult=True)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler ran into an issue. Please use our contact form at chronicler.seanmfrancis.net/contact.php or email thechroniclerbot@gmail.com with the following: 'addKeyword() Failed! ERROR 404: {id}_keywords QUERY: SELECT keyword FROM {id}_keywords WHERE keyword={word}'".format(id=message.channel.id, word=keywordValues[0].strip()))
		conn.close()
		return
	else:
		if rowCount == 0 and exists == True:
			lib.db.queryDatabase("INSERT INTO {id}_keywords (keyword,replacement) VALUES (\"{word}\", \"{replacement}\")".format(id=message.channel.id, word=keywordValues[0].strip(), replacement=keywordValues[1].strip()), connection=conn, checkExists=False, tablename="{id}_keywords".format(id=message.channel.id), commit=True)
		else:
			lib.db.queryDatabase("UPDATE {id}_keywords SET replacement=\"{replacement}\" WHERE keyword=\"{word}\";".format(id=message.channel.id, replacement=keywordValues[1].strip(), word=keywordValues[0].strip()), connection=conn, checkExists=False, tablename="{id}_keywords".format(id=message.channel.id), commit=True)
			
	conn.close()
	await lib.reaction.reactThumbsUp(message, client)

async def removeKeyword(message, client):
	value = message.content.replace('!c remove_keyword', '')
	
	conn = lib.db.connectToDatabase()
	
	rowCount, retval, exists = lib.db.queryDatabase("SELECT keyword FROM {id}_keywords WHERE keyword=\"{word}\"".format(id=message.channel.id, word=value.strip()), connection=conn, checkExists=True, tablename="{id}_keywords".format(id=message.channel.id), getResult=True)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler ran into an issue. Please use our contact form at chronicler.seanmfrancis.net/contact.php or email thechroniclerbot@gmail.com with the following: 'removeKeyword() Failed! ERROR 404: {id}_keywords QUERY: SELECT keyword FROM {id}_keywords WHERE keyword = {word}'".format(id=message.channel.id, word=value.strip()))
		conn.close()
		return
	else:
		if rowCount == 1:
			lib.db.queryDatabase("DELETE FROM {id}_keywords WHERE keyword=\"{word}\"".format(id=message.channel.id, word=value.strip()), connection=conn, checkExists=False, commit=True)
			await lib.reaction.reactThumbsUp(message, client)
		elif rowCount == 0:
			await lib.reaction.reactThumbsDown(message, client)
			await client.send_message(message.channel, "The Chronicler could not find the keyword in its database for this channel. Did you spell it correctly? If you are, make sure it is a keyword that was added to the Chronicle. If you are still having issues, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue.")

	conn.close()

#Gets the List of Keywords, if any, of the Story from the Database
#channel: The Channel to pull the Keywords from
#Returns: An tuple array of {keyword, replacement_string}
def getKeywords(channel):
	wordList = []
	rowCount, retval, exists = lib.db.queryDatabase("SELECT word,replacement FROM {id}_keywords".format(id=channel.id), checkExists=True, tablename="{id}_keywords".format(id=channel.id), getResult=True, closeConn=True)
	
	if rowCount == 0:
		return wordList
	else:
		i = 0
		while i < len(retval):
			combination = (retval[i], retval[i + 1])
			wordList.append(combination)
			print("Word: {word}\nReplacement: {replacement}".format(word=retval[i], replacement=retval[i + 1]))
			i = i + 2
		return wordList

#Searches through the String, replacing all instances of 'keyword' with 'replacement'
#string: The String to Search Through
#keyword: The string to replace
#replacement: The string to replace 'keyword' with
#Returns: The New String with all replacements made
def replaceKeyword(string, keyword, replacement):
	word = " {word} ".format(word=keyword)
	replace = " {replacement} ".format(replacement=replacement)
	if string.find(word) != -1:
		return string.replace(word, replace)
	elif string.find(" ") == -1:
		return string.replace(keyword, replacement)
	else:
		return string