import lib.db
import lib.reaction
import commandList as cmd


async def setWarnings(client, message):
    value = message.content.replace('' + cmd.prefix + ' ' + cmd.set_warning, '')

    #Connect to Database
    conn = lib.db.connectToDatabase()

    if value.strip() == '':
        lib.db.queryDatabase(
            "UPDATE chronicles_info SET has_warnings=FALSE WHERE channel_id=\"{id}\";"
            .format(id=message.channel.id),
            client,
            message.channel,
            connection=conn,
            checkExists=True,
            tablename="chronicles_info",
            commit=True,
            closeConn=False)
    else:
        lib.db.queryDatabase(
            "UPDATE chronicles_info SET has_warnings=TRUE WHERE channel_id=\"{id}\";"
            .format(id=message.channel.id),
            client,
            message.channel,
            connection=conn,
            checkExists=True,
            tablename="chronicles_info",
            commit=True,
            closeConn=False)

    lib.db.queryDatabase(
        "UPDATE chronicles_info SET warning_list=\"{list}\" WHERE channel_id=\"{id}\";"
        .format(list=value.strip(), id=message.channel.id),
        client,
        message.channel,
        connection=conn,
        checkExists=False,
        commit=True,
        closeConn=True)

    await lib.reaction.reactThumbsUp(client, message)


async def addWarning(client, message):
    value = message.content.replace('' + cmd.prefix + ' ' + cmd.add_warning, '')

    #Connect to Database
    conn = lib.db.connectToDatabase()

    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM chronicles_info WHERE channel_id=\"{id}\"".format(
            id=message.channel.id),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="chronicles_info",
        commit=False,
        getResult=True,
        closeConn=False)

    addition = ''

		# 8 = Warning List
    if retval[8].endswith(',') or retval[8] == '':
        addition = value.strip()
    else:
        addition = ', ' + value.strip()

    lib.db.queryDatabase(
        "UPDATE chronicles_info SET has_warnings=TRUE WHERE channel_id=\"{id}\""
        .format(id=message.channel.id),
        client,
        message.channel,
        connection=conn,
        checkExists=False,
        commit=False,
        closeConn=False)
    lib.db.queryDatabase(
        "UPDATE chronicles_info SET warning_list=CONCAT(IFNULL(warning_list, \"\"), \"{add}\")"
        .format(add=addition.strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=False,
        commit=True,
        closeConn=True)

    await lib.reaction.reactThumbsUp(client, message)


async def removeWarning(client, message):
		value = message.content.replace('' + cmd.prefix + ' ' + cmd.remove_warning + ' ', '')
		
		#Connect to Database
		conn = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM chronicles_info WHERE channel_id=\"{id}\"".format(
            id=message.channel.id),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
				tablename = "chronicles_info",
        commit=False,
        getResult=True,
        closeConn=False)
				
		warningList = retval[8]
		index = warningList.find(value)
		
		if index != -1:
				#Need to Check for Comma
				endOfWord = (index + len(value.strip())) - 1
				finalList = ''

				if endOfWord >= len(warningList):
						lib.error.postError(client, message.channel, 'ERROR: Internal Error with Removing Warning.')
						return
				if warningList[endOfWord] == ',' and warningList[index - 2] != ',':
						finalList = warningList.replace((value + ', '), '')
				elif warningList[endOfWord] != ',' and warningList[index - 2] == ',':
						finalList = warningList.replace((', ' + value), '')
				elif warningList[endOfWord] == ',' and warningList[index - 2] == ',':
						finalList = warningList.replace((', ' + value + ', '), '')
				else:
						finalList = warningList.replace(value, '')
						
				if finalList.strip() == '':
						lib.db.queryDatabase(
                "UPDATE chronicles_info SET has_warnings = FALSE WHERE channel_id=\"{id}\""
                .format(id=message.channel.id),
                client,
                message.channel,
                connection=conn,
                checkExists=True,
                commit=False,
                closeConn=False)
				else:
						lib.db.queryDatabase(
                "UPDATE chronicles_info SET has_warnings = TRUE WHERE channel_id=\"{id}\""
                .format(id=message.channel.id),
                client,
                message.channel,
                connection=conn,
                checkExists=True,
                commit=False,
                closeConn=False)
								
				lib.db.queryDatabase(
            "UPDATE chronicles_info SET warning_list=\"{final}\"".format(
                final=finalList.strip()),
            client,
            message.channel,
            connection=conn,
            checkExists=False,
            commit=True,
            closeConn=True)
						
				await lib.reaction.reactThumbsUp(client, message)
		else:
				await client.sendMessage(
            message.channel,
            "The Chronicler did not find the warning you wish to remove. Are you sure you spelled it right?"
        )

async def clearWarnings(client, message):
		conn = lib.db.connectToDatabase()
		
		lib.db.queryDatabase(
                "UPDATE chronicles_info SET has_warnings = FALSE WHERE channel_id=\"{id}\"".format(id=message.channel.id),
                client,
                message.channel,
                connection=conn,
                checkExists=True,
								tablename="chronicles_info",
                commit=False,
                closeConn=False)
						
		lib.db.queryDatabase(
            "UPDATE chronicles_info SET warning_list='' WHERE channel_id=\"{id}\"".format(id=message.channel.id),
            client,
            message.channel,
            connection=conn,
            checkExists=False,
            commit=True,
            closeConn=True)

		await lib.reaction.reactThumbsUp(client, message)