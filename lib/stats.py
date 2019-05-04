import lib.db
import lib.reaction


async def displayChannelStats(client, message):
		"""
		Functions That Posts Various Channel Stats to the User

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM chronicles_info WHERE channel_id = {id}".format(
            id=str(message.channel.id)),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        getResult=True,
        commit=False,
        closeConn=True)
				
		if exists == False:
				await lib.reaction.reactThumbsDown(client, message)
				await lib.message.send(
            message.channel,
            "The Chronicler could not find the table. Please immediately either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue adding the following: ERROR 500: displayChannelStatus() QUERY: SELECT * FROM chronicles_info WHERE channel_id = {id}"
            .format(id=str(message.channel.id)), delete=False)
				return
    
		else:
				if rowCount == 0:
						await lib.message.send(
                message.channel,
                "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?"
            )
						
				else:
						if retval[2] == True:
								await lib.message.send(
                    message.channel,
                    "This channel has been blacklisted. You can no longer get its stats."
                )
								
						else:
								rowCount, contentData, exists = lib.db.queryDatabase(
                    "SELECT * FROM {id}_contents".format(
                        id=str(message.channel.id)),
                    client,
                    message.channel,
                    checkExists=True,
                    tablename="{id}_contents".format(id=str(message.channel.id)),
                    getResult=True,
                    closeConn=True)
										
								char_num = 0
								word_num = 0
								
								for row in contentData:
										char_num += row[2]
										word_num += row[3]
										
								messageStr = ('Stats for ' + message.channel.name + '\n\n'
                              '\tIs Closed = ' + str(retval[4]) + '\n'
                              '\tIs Private = ' + str(retval[3]) + '\n'
                              '\tChannel ID = ' + str(retval[1]) + '\n'
                              '\tChannel Creator = ' + str(retval[6]) + '\n'
                              '\tHas Warnings = ' + str(retval[7]) + '\n'
                              '\tWarning List = ' + str(retval[8]) + '\n'
                              '\tDate Last Modified = ' + str(retval[9]) + '\n'
                              '\tCharacter Count = ' + str(char_num) + '\n'
                              '\tWord Count = ' + str(word_num))
															
								await lib.message.send(message.channel, messageStr,delete=False)
								await lib.reaction.reactThumbsUp(client, message)


async def displayKeywords(client, message):
		"""
		Functions That Posts Various Keyword Related Stats to the User

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		message_list = {}
		message_list[0] = "List of Keywords and Replacements for This Channel:\n\n"
		word_list = lib.keywords.getKeywords(client, message.channel)
		
		i = 0
		
		for word in word_list:
				strToAdd = "\t* " + word[0] + " | " + word[1] + "\n"
				
				if (len(message_list[i]) + len(strToAdd) < 2000):
						message_list[i] += strToAdd
						
				elif (len(message_list[i]) + len(strToAdd) > 2000):
						message_list.add(strToAdd)
						i += 1
						
		for index in message_list:
				await lib.message.send(message.channel, message_list[index], delete=False)
				
		await lib.reaction.reactThumbsUp(client, message)


async def displaySymbols(client, message):
		"""
		Functions That Posts Various Symbol Related Stats to the User

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		message_list = {}
		message_list[0] = "List of Symbols Starts and Ends for This Channel:\n\n"
		
		symbol_list = lib.symbol.getSymbols(client, message.channel)
		
		i = 0
		
		for symbol in symbol_list:
				strToAdd = "\t* " + symbol[0] + " | " + symbol[1] + "\n"
				
				if (len(message_list[i]) + len(strToAdd) < 2000):
						message_list[i] += strToAdd
						
				elif (len(message_list[i]) + len(strToAdd) >= 2000):
						message_list.add(strToAdd)
						i += 1
						
		for index in message_list:
				await lib.message.send(message.channel, message_list[index], delete=False)
				
		await lib.reaction.reactThumbsUp(client, message)


async def displayAllStats(client, message):
		"""
		Functions That Posts All Channel Stats to the User

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		await displayChannelStats(client, message)
		
		await displayKeywords(client, message)
		
		await displaySymbols(client, message)