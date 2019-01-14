import lib.db
import lib.reaction

async def sendIgnoreReaction(message, client):
	await lib.reaction.reactThumbsUp(message, client)

async def addUserToIgnoreList(message,client):
	ignoredUsers = []
	dict_user_keys = ["name", "id"]
	
	value = message.content.replace('!c ignore_users', '')
	usersFound = value.split('|')
	print(usersFound)
	usersInServer = client.get_all_members()
	print(usersInServer)
	for user in usersFound:
		strippedUser = user.strip()
		print("Finding User: " + user)
		for serverUser in usersInServer:
			if serverUser.nick == strippedUser:
				print("Found User Nickname")
				combination = [serverUser.nick, serverUser.id]
				ignoredUsers.append(dict(zip(dict_user_keys, combination)))
			elif serverUser.name == strippedUser:
				print("Found User Name")
				combination = [serverUser.name, serverUser.id]
				ignoredUsers.append(dict(zip(dict_user_keys, combination)))
	
	conn = lib.db.connectToDatabase()
	for user in ignoredUsers:
		lib.db.queryDatabase("INSERT INTO {channel_id}_ignoredUsers (name, id) VALUES (\"{user_name}\", \"{user_id}\")".format(channel_id=message.channel.id, user_name=user["name"], user_id=user["id"]), client, channel=message.channel, connection=conn, commit=False, checkExists=True, tablename="{channel_id}_ignoredUsers".format(channel_id=message.channel.id), closeConn=False)
	conn.commit()
	conn.close()
	
	await lib.reaction.reactThumbsUp(message, client)

#Gets the List of Ignored Users, if any, of the Story from the Database
#channel: The Channel to pull the Users from
#Returns: A tuple array of {username, userID}
def getIgnoredUsers(channel, client):
	userList = []
	dict_user_keys = ['name', 'id']
	rowCount, selectedRows, exists = lib.db.queryDatabase("SELECT name,id FROM {id}_ignoredUsers".format(id=channel.id), client, channel=channel, checkExists=True, tablename="{id}_ignoredUsers".format(id=channel.id), getResult=True, closeConn=True)
	
	if rowCount == 0 or exists == False:
		return userList
	else:
		for row in selectedRows:
			combination = [row['ignoredUser_name'], row['ignoredUser_id']]
			userList.append(dict(zip(dict_user_keys, combination)))
		return userList