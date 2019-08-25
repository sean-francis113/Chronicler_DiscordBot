import lib.db


def validateUser(client, message):
		"""
		Functions That Checks the Database to Make Sure the User That Posted the Message is Valid

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message With the User to Validate
		"""
		
		if str(message.author.id) == str(client.user.id):
				return False
				
		dictionary = lib.db.checkIfDataExists(client, message.channel, "%s_ignoredUsers" %(message.channel.id), name=message.author.name, id=message.author.id)

		if (int(dictionary["name"]) > 0 or int(dictionary["id"]) > 0):
				return False
		else:
				return True

async def checkIfCanPost(client, message):
		"""
		Functions That Makes Sure the Message's Content Can Be Posted to the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message To Validate
		"""
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel_id={id}"
        .format(id=str(message.channel.id)),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        getResult=True,
        closeConn=True)
		
		if exists == True:
				try:
						if retval[0][0] == False and retval[0][1] == False:
								return True
								
						else:
								await lib.message.send(
												client, message.channel,
												"Message Validation Failed. Is the Channel Closed or Blacklisted? Or is the author of the message being ignored?")
								return False
				except:
						return False
						
		else:
				await lib.message.send(
												client, message.channel,
												"We Could Not Find the Database of Chronicles. Please email thechroniclerbot@gmail.com immediately.")
				return False


def checkBlacklist(client, message):
    """
		Functions That Checks the Database to See if the Channel is Blacklisted

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message of the Channel to Check
		"""

    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT is_blacklisted FROM chronicles_info WHERE channel_id={id}".
        format(id=str(message.channel.id)),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        getResult=True,
        closeConn=True)

    if exists == True:
        if rowCount == 0:
            return False
        elif retval[0] == True:
            return True
        else:
            return False
    else:
        return True
