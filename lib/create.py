import discord
import datetime
import lib.db
import lib.h
import lib.w
import lib.record
import lib.reaction

async def createChroniclerChannel(message, client, createNew=True):
	#Initialize Variables
	isPrivate = False
	dict_word_keys = ['word', 'replacement']
	keywords = []
	hasWarnings = False
	warnings = ''
	dict_user_keys = ['name', 'id']
	ignoredUsers = []
	channelName = message.author.name + '\'s Chronicle'
	everyone_perms = discord.PermissionOverwrite(
		create_instant_invite=False, 
		manage_channels=False, 
		manage_permissions=False, 
		manage_webhooks=False, 
		read_message_history=True, 
		read_messages=True, 
		send_messages=False, 
		manage_messages=False, 
		send_tts_messages=False, 
		embed_links=False, 
		attach_files=False, 
		mention_everyone=False
		)
	user_perms = discord.PermissionOverwrite(
		create_instant_invite=True, 
			manage_channels=True, 
			manage_permissions=True, 
			manage_webhooks=True, 
			read_message_history=True, 
			read_messages=True,
			send_messages=True, 
			manage_messages=True, 
			send_tts_messages=True, 
			embed_links=True, 
			attach_files=True, 
			mention_everyone=True
			)
	showWelcomeMessage = True
	showHelpMessage = True
	willRewrite = False

	#Parse out options, if any
	channelOptionsStr = message.content.replace('!c create_channel ', '')
	if(channelOptionsStr.find('=') != -1):
		channelOptionsStr = channelOptionsStr.replace('; ', ';')
		channelOptionsArr = channelOptionsStr.split(';')
	for option in channelOptionsArr:
		if(option.startswith('channelName=') and createNew==True):
			value = option.replace('channelName=', '')
			channelName = value
		if(option.startswith('isPrivate=')):
			value = option.replace('isPrivate=', '')
			value = value.lower()
			if(value.find('true') != -1):
				isPrivate = True
		elif(option.startswith('keyword=')):
			value = option.replace('keyword=', '')
			keywordValues = value.split('|')
			finalCombination = [keywordValues[0].strip(), keywordValues[1].strip()]
			keywords.append(dict(zip(dict_word_keys, finalCombination)))
		elif(option.startswith('warnings=')):
			value = option.replace('warnings=', '')
			warnings = value
		elif(option.startswith('ignoreUsers=')):
			value = option.replace('ignoreUsers=', '')
			usersFound = value.split('|')
			usersInServer = client.get_all_members()
			for user in usersFound:
				strippedUser = user.strip()
				for serverUser in usersInServer:
					if serverUser.nick == strippedUser:
						combination = [serverUser.nick, serverUser.id]
						ignoredUsers.append(dict(zip(dict_user_keys, combination)))
					elif serverUser.name == strippedUser:
						combination = [serverUser.name, serverUser.id]
						ignoredUsers.append(dict(zip(dict_user_keys, combination)))
		elif(option.startswith('soleOwnership=') and createNew==True):
			value = option.replace('soleOwnership=', '')
			value = value.lower()
			if(value.find('false') != -1):
				everyone_perms = discord.PermissionOverwrite(create_instant_invite=True, 
				manage_channels=True, 
				manage_permissions=True, 
				manage_webhooks=True, 
				read_message_history=True, 
				read_messages=True,
				send_messages=True, 
				manage_messages=True, 
				send_tts_messages=True, 
				embed_links=True, 
				attach_files=True, 
				mention_everyone=True
				)
		elif(option.startswith('showWelcome=')):
			value = option.replace('showWelcome=', '')
			value = value.lower()
			if(value.find('false') != -1):
				showWelcomeMessage = False
		elif(option.startswith('showHelp=')):
			value = option.replace('showHelp=', '')
			value = value.lower()
			if(value.find('false') != -1):
				showHelpMessage = False
		elif(option.startswith('rewrite=') and createNew==False):
			value = option.replace('rewrite=', '')
			lowerValue = value.lower()
			if lowerValue.strip() == 'true':
				willRewrite = True

	#Create Channel Permissions
	everyone = discord.ChannelPermissions(target=message.server.default_role, overwrite=everyone_perms)
	channelCreator = discord.ChannelPermissions(target=message.author, overwrite=user_perms)
	chronicler = discord.ChannelPermissions(target=client.user, overwrite=user_perms)

	chroniclerChannel = None

	if createNew == True:
		#Create the New Channel
		chroniclerChannel = await client.create_channel(message.server, channelName, everyone, channelCreator, chronicler)
	else:
		chroniclerChannel = message.channel

	#Connect to Database
	#Need connection for Future Executions
	conn = lib.db.connectToDatabase()

	#Create Channel Tables
	lib.db.queryDatabase("CREATE TABLE {id}_contents (entry_id INT AUTO_INCREMENT PRIMARY KEY, entry_type VARCHAR(255) NOT NULL DEFAULT(\"In-Character\"), char_count INT NOT NULL, word_count INT NOT NULL, entry_owner TEXT, entry_editted MEDIUMTEXT, entry_original MEDIUMTEXT)".format(id=chroniclerChannel.id), connection=conn, checkExists=False, closeConn=False)
	lib.db.queryDatabase("CREATE TABLE {id}_keywords (kw_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, word TEXT NOT NULL, replacement TEXT NOT NULL)".format(id=chroniclerChannel.id), checkExists=False, closeConn=False)
	lib.db.queryDatabase("CREATE TABLE {id}_ignoredUsers (iu_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, name TEXT NOT NULL, id TEXT NOT NULL)".format(id=chroniclerChannel.id), checkExists=False, closeConn=False)
	lib.db.queryDatabase("CREATE TABLE {id}_ignoredSymbols (is_id INT AUTO_INCREMENT PRIMARY KEY, start VARCHAR(50) NOT NULL, end VARCHAR(50) NOT NULL)".format(id=chroniclerChannel.id), checkExists=False, closeConn=False)
  
	#Add New Channel Into chronicles_info
	lib.db.queryDatabase("INSERT INTO chronicles_info (channel_id, is_blacklisted, is_private, is_closed, channel_name, channel_owner, has_warnings, warning_list, date_last_modified) VALUES (\"{id}\", FALSE, {private}, FALSE, \"{name}\", \"{owner}\", {has_warn}, \"{warn_list}\", \"{datetime}\")".format(id=chroniclerChannel.id, private=str(isPrivate).upper(), name=channelName, owner=message.author.name, has_warn=str(hasWarnings).upper(), warn_list=warnings, datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), checkExists=True, tablename="chronicles_info", commit=True, closeConn=False)

	#Add Any Specified Keywords
	if(len(keywords) > 0):
		for index in keywords:
			lib.db.queryDatabase("INSERT INTO {id}_keywords (word, replacement) VALUES ({word}, {replacement})".format(id=chroniclerChannel.id, word=index['word'], replacement=index['replacement']), connection=conn, checkExists=True, tablename="{id}_ignoredUsers".format(id=chroniclerChannel.id), commit=False, closeConn=False)
		conn.commit()

	#Add Any Specified Users to Ignore
	if(len(ignoredUsers) > 0):
		for index in ignoredUsers:
			lib.db.queryDatabase("INSERT INTO {channel_id}_ignoredUsers (name, id) VALUES ({user_name}, {user_id})".format(channel_id=chroniclerChannel.id, user_name=index['name'], user_id=index['id']), connection=conn, checkExists=True, tablename="{id}_ignoredUsers".format(id=chroniclerChannel.id), commit=False, closeConn=False)
		conn.commit()

	#Send Welcome and Help Messages into New Channel
	if(showWelcomeMessage == True or showHelpMessage == True):
		openingMessage = await client.send_message(chroniclerChannel, 'Welcome to your new channel!')
		if(showWelcomeMessage == True):
			await lib.w.showWelcome(openingMessage, client)
		if(showHelpMessage == True):
			await lib.h.showHelp(openingMessage, client)

	#Rewrite the Chroncile if User Wishes
	if willRewrite == True:
		await lib.record.startRewrite(message, client)

	conn.cursor().close()
	conn.close()

	#Tell User We Are Done
	await lib.reaction.reactThumbsUp(message, client)