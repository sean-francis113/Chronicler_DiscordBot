import discord
import lib.db

def validateUser(message, client):
	ignoredUsers = { client.user }

	rowCount, usersFound = lib.db.connectAndQuery(("SELECT user_name,user_id FROM %s_ignoredUsers", (message.channel.id)), False, True)

	if rowCount > 0:
		for found in usersFound:
			ignoredUsers.append(client.get_user_info(found['id']))

	for user in ignoredUsers:
		if message.author == user:
			return False
	return True

async def checkIfCanPost(message, client):
	cursor = lib.db.connectToDatabase().cursor()

	rowCount, retval = lib.db.connectAndQuery(("SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel.id=%s", (message.channel.id)), False, True)

	if rowCount > 0:
		if retval['is_blacklisted'] == False and retval['is_closed'] == False:
			return True
		else:
			return False
	else:
		return False