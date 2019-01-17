import lib.db

def validateUser(client, message):
	ignoredUsers = [ client.user ]

	rowCount, usersFound, exists = lib.db.queryDatabase("SELECT name,id FROM {id}_ignoredUsers".format(id=message.channel.id), client, channel=message.channel, checkExists=True, tablename="{id}_ignoredUsers".format(id=message.channel.id), getResult=True, closeConn=True)

	if exists == True and usersFound != None:
		for found in usersFound:
			ignoredUsers.append(client.get_user_info(found[1]))

		for user in ignoredUsers:
			if message.author == user:
				return False
		
	return True

def checkIfCanPost(client, message):
	rowCount, retval, exists = lib.db.queryDatabase("SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel_id={id}".format(id=message.channel.id), client, channel=message.channel, checkExists=True, tablename="chronicles_info", getResult=True, closeConn=True)

	if exists == True:
		if retval[0] == False and retval[1] == False:
			return True
		else:
			return False
	else:
		return False