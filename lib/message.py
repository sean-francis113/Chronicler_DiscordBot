import asyncio

async def send(client, channel, messageStr, ignoreStyle=False, feedback=False, delete=True, time=5.0):
		"""
		Send a Message to the Specified Channel, Formatted Specificially for The Chronicler's Messages

		Parameters:
		-----------
				channel (discord.TextChannel)
						The Channel to Post the Message Into
				messageStr (string)
						The Contents of the Message
				ignoreStyle (boolean, OPTIONAL)
						Flag to Ignore the Formatting of the Message
				delete (boolean, OPTIONAL)
						Flag to Delete the Message After a Period of Time
				time (float, OPTIONAL)
						How Long to Wait Before Deleting the Message, if delete is True
		"""
		
		#settings = lib.settings.checkSettings(client, channel)

		#if (feedback == True and (settings[0][1] == "Full" or settings[0][1] == "Messages")) or feedback == False:
		#The Final String to Be the Message's Content
		finalStr = ""

		#If We Are Not Ignoring Formatting
		if ignoreStyle == False:
				finalStr = "```" + messageStr + "```"

		#Otherwise
		else:
				finalStr = messageStr

		#If the Message Will be Deleted
		if delete == True:
				message = await channel.send(finalStr, delete_after=time)

		#Otherwise
		else:
				message = await channel.send(finalStr)

		#Return the Message
		return message
		#else:
				#return None


async def edit(client, message, newStr, feedback=False):
		"""
		Function That Edits the Provided Message.

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to Edit
				newStr (string)
						The Content of the Editted Message
		"""

		if message == None:
				return None
				
		#settings = lib.settings.checkSettings(client, message.channel)

		#if (feedback == True and (settings[0][1] == "Full" or settings[0][1] == "Messages")) or feedback == False:
		finalStr = "```" + newStr + "```"
		await message.edit(content=finalStr)
		#else:
				#return None


async def delete(client, message):
		"""
		Delete the Provided Message

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to Delete
		"""
		
		try:
				await message.delete()
		except:
				return


async def waitThenDelete(client, message, time=5.0):
    """
		Wait for a While, Then Delete the Provided Message

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to Delete
				time (float)
						How Long to Wait Before Deleting
		"""

    await asyncio.sleep(time)
    await delete(client, message)


async def getMessageFromPayload(client, payload):
		"""
		Retrieve a Message From Raw Payload Data.
		
		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				payload (discord.RawMessageUpdateEvent)
						The Raw Data From Events
				deleteEvent (boolean, OPTIONAL)
						Flag to Say if This is From a Delete Event or Not
		"""
		
		channel = None
		server = None
		message = None

    #Do Nothing if the Editted Message Belongs to The Chronicler
		if str(payload.data['author']['id']) == str(client.user.id):
				return

		messageID = payload.message_id
		channelID = payload.data['channel_id']
		serverID = payload.data['guild_id']

    #Find the Server This Message is in. Needed to Find the Channel, then the Message.
		if server == None:
				for guild in client.guilds:
						if str(guild.id) == str(serverID):
								server = guild
								
		if server == None:
				return

    #Get a List of All Channels In the Server
		cList = server.text_channels

    #Look Through the Channel List to Find the One the Message is in
		for c in cList:
				if str(c.id) == str(channelID):
						channel = c
						
		if channel == None:
				return

    #Grab the Message From the Channel
		message = await channel.fetch_message(messageID)
		
		if message == None:
				return

    #Return Message
		return message