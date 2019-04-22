import lib.db


def validateUser(client, message):		

		if str(message.author.id) == str(client.user.id):
				print("User Not Valid")
				return False
		
		ignoredID = []
		
		rowCount, usersFound, exists = lib.db.queryDatabase(
				"SELECT id FROM {id}_ignoredUsers".format(id=message.channel.id),
        client,
        message.channel,
        checkExists=True,
        tablename="{id}_ignoredUsers".format(id=message.channel.id),
        getResult=True,
        closeConn=True)
				
		if exists == True and usersFound != None:
				for found in usersFound:
						ignoredID.append(found)
						
				for user in ignoredID:
						#2 = Ignored User ID
						if str(message.author.id) == str(user[2]):
								print("User Not Valid")
								return False
		elif exists == True and usersFound == None:
				if str(message.author.id) == str(client.user.id):
							print("User Not Valid")
							return False
				else:
							print("User Valid")
							return True

		print("User Valid")				
		return True


def checkIfCanPost(client, message):
    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel_id={id}"
        .format(id=message.channel.id),
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
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT is_blacklisted FROM chronicles_info WHERE channel_id={id}"
        .format(id=message.channel.id),
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