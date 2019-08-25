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
				
		channel_info = retval[0]
		
		if exists == False:
				await lib.reaction.reactThumbsDown(client, message)
				await lib.message.send(client, 
            message.channel,
            "The Chronicler could not find the table. Please immediately either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue adding the following: ERROR 500: displayChannelStatus() QUERY: SELECT * FROM chronicles_info WHERE channel_id = {id}"
            .format(id=str(message.channel.id)), delete=False)
				return
    
		else:
				if rowCount == 0:
						await lib.message.send(client, 
                message.channel,
                "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?",
								feedback=True
            )
						
				else:
						if channel_info[2] == True:
								await lib.message.send(client, 
                    message.channel,
                    "This channel has been blacklisted. You can no longer get its stats.",
										feedback=True
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
										char_num += row[4]
										word_num += row[5]

								has_warning_str = ""
								warning_list = ""
								closed_str = ""
								privacy_str = ""
								nsfw_str = ""

								if(channel_info[8] == False):
										has_warning_str = "False"
								else:
										has_warning_str = "True"

								if(channel_info[9] == ""):
										warning_list = "No Warnings Listed"
								else:
										warning_list = channel_info[9]

								if(channel_info[4] == False):
										closed_str = "False"
								else:
										closed_str = "True"

								if(channel_info[3] == "False"):
										privacy_str = "False"
								else:
										privacy_str = "True"
										
								if(channel_info[5] == "False"):
										nsfw_str = "False"
								else:
										nsfw_str = "True"

								messageStr = ('Stats for ' + message.channel.name + '\n\n'
															'\tChannel ID = ' + str(channel_info[1]) + '\n'
															'\tChannel Name = ' + str(channel_info[6]) + '\n'
                              '\tChannel Creator = ' + str(channel_info[7]) + '\n'
                              '\tIs Closed = ' + str(closed_str) + '\n'
                              '\tIs Private = ' + str(privacy_str) + '\n'
															'\tIs NSFW = ' + str(nsfw_str) + '\n'
                              '\tHas Warnings = ' + str(has_warning_str) + '\n'
                              '\tWarning List = ' + str(warning_list) + '\n'
                              '\tDate Last Modified = ' + str(channel_info[10]) + '\n'
                              '\tCharacter Count = ' + str(char_num) + '\n'
                              '\tWord Count = ' + str(word_num))
															
								await lib.message.send(client, message.channel, messageStr,delete=False)
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

		if(len(word_list) == 0):
				message_list[i] += "\tNo Keywords and Replacements"
		else:
				for word in word_list:
						strToAdd = "\t* " + word[0] + " | " + word[1] + "\n"
						
						if (len(message_list[i]) + len(strToAdd) < 2000):
								message_list[i] += strToAdd
								
						elif (len(message_list[i]) + len(strToAdd) > 2000):
								message_list.add(strToAdd)
								i += 1
						
		for index in message_list:
				await lib.message.send(client, message.channel, message_list[index], delete=False)
				
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

		if(len(symbol_list) == 0):
				message_list[0] += "\tNo Symbol Starts and Ends"
		
		for symbol in symbol_list:
				strToAdd = "\t* " + symbol[0] + " | " + symbol[1] + "\n"
				
				if (len(message_list[i]) + len(strToAdd) < 2000):
						message_list[i] += strToAdd
						
				elif (len(message_list[i]) + len(strToAdd) >= 2000):
						message_list.add(strToAdd)
						i += 1
						
		for index in message_list:
				await lib.message.send(client, message.channel, message_list[index], delete=False)
				
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