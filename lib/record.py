import lib.keywords
import lib.symbol
import lib.db
import lib.reaction
import lib.log


async def postToDatabase(client, message):
		"""
		Function That Posts the Provided Message Into the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to Post
		"""
		
		original_content = message.content
		
		editted_content = message.content
		
		word_list = lib.keywords.getKeywords(client, message.channel)
		symbol_list = lib.symbol.getSymbols(client, message.channel)
		
		for word in word_list:
				editted_content = lib.keywords.replaceKeyword(editted_content, word[0],
                                                      word[1])
																											
		for symbol in symbol_list:
				editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0],
                                                  symbol[1])
																									
		editted_content = lib.symbol.replaceMarkdown(editted_content)
		
		taglessStr = editted_content
		
		while taglessStr.find("<span class=") != -1:
				startIndex = taglessStr.find("<span class=")
				midIndex = taglessStr.find(">", startIndex)
				endIndex = taglessStr.find("</span>", midIndex)
				
				if startIndex != -1 and midIndex != -1 and endIndex != -1:
						taglessStr = taglessStr[:startIndex] + taglessStr[
                midIndex:endIndex] + taglessStr[endIndex + len("</span>"):]

		#Handle Curly Quotes
		original_content = original_content.replace('“','"').replace('”','"')
		original_content = original_content.replace("‘","'").replace("’","'")
		editted_content = editted_content.replace('“','"').replace('”','"')
		editted_content = editted_content.replace("‘","'").replace("’","'")

    #Keep Any Quotes in the Message
		original_content = original_content.replace("'", "\\'")
		editted_content = editted_content.replace("'", "\\'")
		
		lib.db.queryDatabase(
        "INSERT INTO {id}_contents (message_id, is_pinned, entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{message_id}\', {pinned}, \'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')"
        .format(
            id=str(message.channel.id),
            message_id=str(message.id),
            pinned=str(message.pinned).upper(),
            type="In-Character",
            char_count=len(taglessStr),
            word_count=len(taglessStr.split(" ")),
            entry_owner=message.author.name,
            entry_editted=editted_content,
            entry_original=original_content),
        client,
        message.channel,
        checkExists=True,
        tablename="{id}_contents".format(id=str(message.channel.id)),
        commit=True,
        closeConn=True)
				
		lib.db.updateModifiedTime(client, message.channel)
		
		await lib.reaction.reactThumbsUp(client, message)


#Rewrite the Whole Chronicle From the Beginning
async def startRewrite(client,
                       message,
                       connection=None,
                       messageArray=[],
                       lastMessageFound=None,
                       checkCount=500):
		"""
		Function that Starts, or Continues, Rewriting the Channel's Messages

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Rewrite Command
				connection (pymysql.connections.Connection, OPTIONAL)
						The Connection to the Database. Will Be Created if Not Provided
				messageArray (Array, OPTIONAL)
						The Array of Messages Found. Will Add Onto This Array if Provided
				lastMessageFound (discord.Message, OPTIONAL)
						The Last Message Found in the Rewrite Process. Will Start Searching for Messages From This One if Provided.
				checkCount (integer, OPTIONAL)
						How Many Messages to Search For At a Time.
		"""
		
		conn = None
		
		if connection == None:
				conn = lib.db.connectToDatabase()
		else:
				conn = connection
				
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM {id}_contents".format(id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_contents".format(id=str(message.channel.id)),
        commit=False,
        closeConn=False)
		
		if exists == False:
				lib.reaction.reactThumbsDown(client, message)
				lib.message.send(
            message.channel,
            "The Chronicler could not find this channel in it's database. Has this channel been Whitelisted?"
            .format(id=str(message.channel.id)))
				return
				
		if len(messageArray) == 0 or messageArray == None:
				messageArray = await message.channel.history(
            after=lastMessageFound, limit=checkCount,
            oldest_first=True).flatten()
		else:
				newArray = await message.channel.history(
            after=lastMessageFound, limit=checkCount,
            oldest_first=True).flatten()
				messageArray.extend(newArray)
				
		lastMessage = messageArray[-1]
		testArray = await message.channel.history(
        after=lastMessage, limit=checkCount, oldest_first=True).flatten()
				
		if len(testArray) > 0:
				await startRewrite(
            client,
            message,
            connection=conn,
            messageArray=messageArray,
            lastMessageFound=lastMessage,
            checkCount=checkCount)
				return

    #Once We Have All Messages, Work to Grab Data and Edit Content as Needed
		contentArray = []
		messageNum = 1
		for message in messageArray:
				validUser = lib.validation.validateUser(client, message)
				if validUser == True and message.content.startswith("!c") == False:
						original_content = message.content
						editted_content = message.content
						
						word_list = lib.keywords.getKeywords(client, message.channel)
						symbol_list = lib.symbol.getSymbols(client, message.channel)
						
						for word in word_list:
								editted_content = lib.keywords.replaceKeyword(
                    editted_content, word[0], word[1])
										
						for symbol in symbol_list:
								editted_content = lib.symbol.pluckSymbols(
                    editted_content, symbol[0], symbol[1])
										
						editted_content = lib.symbol.replaceMarkdown(editted_content)

						#Handle Curly Quotes
						original_content = original_content.replace('“','"').replace('”','"')
						original_content = original_content.replace("‘","'").replace("’","'")
						editted_content = editted_content.replace('“','"').replace('”','"')
						editted_content = editted_content.replace("‘","'").replace("’","'")

						#Keep Any Quotes in the Message
						original_content = original_content.replace("'", "\\'")
						editted_content = editted_content.replace("'", "\\'")
						
						if editted_content != "":
								contentArray.append((message, original_content, editted_content, message.author))
								
						messageNum += 1
										
		rowCount, result, exists = lib.db.queryDatabase(
        "DELETE FROM {id}_contents".format(id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_contents".format(id=str(message.channel.id)),
        commit=False,
        closeConn=False)
				
		for content in contentArray:
				if content != None:
						lib.db.queryDatabase(
								"INSERT INTO {id}_contents (message_id, is_pinned, entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{message_id}\', {pinned}, \'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')"
								.format(
										id=str(message.channel.id),
										message_id=str(content[0].id),
										pinned=str(content[0].pinned).upper(),
										type="In-Character",
										char_count=len(content[2]),
										word_count=len(content[2].split(" ")),
										entry_owner=content[3].name,
										entry_editted=content[2],
										entry_original=content[1]),
								client,
								content[0].channel,
								connection=conn,
								checkExists=False,
								commit=False,
								closeConn=False)
				
		conn.commit()
		conn.close()
		lib.db.updateModifiedTime(client, message.channel)
