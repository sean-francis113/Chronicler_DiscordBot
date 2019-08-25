#Import Statements
import discord
import os
import lib.keep_alive
import lib.blacklist
import lib.channel
import lib.create
import lib.db
import lib.h
import lib.ignore
import lib.keywords
import lib.link
import lib.privacy
import lib.message
import lib.record
import lib.stats
import lib.story
import lib.validation
import lib.w
import lib.warning
import commandList as cmd

#Setting the Client
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name='the story', type=discord.ActivityType.listening))

async def postInvalidComment(message):
    """
		Function That Posts a Message Telling the User They Have Entered an Invalid Command Into The Chronicler.

		Parameters:
		-----------
				message (discord.Message)
						The Message the User Sent.
		"""

    await lib.message.send(client, 
        message.channel,
        "Did not find a valid command. Type '!c help' for a list of valid commands.",
        time=15.0, feedback=True)


@client.event
async def on_raw_message_delete(payload):
    """
		Discord Event Called When Any Message Has Been Deleted.
		Will Try to Find the Old Message in the Chronicle and Delete It.

		Parameters:
		-----------
				payload (discord.RawMessageUpdateEvent)
						The Data of the Deleted Message.
		"""

    #Grab the Message and Channel IDs From Payload
    messageID = payload.message_id
    channelID = payload.channel_id
    serverID = payload.guild_id

    #Delete Message From Database
    lib.story.deleteChronicle(client, messageID, channelID)


@client.event
async def on_raw_message_edit(payload):
    """
		Discord Event Called When Any Message Has Been Editted.
		Will Try to Find the Old Message in the Chronicle and Replace it With the New Message.

		Parameters:
		-----------
				payload (discord.RawMessageUpdateEvent)
						The Data of the Editted Message.
		"""

    #Grab the Message From Payload
    message = await lib.message.getMessageFromPayload(client, payload)

    if message != None:
        #Edit the Message in the Database
        lib.story.editChronicle(client, message)


@client.event
async def on_guild_channel_update(before, after):
    """
		Discord Event Called When a Channel's Settings Have Been Updated.

		Parameters:
		-----------
				before (discord.abs.GuildChannel)
						The Channel Data Before Editting.
				after (discord.abs.GuildChannel)	
						The Channel Data After Editting.
		"""
    #Update the Channel in the Database
    lib.channel.updateChannel(client, before, after)


@client.event
async def on_guild_channel_delete(channel):
    """
		Discord Event Called When a Channel is Deleted

		Parameters:
		-----------
				channel (discord.abs.GuildChannel)
						The Channel Deleted
		"""

    #Close Channel in the Database
    lib.db.queryDatabase(
        "UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id={id};".
        format(id=str(channel.id)),
        client,
        channel,
        commit=True,
        checkExists=True,
        tablename="chronicles_info")

    if channel != None:
        #Update the Last Modified Time in the Database
        await lib.db.updateModifiedTime(client, channel)


