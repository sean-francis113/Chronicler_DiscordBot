import lib.reaction

async def addSymbol(message, client):
	value = message.content.replace('!c add_symbol ', '')
	symbolValues = value.split('|')
	
	conn = lib.db.connectToDatabase()
	
	rowCount, result, exists = lib.db.queryDatabase("SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(id=message.channel.id, start=symbolValues[0].strip()), connection=conn, checkExists=True, tablename="{id}_ignoredSymbols".format(id=message.channel.id), getResult=True, closeConn=False)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler ran into an issue. Please use our contact form at chronicler.seanmfrancis.net/contact.php or email thechroniclerbot@gmail.com with the following: 'addSymbol() Failed! ERROR 404: {id}_ignoredSymbols QUERY: SELECT start FROM {id}_ignoredSymbols WHERE start={start}'".format(id=message.channel.id, start=symbolValues[0].strip()))
		conn.close()
		return
	else:
		if rowCount == 0:
			lib.db.queryDatabase("INSERT INTO {id}_ignoredSymbols (start,end) VALUES (\"{start}\", \"{end}\")".format(id=message.channel.id, start=symbolValues[0].strip(), end=symbolValues[1].strip()), connection=conn, checkExists=False, tablename="{id}_ignoredSymbols".format(id=message.channel.id), commit=True, closeConn=True)
		else:
			lib.db.queryDatabase("UPDATE {id}_ignoredSymbols SET end=\"{end}\" WHERE start=\"{start}\"".format(id=message.channel.id, start=symbolValues[0].strip(), end=symbolValues[1].strip()), connection=conn, checkExists=False, tablename="{id}_ignoredSymbols".format(id=message.channel.id), commit=True, closeConn=True)

	await lib.reaction.reactThumbsUp(message, client)

async def removeSymbol(message, client):
	value = message.content.replace('!c remove_symbol', '')
	
	conn = lib.db.connectToDatabase()
	
	rowCount, retval, exists = lib.db.queryDatabase("SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(id=message.channel.id, start=value.strip()), connection=conn, checkExists=True, tablename="{id}_ignoredSymbols".format(id=message.channel.id), getResult=True, closeConn=False)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler ran into an issue. Please use our contact form at chronicler.seanmfrancis.net/contact.php or email thechroniclerbot@gmail.com with the following: 'removeSymbol() Failed! ERROR 404: {id}_ignoredSymbols QUERY: SELECT start FROM {id}_ignoredSymbols WHERE start = {start}'".format(id=message.channel.id, start=value.strip()))
		conn.close()
		return
	else:
		if rowCount == 1:
			lib.db.queryDatabase("DELETE FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(id=message.channel.id, start=value.strip()), connection=conn, checkExists=False, commit=True, closeConn=True)
			await lib.reaction.reactThumbsUp(message, client)
		elif rowCount == 0:
			await lib.reaction.reactThumbsDown(message, client)
			await client.send_message(message.channel, "The Chronicler could not find the symbol in its database for this channel. Did you type it correctly? If you are, make sure it is a keyword that was added to the Chronicle. If you are still having issues, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue.")

def pluckSymbols(start, end, string, removeInside=True):
	edittedString = string
	startIndex = string.find(start)
	if startIndex > -1:
		endIndex = string.find(end)
		if endIndex > startIndex:
			if removeInside == True:
				edittedString = string[:startIndex] + string[(endIndex + len(end)):]
			else:
					edittedString = string[:startIndex]+ string[(startIndex + len(start)):endIndex] + string[(endIndex + len(end)):]
	return ' '.join(edittedString.split())

def getSymbols(channel):
	symbolList = []
	rowCount, retval, exists = lib.db.queryDatabase("SELECT start,end FROM {id}_ignoredSymbols".format(id=channel.id), checkExists=True, tablename="{id}_ignoredSymbols".format(id=channel.id), getResult=True, closeConn=True)
	
	if rowCount == 0:
		return symbolList
	else:
		i = 0
		while i < len(retval):
			combination = (retval[0], retval[1])
			symbolList.append(combination)
			i = i + 2
		return symbolList