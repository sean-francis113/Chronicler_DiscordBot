import lib.db
import lib.reaction
import commandList as cmd
import lib.message


async def sendIgnoreReaction(client, message):
		"""
		Function That Sends a Reaction When the User Specifies a Message to be Ignored

		Parameters:
		-----------
				client (discord.Client)
						The Chroniler Client
				message (discord.Message)
						The Message to Be Ignored By The Chronicler
		"""
		
		await lib.reaction.reactThumbsUp(client, message)


async def addUserToIgnoreList(client, message):
		"""
		Function That Adds the Specified Users in the Message to The Channel's Ignore List

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Had the Command
		"""

		#The Array of Ignored Users to Be Filled
		ignoredUsers = []

		#The Keys of the Dictionary to Be Used
		dict_user_keys = ["name", "id"]

		#Grab All of the Users In the Message
		value = message.content.replace(cmd.ignore_users["command"], '')
		usersFound = value.split('|')

		#Grab All of the Users in the Server to Reference
		usersInServer = message.channel.guild.members

		#Look Through All of the Users in the Message
		for user in usersFound:
				strippedUser = user.strip()

				#Look Through All of the Users in the Server
				for serverUser in usersInServer:
						#Make Sure We Grab the Right User, Even if They Are Using a Nickname
						if serverUser.nick == strippedUser:
								combination = [serverUser.nick, str(serverUser.id)]
								ignoredUsers.append(dict(zip(dict_user_keys, combination)))
						elif serverUser.name == strippedUser:
								combination = [serverUser.name, str(serverUser.id)]
								ignoredUsers.append(dict(zip(dict_user_keys, combination)))

		#Connect To Database
		conn = lib.db.connectToDatabase()

		#For Users We've Found and Are Going to Ignore
		for user in ignoredUsers:
				dictionary = lib.db.checkIfDataExists(client, message.channel, "%s_ignoredUsers" %(message.channel.id), name=user["name"], id=user["id"])

				print(dictionary)

				if(int(dictionary["name"]) == 0 and int(dictionary["id"]) == 0):

						#Add User to Database Ignore List
						lib.db.queryDatabase(
								"INSERT INTO {channel_id}_ignoredUsers (name, id) VALUES (\"{user_name}\", \"{user_id}\")"
								.format(
										channel_id=str(message.channel.id),
										user_name=user["name"],
										user_id=user["id"]),
								client,
								message.channel,
								connection=conn,
								commit=False,
								
								tablename="{channel_id}_ignoredUsers".format(
										channel_id=str(message.channel.id)),
								closeConn=False)

		#Commit to Database Once We Are Done
		conn.commit()

		#Close Database Connection
		conn.close()

		#Show Success
		await lib.reaction.reactThumbsUp(client, message)


async def removeIgnoredUsers(client, message):
		"""
		Function That Deletes the Provided Users from the Ignored Users table, if They Exist

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Has the Users to Remove
		"""

		# Grab the Users to Remove From Message
		value = message.content.replace(cmd.remove_ignored_users["command"], '')
		usersFound = value.split('|')

		#Connect to Database
		conn = lib.db.connectToDatabase()

		#Get All Users in the Ignored User Table
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT name,id FROM {channel_id}_ignoredUsers".format(channel_id=str(message.channel.id)),
        client,
        message.channel,
        connection=conn,
        commit=False,
        
        tablename="{channel_id}_ignoredUsers".format(channel_id=str(message.channel.id)),
        reportExistance=True,
        getResult=False,
        closeConn=False)

		#Make Sure Table Exists
		if exists == False:
				return

		#If There Are No Users in the List
		elif rowCount == 0:
				await lib.message.send(client, 
            message.channel,
            "The Chronicler could not find any users in your Ignored User List.",
						feedback=True
        )
				return

		#Grab All of the Users in Servers
		serverUsers = message.channel.guild.members

		#Look Through All of the Users In the Message
		for user in usersFound:

				#Look Through All of the Users in the Server
				for sUser in serverUsers:
						if user.strip() == sUser.nick or user.strip() == sUser.name:
								lib.db.queryDatabase(
                    "DELETE FROM {channel_id}_ignoredUsers WHERE id=\"{userID}\""
                    .format(channel_id=str(message.channel.id), userID=sUser.id),
                    client,
                    message.channel,
                    connection=conn,
                    commit=False,
                    getResult=False,
                    closeConn=False)
								break

		#Commit the Database Once We Are Done
		conn.commit()
		#Close the Database Connection
		conn.close()

		#Show Success
		await lib.reaction.reactThumbsUp(client, message)


def getIgnoredUsers(client, channel):
		"""
		Function That Gets the List of Ignored Users, if any, of the Channel from the Database

		Parameters:
		-----------

		"""
		
		userList = []
		dict_user_keys = ['name', 'id']
		rowCount, selectedRows, exists = lib.db.queryDatabase(
        "SELECT name,id FROM {id}_ignoredUsers".format(id=channel.id),
        client,
        channel,
        
        tablename="{id}_ignoredUsers".format(id=channel.id),
        getResult=True,
        closeConn=True)
				
		if rowCount == 0 or exists == False:
				return userList
        
				
		else:
				for row in selectedRows:
						combination = [row[0], row[1]]
						userList.append(dict(zip(dict_user_keys, combination)))
				return userList

async def clearUsers(client, message):
		lib.db.queryDatabase(
                    "DELETE FROM {channel_id}_ignoredUsers"
                    .format(channel_id=str(message.channel.id)),
                    client,
                    message.channel,
                    getResult=False, commit=True)