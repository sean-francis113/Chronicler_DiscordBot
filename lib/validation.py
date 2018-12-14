import discord
import lib.db

def validateUser(message, client):
	ignoredUsers = { client.user }

	rowCount, usersFound, exists = lib.db.queryDatabase("SELECT name,id FROM {id}_ignoredUsers".format(id=message.channel.id), checkExists=True, tablename="{id}_ignoredUsers".format(id=message.channel.id), getResult=True, closeConn=True)

	if rowCount > 0:
		for found in usersFound:
			ignoredUsers.append(client.get_user_info(found['id']))

		for user in ignoredUsers:
			if message.author == user:
				return False
		
	return True

async def checkIfCanPost(message, client):
	rowCount, retval, exists = lib.db.queryDatabase("SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel_id={id}".format(message.channel.id), checkExists=True, tablename="chronicles_info", getResult=True, closeConn=True)

	if rowCount > 0:
		if retval['is_blacklisted'] == False and retval['is_closed'] == False:
			return True
		else:
			return False
	else:
		return False