@client.event
async def on_message(message):
		"""
		Discord Event Called When a Message is Sent to the Server/Channel.
		If a Command is Found, Act Based on Command. If Not, Attempt to Record the Message.

		Parameters:
		-----------
				message (discord.Message)
						The Message Sent to the Server
		"""

    #Confirm That the Message Actually Has Content to Post to the Database or a Command to Make.
		if message.content == "":
				return

		#settings = lib.settings.checkSettings(client, message.channel)

		#if settings[0][2] == False:

		async with message.channel.typing():
				#Confirm That the Message Was Sent By Someone Other Than Itself, or Someone Not On the Channel's Ignored User List
				validUser = lib.validation.validateUser(client, message)
				is_blacklisted = lib.validation.checkBlacklist(client, message)

		#If the Message Author is Valid
		if validUser is True and is_blacklisted is False:
				
				#If a Command Was Typed In
				if (message.content.startswith(cmd.prefix)):

						async with message.channel.typing():

								#Get the Arguments by Splitting on Spaces
								args = message.content.split(' ')
								args[1] = args[1].lower()

								#Show Welcome Command
								if (args[1] == cmd.show_welcome["command_name"]):
										await lib.w.showWelcome(client, message)

								#Show Help Command
								elif (args[1] == cmd.show_help["command_name"]):
										await lib.h.showHelp(client, message)

								#Rewrite Chronicle Command
								elif (args[1] == cmd.rewrite_story["command_name"]):
										await lib.record.startRewrite(client, message, checkCount=100)

								#Set Channel Privacy Command
								elif (args[1] == cmd.set_privacy["command_name"]):
										await lib.privacy.setPrivacy(client, message)

								#Add a New Keyword Command
								elif (args[1] == cmd.add_keyword["command_name"]):
										await lib.keywords.addKeyword(client, message)

								#Add a New Symbol Command
								elif (args[1] == cmd.add_symbol["command_name"]):
										await lib.symbol.addSymbol(client, message)

								#Remove a Old Symbol Command
								elif (args[1] == cmd.remove_symbol["command_name"]):
										await lib.symbol.removeSymbol(client, message)

								#Remove an Old Keyword Command
								elif (args[1] == cmd.remove_keyword["command_name"]):
										await lib.keywords.removeKeyword(client, message)

								#Close the Chronicle Command
								elif (args[1] == cmd.close_story["command_name"]):
										await lib.story.closeStory(client, message)

								#Reopen the Chronicle Command
								elif (args[1] == cmd.open_story["command_name"]):
										await lib.story.openStory(client, message)

								#Set the Chronicle's Warnings Command
								elif (args[1] == cmd.set_warning["command_name"]):
										await lib.warning.setWarnings(client, message)

								#Add a New Chronicle Warning Command
								elif (args[1] == cmd.add_warning["command_name"]):
										await lib.warning.addWarning(client, message)

								#Remove an Old Chronicle Warning Command
								elif (args[1] == cmd.remove_warning["command_name"]):
										await lib.warning.removeWarning(client, message)

								#Clear All Warnings Command
								elif (args[1] == cmd.clear_warning["command_name"]):
										await lib.warning.clearWarnings(client, message)

								#Clear All Ignored Users
								elif (args[1] == cmd.clear_ignored_users["command_name"]):
										await lib.ignore.clearUsers(client, message)

								#Clear All Keywords
								elif (args[1] == cmd.clear_keywords["command_name"]):
										await lib.keywords.clearList(client, message)

								#Clear All Keywords
								elif (args[1] == cmd.clear_symbols["command_name"]):
										await lib.symbol.clearList(client, message)

								#Create a New Channel Command
								elif (args[1] == cmd.create_channel["command_name"]):
										await lib.create.createChroniclerChannel(
												client, message, createNew=True)

								#Rename Channel Command
								elif (args[1] == cmd.rename_channel["command_name"]):
										lib.channel.changeName(client, message.channel, message)

								#Ignore Posted Message Command
								elif (args[1] == cmd.ignore_message["command_name"]):
										await lib.ignore.sendIgnoreReaction(client, message)

								#Add User to Ignore List Command
								elif (args[1] == cmd.ignore_users["command_name"]):
										await lib.ignore.addUserToIgnoreList(client, message)

								#Remove Users from Ignored List Command
								elif (args[1] == cmd.remove_ignored_users["command_name"]):
										await lib.ignore.removeIgnoredUsers(client, message)

								#Post Link to Chronicle Command
								elif (args[1] == cmd.story_link["command_name"]):
										await lib.link.getChronicle(client, message)

								#Blacklist Channel Command
								elif (args[1] == cmd.blacklist_channel["command_name"]):
										await lib.blacklist.blacklistChronicle(client, message)

								#Show Channel General Stats Command
								elif (args[1] == cmd.stats_general["command_name"]):
										await lib.stats.displayChannelStats(client, message)

								#Show Channel's Keywords Command
								elif (args[1] == cmd.stats_keywords["command_name"]):
										await lib.stats.displayKeywords(client, message)

								#Show Channel's Symbols Command
								elif (args[1] == cmd.stats_symbols["command_name"]):
										await lib.stats.displaySymbols(client, message)

								#Show All Stats for Channel
								elif (args[1] == cmd.stats_all["command_name"]):
										await lib.stats.displayAllStats(client, message)

								#Add a Channel to Database Command
								elif (args[1] == cmd.whitelist_channel["command_name"]):
										await lib.create.createChroniclerChannel(
												client, message, createNew=False)

								#No Valid Command
								else:

										#Show Player That The Chronicler Was Unsuccessful
										await lib.reaction.reactThumbsDown(client, message)

										#Post the Invalid Command Comment
										await postInvalidComment(message)

						if not message.content.startswith(cmd.ignore_message["command"]):
								await lib.message.waitThenDelete(client, message)

				#No Command Found
				else:

						async with message.channel.typing():

								#Make Sure The Chronicle Can Record
								if await lib.validation.checkIfCanPost(client, message):
										await lib.record.postToDatabase(client, message)
				
				await lib.reaction.waitThenClearAll(client, message)

#Keep the Bot Alive
lib.keep_alive.keep_alive()

#Get the Token From .env File
token = os.environ.get("DISCORD_BOT_TOKEN")

#Log Bot In
client.run(token)