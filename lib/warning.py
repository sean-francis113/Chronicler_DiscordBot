import lib.db
import lib.reaction
import commandList as cmd


async def setWarnings(client, message):
    """
		Functions That Resets the Warning List in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""

    value = message.content.replace(cmd.set_warning["command"], '')

    #Connect to Database
    conn = lib.db.connectToDatabase()

    if value.strip() == '':
        lib.db.queryDatabase(
            "UPDATE chronicles_info SET has_warnings=FALSE WHERE channel_id=\"{id}\";"
            .format(id=str(message.channel.id)),
            client,
            message.channel,
            connection=conn,
						tablename="chronicles_info",
            commit=True,
            closeConn=False)

    else:
        lib.db.queryDatabase(
            "UPDATE chronicles_info SET has_warnings=TRUE WHERE channel_id=\"{id}\";"
            .format(id=str(message.channel.id)),
            client,
            message.channel,
            connection=conn,
						tablename="chronicles_info",
            commit=True,
            closeConn=False)

    lib.db.queryDatabase(
        "UPDATE chronicles_info SET warning_list=\"{list}\" WHERE channel_id=\"{id}\";"
        .format(list=value.strip(), id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)

    await lib.reaction.reactThumbsUp(client, message)
		
async def addWarning(client, message):
		"""
		Functions That Adds a Warning to the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		value = message.content.replace(cmd.add_warning["command"], '')

		print(value)
		print(message.content.replace
		(cmd.add_warning["command"], ''))

		#Connect to Database
		conn = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM chronicles_info WHERE channel_id=\"{id}\"".format(
            id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="chronicles_info",
        commit=False,
        getResult=True,
        closeConn=False)
				
		addition = ''
		
		channel_info = retval[0]
		
		# 9 = Warning List
		if channel_info[9].endswith(', ') or channel_info[9] == '':
				addition = value.strip()
		elif channel_info[9].endswith(','):
				addition = ' ' + value.strip()
		else:
				addition = ', ' + value.strip()
				
		lib.db.queryDatabase(
        "UPDATE chronicles_info SET has_warnings=TRUE WHERE channel_id=\"{id}\""
        .format(id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
        tablename="chronicles_info",
        commit=False,
        closeConn=False)
				
		lib.db.queryDatabase(
        "UPDATE chronicles_info SET warning_list=CONCAT(IFNULL(warning_list, \"\"), \"{add}\")"
        .format(add=addition.strip()),
        client,
        message.channel,
        connection=conn,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)
				
		await lib.reaction.reactThumbsUp(client, message)


async def removeWarning(client, message):
		"""
		Functions That Posts Removes a Warning From the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		value = message.content.replace(cmd.remove_warning["command"] + ' ', '')

    #Connect to Database
		conn = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM chronicles_info WHERE channel_id=\"{id}\"".format(
            id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="chronicles_info",
        commit=False,
        getResult=True,
        closeConn=False)

		channel_info = retval[0]
				
		warningList = channel_info[9]
		index = warningList.find(value)
		
		if index != -1:
        #Need to Check for Comma
				endOfWord = (index + len(value.strip())) - 1
				finalList = ''
				
				if endOfWord >= len(warningList):
						#Show Player That The Chronicler Was Unsuccessful
						await lib.reaction.reactThumbsDown(client, message)

						lib.error.postError(
                client, message.channel,
                'ERROR: Internal Error with Removing Warning.')
						return
						
				if warningList[endOfWord + 1] == ',' and warningList[index - 2] != ',':
						finalList = warningList.replace((value + ', '), '')
				
				elif warningList[endOfWord + 1] != ',' and warningList[index - 2] == ',':
						finalList = warningList.replace((', ' + value), '')
				
				elif warningList[endOfWord + 1] == ',' and warningList[index - 2] == ',':
						finalList = warningList.replace((', ' + value + ', '), '')
        
				else:
						finalList = warningList.replace(value, '')
						
				if finalList.strip() == '':
						lib.db.queryDatabase(
                "UPDATE chronicles_info SET has_warnings = FALSE WHERE channel_id=\"{id}\""
                .format(id=str(message.channel.id)),
                client,
                message.channel,
                connection=conn,
                tablename="chronicles_info",
                commit=False,
                closeConn=False)
        
				else:
						lib.db.queryDatabase(
                "UPDATE chronicles_info SET has_warnings = TRUE WHERE channel_id=\"{id}\""
                .format(id=str(message.channel.id)),
                client,
                message.channel,
                connection=conn,
                tablename="chronicles_info",
                commit=False,
                closeConn=False)
								
				lib.db.queryDatabase(
            "UPDATE chronicles_info SET warning_list=\"{final}\"".format(
                final=finalList.strip()),
            client,
            message.channel,
            connection=conn,
            tablename="chronicles_info",
            commit=True,
            closeConn=True)
						
				await lib.reaction.reactThumbsUp(client, message)
		
		else:
				await lib.message.send(client,
            message.channel,
            "The Chronicler did not find the warning you wish to remove. Are you sure you spelled it right?",
						feedback=True
        )


async def clearWarnings(client, message):
		"""
		Functions That Clears All Warnings From the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		conn = lib.db.connectToDatabase()
		
		lib.db.queryDatabase(
        "UPDATE chronicles_info SET has_warnings = FALSE WHERE channel_id=\"{id}\""
        .format(id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
				tablename="chronicles_info",
        commit=False,
        closeConn=False)
				
		lib.db.queryDatabase(
        "UPDATE chronicles_info SET warning_list='' WHERE channel_id=\"{id}\"".
        format(id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
        tablename="chronicles_info",
        commit=True,
        closeConn=True)
				
		await lib.reaction.reactThumbsUp(client, message)
