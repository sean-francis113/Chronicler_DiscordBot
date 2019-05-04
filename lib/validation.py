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
		
		ignoredID = []
		
		rowCount, usersFound, exists = lib.db.queryDatabase(
				"SELECT id FROM {id}_ignoredUsers".format(id=str(message.channel.id)),
        client,
        message.channel,
        checkExists=True,
        tablename="{id}_ignoredUsers".format(id=str(message.channel.id)),
        getResult=True,
        reportExistance=True)

		if usersFound == None or rowCount == 0:
				return True
				
		if exists == True and usersFound != None:
				for found in usersFound:
						ignoredID.append(found)
						
				for user in ignoredID:
						#2 = Ignored User ID
						if str(message.author.id) == str(user[2]):
								return False
		elif exists == True and usersFound == None:
				return True
			
		return True


def checkIfCanPost(client, message):
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
				if retval[0] == False and retval[1] == False:
						return True
						
				else:
						return False
    
		else:
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
        "SELECT is_blacklisted FROM chronicles_info WHERE channel_id={id}"
        .format(id=str(message.channel.id)),
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