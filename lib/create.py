#Import Statements
import discord
import datetime
import lib.db
import lib.h
import lib.w
import lib.record
import lib.reaction
import commandList as cmd


async def createChroniclerChannel(client, message, createNew=True):
		"""
		Function That Creates a New Channel Both in the Discord Server and the Database, Using Different Values (Provided or Default) to Customize the Channel.

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Sent the Command
				createNew (boolean, OPTIONAL)
						Flag to Determine if a Channel Should be Created in the Discord Server
		"""

		#Initialize Variables
		isPrivate = False
		isNSFW = False
		dict_word_keys = ['word', 'replacement']
		keywords = []
		hasWarnings = False
		warnings = ''
		dict_user_keys = ['name', 'id']
		ignoredUsers = []
		dict_symbol_keys = ['start', 'end']
		ignoredSymbols = []
		channelName = message.author.name + '\'s Chronicle'
		everyone_perms = discord.PermissionOverwrite(
        create_instant_invite=False,
        manage_channels=False,
        manage_webhooks=False,
        read_message_history=True,
        read_messages=True,
        send_messages=False,
        manage_messages=False,
        send_tts_messages=False,
        embed_links=False,
        attach_files=False,
        mention_everyone=False)
		user_perms = discord.PermissionOverwrite(
        create_instant_invite=True,
        manage_channels=True,
        manage_webhooks=True,
        read_message_history=True,
        read_messages=True,
        send_messages=True,
        manage_messages=True,
        send_tts_messages=True,
        embed_links=True,
        attach_files=True,
        mention_everyone=True)
		bot_perms = discord.PermissionOverwrite(
				administrator=True)
		showWelcomeMessage = True
		showHelpMessage = True
		willRewrite = False

		if(createNew is False):			
			check_result = lib.db.checkIfDataExists(client, message.channel, "chronicles_info", channel_id=message.channel.id)

			if(int(check_result["channel_id"]) > 0):

					#Show Player That The Chronicler Was Unsuccessful
					await lib.reaction.reactThumbsDown(client, message)

					lib.error.postError(client, message.channel, "This Channel's ID is already in the Chronicler's Database.")

					return
		
		#Parse out options, if any
		channelOptionsStr = message.content.replace(
        cmd.create_channel["command"], '')
		channelOptionsStr = channelOptionsStr.replace(
        cmd.whitelist_channel["command"], '')
		channelOptionsStr = channelOptionsStr.strip()

		#Array of Channel Options Provided by the User
		channelOptionsArr = []

		#Grab All Channel Options if Any Have Been Provided
		if (channelOptionsStr.find('=') != -1):
				channelOptionsStr = channelOptionsStr.replace('; ', ';')
				channelOptionsArr = channelOptionsStr.split(';')

		#Look Through All of the Options Provided, if Any
		for option in channelOptionsArr:

				#If a Channel Name Has Been Provided
				if (option.startswith('channel_name=') and createNew == True):
						value = option.replace('channel_name=', '')
						channelName = value.strip()

				#If the Private Flag Has Been Provided
				elif (option.startswith('is_private=')):
						value = option.replace('is_private=', '')
						value = value.lower()
						if (value.find('true') != -1):
								isPrivate = True

				#If the NSFW Flag Has Been Provided
				elif (option.startswith('is_nsfw=')):
						value = option.replace('is_nsfw=', '')
						value = value.lower()
						if (value.find('true') != -1):
								isNSFW = True

				#If Keywords Have Been Provided
				elif (option.startswith('keyword=')):
						value = option.replace('keyword=', '')
						keywordValues = value.split('|')
						finalCombination = [
                keywordValues[0].strip(), keywordValues[1].strip()
            ]
						keywords.append(dict(zip(dict_word_keys, finalCombination)))

				#If Warnings Have Been Provided
				elif (option.startswith('warnings=')):
						value = option.replace('warnings=', '')
						warnings = value

				#If Users to Ignore Have Been Provided
				elif (option.startswith('ignore_users=')):
						value = option.replace('ignore_users=', '')
						usersFound = value.split('|')
						usersInServer = client.get_all_members()
						for user in usersFound:
								strippedUser = user.strip()
								for serverUser in usersInServer:
										if serverUser.nick == strippedUser:
												combination = [serverUser.nick, serverUser.id]
												ignoredUsers.append(
                            dict(zip(dict_user_keys, combination)))
										elif serverUser.name == strippedUser:
												combination = [serverUser.name, serverUser.id]
												ignoredUsers.append(
                            dict(zip(dict_user_keys, combination)))

				#If Symbols to Ignore Have Been Provided
				elif (option.startswith('ignore_symbols=')):
						value = option.replace('ignore_symbols=', '')
						symbolCombination = value.split(';')
						for symbol in symbolCombination:
								symbolArr = symbol.split('|')
								ignoredSymbols.append(
                    dict(zip(dict_symbol_keys, [symbolArr[0], symbolArr[1]])))

				#If the Sole Ownership Flag Has Been Provided (Only Works if the Create New Flag is On)
				elif (option.startswith('sole_ownership=') and createNew == True):
						value = option.replace('sole_ownership=', '')
						value = value.lower()
						if (value.find('false') != -1):
								everyone_perms = discord.PermissionOverwrite(
                    create_instant_invite=True,
                    manage_channels=True,
                    manage_webhooks=True,
                    read_message_history=True,
                    read_messages=True,
                    send_messages=True,
                    manage_messages=True,
                    send_tts_messages=True,
                    embed_links=True,
                    attach_files=True,
                    mention_everyone=True)

				#If the Show Welcome Flag Has Been Provided
				elif (option.startswith('show_welcome=')):
						value = option.replace('show_welcome=', '')
						value = value.lower()
						if (value.find('false') != -1):
								showWelcomeMessage = False

				#If the Show Help Flag Has Been Provided
				elif (option.startswith('show_help=')):
						value = option.replace('show_help=', '')
						value = value.lower()
						if (value.find('false') != -1):
								showHelpMessage = False

				#If the Rewrite Flag Has Been Provided (Only Works if the Create New Flag is Off)
				elif (option.startswith('rewrite=') and createNew == False):
						value = option.replace('rewrite=', '')
						lowerValue = value.lower()
						if lowerValue.strip() == 'true':
								willRewrite = True
								
		#The Newly Created Channel
		chroniclerChannel = None
		
		#If We Are Creating a New Channel in Discord
		if createNew == True:
        #Create the New Channel
				chroniclerChannel = await message.channel.guild.create_text_channel(channelName, nsfw=isNSFW)

		#Otherwise		
		else:
				channelName = message.channel.name
				chroniclerChannel = message.channel
				await chroniclerChannel.edit(nsfw=isNSFW)

		#Set Channel Permissions
		await chroniclerChannel.set_permissions(message.channel.guild.default_role, overwrite=everyone_perms)
		await chroniclerChannel.set_permissions(message.author, overwrite=user_perms)
		await chroniclerChannel.set_permissions(client.user, overwrite=bot_perms)
		
		#Connect to Database
		conn = lib.db.connectToDatabase()
		
		#Create Channel Tables
		lib.db.queryDatabase(
        "CREATE TABLE {id}_contents (entry_id INT AUTO_INCREMENT PRIMARY KEY, message_id TEXT NOT NULL, is_pinned BOOLEAN DEFAULT(FALSE) NOT NULL, entry_type VARCHAR(255) NOT NULL DEFAULT(\"In-Character\"), char_count INT NOT NULL, word_count INT NOT NULL, entry_owner TEXT, entry_editted MEDIUMTEXT, entry_original MEDIUMTEXT)"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="{id}_contents".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "ALTER TABLE {id}_contents CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="{id}_contents".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "CREATE TABLE {id}_keywords (kw_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, word TEXT NOT NULL, replacement TEXT NOT NULL)"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
				tablename="{id}_keywords".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "ALTER TABLE {id}_keywords CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="{id}_keywords".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "CREATE TABLE {id}_ignoredUsers (iu_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, name TEXT NOT NULL, id TEXT NOT NULL)"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
				tablename="{id}_ignoredUsers".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "ALTER TABLE {id}_ignoredUsers CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="{id}_ignoredUsers".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "CREATE TABLE {id}_ignoredSymbols (is_id INT AUTO_INCREMENT PRIMARY KEY, start VARCHAR(50) NOT NULL, end VARCHAR(50) NOT NULL)"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
				tablename="{id}_ignoredSymbols".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
		lib.db.queryDatabase(
        "ALTER TABLE {id}_ignoredSymbols CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        .format(id=str(chroniclerChannel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="{id}_ignoredSymbols".format(id=str(chroniclerChannel.id)),
				ignoreExistance=True,
        closeConn=False)
				
		#Add New Channel Into chronicles_info
		lib.db.queryDatabase(
        "INSERT INTO chronicles_info (channel_id, is_blacklisted, is_private, is_closed, is_NSFW, channel_name, channel_owner, has_warnings, warning_list, date_last_modified) VALUES (\"{id}\", FALSE, {private}, FALSE, {NSFW}, \"{name}\", \"{owner}\", {has_warn}, \"{warn_list}\", \"{datetime}\")"
        .format(
            id=str(chroniclerChannel.id),
            private=str(isPrivate).upper(),
						NSFW=str(isNSFW).upper(),
            name=channelName,
            owner=message.author.name,
            has_warn=str(hasWarnings).upper(),
            warn_list=warnings,
            datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        client,
        message.channel,tablename="chronicles_info",
        commit=True,
        closeConn=False)

    #Add Any Specified Keywords
		if (len(keywords) > 0):
				for index in keywords:
					lib.db.queryDatabase(
                "INSERT INTO {id}_keywords (word, replacement) VALUES (\"{word}\", \"{replacement}\")"
                .format(
                    id=str(chroniclerChannel.id),
                    word=index['word'],
                    replacement=index['replacement']),
                client,
                message.channel,
                connection=conn,
								tablename="{id}_keywords".format(id=str(chroniclerChannel.id)),
                commit=False,
                closeConn=False)
					conn.commit()

    #Add Any Specified Users to Ignore
		if (len(ignoredUsers) > 0):
				for index in ignoredUsers:
						lib.db.queryDatabase(
                "INSERT INTO {channel_id}_ignoredUsers (name, id) VALUES (\"{user_name}\", \"{user_id}\")"
                .format(
                    channel_id=str(chroniclerChannel.id),
                    user_name=index['name'],
                    user_id=index['id']),
                client,
                message.channel,
                connection=conn,
								tablename="{id}_ignoredUsers".format(id=str(chroniclerChannel.id)),
                commit=False,
                closeConn=False)
				conn.commit()

    #Add Any Specified Symbols to Ignore
		if (len(ignoredSymbols) > 0):
				for index in ignoredSymbols:
						lib.db.queryDatabase(
                "INSERT INTO {id}_ignoredSymbols (start,end) VALUES (\"{start}\", \"{end}\")"
                .format(
                    id=str(chroniclerChannel.id),
                    start=index['start'],
                    end=index['end']),
                client,
                message.channel,
                connection=conn,
								tablename="{id}_ignoredSymbols".format(
                    id=str(chroniclerChannel.id)),
                commit=False,
                closeConn=False)
				conn.commit()

		#Send Welcome Message
		openingMessage = await lib.message.send(client, chroniclerChannel, "Welcome to your new channel!", delete=False)

    #Send Welcome and Help Messages into New Channel
		if (showWelcomeMessage == True):
				await lib.w.showWelcome(client, openingMessage)
		if (showHelpMessage == True):
				await lib.h.showHelp(client, openingMessage)

    #Rewrite the Chroncile if User Wishes
		if willRewrite == True:
				await lib.record.startRewrite(client, message)
		
		#Close Database Connection
		conn.cursor().close()
		conn.close()

    #Tell User We Are Done
		await lib.reaction.reactThumbsUp(client, message)