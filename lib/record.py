import lib.keywords
import lib.symbol
import lib.db
import lib.reaction
import lib.log
import asyncio


#Posts the message into the database
#message: The message to post
#client: The bot's client
async def postToDatabase(client, message):
		
		word_list = lib.keywords.getKeywords(client, message.channel)
		symbol_list = lib.symbol.getSymbols(client, message.channel)
		
		for word in word_list:
				editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])

		for symbol in symbol_list:
				editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0], symbol[1])

		editted_content = lib.symbol.replaceMarkdown(editted_content)
		taglessStr = editted_content

		while taglessStr.find("<span class=") != -1:
				startIndex = taglessStr.find("<span class=")
				midIndex = taglessStr.find(">", startIndex)
				endIndex = taglessStr.find("</span>", midIndex)
				
				if startIndex != -1 and midIndex != -1 and endIndex != -1:
						taglessStr = taglessStr[ : startIndex] + taglessStr[midIndex : endIndex] + taglessStr[endIndex + len("</span>") : ]

		lib.db.queryDatabase(
        "INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')"
        .format(
            id=message.channel.id,
            type="In-Character",
            char_count=len(taglessStr),
            word_count=len(taglessStr.split(" ")),
            entry_owner=message.author.name,
            entry_editted=editted_content,
            entry_original=message.content),
        client,
        message.channel,
        checkExists=True,
        tablename="{id}_contents".format(id=message.channel.id),
        commit=True,
        closeConn=True)
				
		lib.db.updateModifiedTime(client, message.channel)
		
		await lib.reaction.reactThumbsUp(client, message)


#Rewrite the Whole Chronicle Frm the Beginning
async def startRewrite(client,
												message,
                      	connection=None,
                       	messageArray=[],
                       	lastMessageFound=None,
												checkCount=500):
												
		conn = None

		if connection == None:
				conn = lib.db.connectToDatabase()
		else:
				conn = connection

		rowCount, retval, exists = lib.db.queryDatabase(
				"SELECT * FROM {id}_contents".format(id=message.channel.id), 
				client, 
				message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_contents".format(id=message.channel.id),
        commit=False,
        closeConn=False)
		
		if exists == False:
				lib.reaction.reactThumbsDown(client, message)
				lib.message.semd(
          	message.channel,
            "The Chronicler could not find this channel in it's database. Has this channel been Whitelisted?"
            .format(id=message.channel.id))
				return

		if len(messageArray) == 0 or messageArray == None:
				messageArray = await message.channel.history(after=lastMessageFound, limit=checkCount, oldest_first=True).flatten()
				print(len(messageArray))
		else:
				newArray = await message.channel.history(after=lastMessageFound, limit=checkCount, oldest_first=True).flatten()
				messageArray.extend(newArray)
				print(len(messageArray))

		lastMessage = messageArray[-1]
		testArray = await message.channel.history(after=lastMessage, limit=checkCount, oldest_first=True).flatten()

		if len(testArray) > 0:
				print("Continuing Rewrite")
				await startRewrite(client, message, connection=conn, messageArray=messageArray, lastMessageFound=lastMessage, checkCount=checkCount)
				return

		#Once We Have All Messages, Work to Grab Data and Edit Content as Needed
		print(len(messageArray))
		contentArray = []
		messageNum = 1
		for message in messageArray:
				validUser = lib.validation.validateUser(client, message)
				if validUser == True and message.content.startswith("!c") == False:
						editted_content = message.content
						print(messageNum)
						editted_content = message.content
						print(editted_content)

						word_list = lib.keywords.getKeywords(client, message.channel)
						symbol_list = lib.symbol.getSymbols(client, message.channel)
								
						for word in word_list:
								editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])
												
						for symbol in symbol_list:
								editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0], symbol[1])

						editted_content = lib.symbol.replaceMarkdown(editted_content)

						if editted_content != "":
							contentArray.append((message, editted_content, message.author))

						messageNum += 1 

		rowCount, result, exists = lib.db.queryDatabase(
     		"DELETE FROM {id}_contents".format(id=message.channel.id),
     		client,
     		message.channel,
     		connection=conn,
     		checkExists=True,
     		tablename="{id}_contents".format(id=message.channel.id),
     		commit=False,
     		closeConn=False)

		i = 0
		while i < len(contentArray):
				print(i)
				lib.db.queryDatabase(
         		"INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')".format(
             		id=message.channel.id,
                type="In-Character",
                char_count=len(contentArray[i][1]),
                word_count=len(contentArray[i][1].split(" ")),
                entry_owner=contentArray[i][2].name,
                entry_editted=contentArray[i][1],
                entry_original=contentArray[i][0].content),
            client,
            contentArray[i][0].channel,
            connection=conn,
            checkExists=False,
            commit=False,
            closeConn=False)
				i += 1
								
		conn.commit()
		conn.close()
		lib.db.updateModifiedTime(client, message.channel)