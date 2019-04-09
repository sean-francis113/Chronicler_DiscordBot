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
		editted_content = message.content
		print("String At Record Start: " + editted_content)
		
		editted_content = lib.symbol.replaceMarkdown(editted_content)
		print("String After Markdown: " + editted_content)
		
		word_list = lib.keywords.getKeywords(client, message.channel)
		symbol_list = lib.symbol.getSymbols(client, message.channel)
		
		for word in word_list:
				editted_content = lib.keywords.replaceKeyword(editted_content, word[0], word[1])

		print("String After Keywords: " + editted_content)																									
		for symbol in symbol_list:
				editted_content = lib.symbol.pluckSymbols(editted_content, symbol[0], symbol[1])

		print("String After Symbols: " + editted_content)

		charCount = 0

		#NEED TO GET ACCURATE CHARACTER/WORD COUNT BY LOOKING AT EVERYTHING NOT WITHIN SPAN TAGS!!!!
		while editted_content.find("<span class=") != -1:
				break
		
		print("Query String: INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{type}\', {char_count}, {word_count}, \"{entry_owner}\", \"{entry_editted}\", \"{entry_original}\")"
        .format(
            id=message.channel.id,
            type="In-Character",
            char_count=len(editted_content),
            word_count=len(editted_content.split(" ")),
            entry_owner=message.author.name,
            entry_editted=editted_content,
            entry_original=message.content))

		lib.db.queryDatabase(
        "INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')"
        .format(
            id=message.channel.id,
            type="In-Character",
            char_count=len(editted_content),
            word_count=len(editted_content.split(" ")),
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

		messagesChecked = 0
		async for curMessage in client.logs_from(
      	message.channel, before=lastMessageFound, limit=checkCount):

				messagesChecked += 1

				validUser = lib.validation.validateUser(client, curMessage)
				editted_content = ""
						
				if validUser == True and curMessage.content.startswith(
          	"!c") == False:
						editted_content = curMessage.content

						editted_content = lib.symbol.replaceMarkdown(editted_content)
								
						word_list = lib.keywords.getKeywords(client, message.channel)
						symbol_list = lib.symbol.getSymbols(client, message.channel)
								
						for word in word_list:
								editted_content = lib.keywords.replaceKeyword(
              	editted_content, word[0], word[1])
												
						for symbol in symbol_list:
								editted_content = lib.symbol.pluckSymbols(
              	editted_content, symbol[0], symbol[1])
												
						messageArray.append((curMessage, editted_content, curMessage.author))
						if messagesChecked == checkCount:
								lastMessageFound = curMessage
								if client.logs_from(
                   	message.channel, before=lastMessageFound, limit=checkCount):
									await startRewrite(client, message, conn, messageArray, lastMessageFound, checkCount)
					
						elif client.logs_from(
                   	message.channel, before=lastMessageFound, limit=checkCount) == None:
								return messageArray

		rowCount, result, exists = lib.db.queryDatabase(
     		"DELETE FROM {id}_contents".format(id=message.channel.id),
     		client,
     		message.channel,
     		connection=conn,
     		checkExists=True,
     		tablename="{id}_contents".format(id=message.channel.id),
     		commit=False,
     		closeConn=False)

		i = len(messageArray) - 1
		while i >= 0:
				lib.db.queryDatabase(
         		"INSERT INTO {id}_contents (entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')".format(
             		id=message.channel.id,
                type="In-Character",
                char_count=len(messageArray[i][1]),
                word_count=len(messageArray[i][1].split(" ")),
                entry_owner=messageArray[i][2].name,
                entry_editted=messageArray[i][1],
                entry_original=messageArray[i][0].content),
            client,
            messageArray[i][0].channel,
            connection=conn,
            checkExists=False,
            commit=False,
            closeConn=False)
				i -= 1
								
		conn.commit()
		conn.close()
		lib.db.updateModifiedTime(client, message.channel)