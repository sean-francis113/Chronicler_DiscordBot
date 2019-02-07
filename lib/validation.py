import lib.db


def validateUser(client, message):
		print("Message Author ID: " + message.author.id)
		
		ignoredID = [client.user.id]
		
		rowCount, usersFound, exists = lib.db.queryDatabase(
				"SELECT id FROM {id}_ignoredUsers".format(id=message.channel.id),
        client,
        message.channel,
        checkExists=True,
        tablename="{id}_ignoredUsers".format(id=message.channel.id),
        getResult=True,
        closeConn=True)
				
		print(usersFound)
				
		if exists == True and usersFound != None:
				for found in usersFound:
						print("Ignored User ID: " + found)
						ignoredID.append(found)
						
				for user in ignoredID:
						print("Checking User")
						if message.author.id == user.id:
								print("This Message was written by an ignored user")
								return False
		elif exists == True and usersFound == None:
				if message.author == client.user:
							return False
				else:
							return True
								
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
