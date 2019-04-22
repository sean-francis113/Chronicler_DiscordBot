#Import Statements
import discord
import os
import lib.keep_alive
import lib.blacklist
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


#Post a Message Telling the User They Entered an Invalid Command
#message: The Message the User Sent.
async def postInvalidComment(message):
  await lib.message.send(message.channel, "Did not find a valid command. Type '!c help' for a list of valid commands.", time=15.0)


#Discord Event Called When a Message Has Been Editted
#Will Try to Find the Old Message in the Chronicle and Replace it With the New Message
#before: The Message Before it Was Editted
#after: The Message After it Was Editted
@client.event
async def on_message_edit(before, after):
	if before.author != client.user:
			progressMessage = await lib.message.send(before.channel, "Message Has Been Editted. Editting Chronicle Message As Needed.", delete=False)
			lib.story.editChronicle(client, before, after)
			await lib.message.waitThenDelete(client, progressMessage)


#Discord Event Called When a Channel is Deleted
#Will Close the Chronicle
#Channel: The Channel Deleted.
@client.event
async def on_guild_channel_delete(channel):
  #Close Channel
  lib.db.queryDatabase("UPDATE chronicles_info SET is_closed = TRUE WHERE channel_id={id};".format(id=str(channel.id)), client, channel, commit=True,checkExists=True,tablename="chronicles_info")


#Discord Event Called When a Message is Sent to the Server/Channel
#Will Control The Chronicler Based on Finding a Command or Not
#If a Command is Found, Act Based on Command. If Not, Attempt to Record the Message
#message: The Message Sent.
@client.event
async def on_message(message):
	#Confirm That the Message Was Sent By Someone Other Than Itself, or
	#Someone Not On the Channel's Ignored User List
	print(message.content)
	validUser = lib.validation.validateUser(client, message)
	is_blacklisted = lib.validation.checkBlacklist(client, message)
	#If the Message Author is Valid
	if validUser is True and is_blacklisted is False:
		await lib.reaction.reactWrench(client, message)
		#If a Command Was Typed In
		if (message.content.startswith(cmd.prefix)):
			progressMessage = await lib.message.send(message.channel, "Found Command. Reading Command.", delete=False)
			#Get the Arguments by Splitting on Spaces
			args = message.content.split(' ')
			#Show Welcome Command
			if (args[1] == cmd.show_welcome):
				await lib.message.edit(client, progressMessage, "Found Show Welcome Command. Posting Welcome Message.")
				await lib.w.showWelcome(client, message)
      #Show Help Command
			elif (args[1] == cmd.show_help):
				await lib.message.edit(client, progressMessage, "Found Show Help Command. Posting Help Messages.")
				await lib.h.showHelp(client, message)
      #Rewrite Chronicle Command
			elif (args[1] == cmd.rewrite_story):
				await lib.message.edit(client, progressMessage, "Found Rewrite Command. Starting Rewrite Process.")
				await lib.record.startRewrite(client, message, checkCount=100)
      #Set Channel Privacy Command
			elif (args[1] == cmd.set_privacy):
				await lib.message.edit(client, progressMessage, "Found Set Privacy Command. Setting the New Privacy Setting.")
				await lib.privacy.setPrivacy(client, message)
			#Add a New Keyword Command
			elif (args[1] == cmd.add_keyword):
				await lib.message.edit(client, progressMessage, "Found Add Keyword Command. Adding Keyword(s).")
				await lib.keywords.addKeyword(client, message)
			#Add a New Symbol Command
			elif (args[1] == cmd.add_symbol):
				await lib.message.edit(client, progressMessage, "Found Add Symbol Command. Adding Symbol(s).")
				await lib.symbol.addSymbol(client, message)
      #Remove a Old Symbol Command
			elif (args[1] == cmd.remove_symbol):
				await lib.message.edit(client, progressMessage, "Found Remove Symbol Command. Removing Symbol(s).")
				await lib.symbol.removeSymbol(client, message)
			#Remove an Old Keyword Command
			elif (args[1] == cmd.remove_keyword):
				await lib.message.edit(client, progressMessage, "Found Remove Keyword Command. Removing Keyword(s).")
				await lib.keywords.removeKeyword(client, message)
      #Close the Chronicle Command
			elif (args[1] == cmd.close_story):
				await lib.message.edit(client, progressMessage, "Found Close Story Command. Closing Story.")
				await lib.story.closeStory(client, message)
      #Reopen the Chronicle Command
			elif (args[1] == cmd.open_story):
				await lib.message.edit(client, progressMessage, "Found Open Story Command. Opening Story.")
				await lib.story.openStory(client, message)
      #Set the Chronicle's Warnings Command
			elif (args[1] == cmd.set_warning):
				await lib.message.edit(client, progressMessage, "Found Set Warning Command. Setting Chronicle Warnings.")
				await lib.warning.setWarnings(client, message)
      #Add a New Chronicle Warning Command
			elif (args[1] == cmd.add_warning):
				await lib.message.edit(client, progressMessage, "Found Add Warning Command. Adding Chronicle Warnings.")
				await lib.warning.addWarning(client, message)
      #Remove an Old Chronicle Warning Command
			elif (args[1] == cmd.remove_warning):
				await lib.message.edit(client, progressMessage, "Found Remove Warning Command. Removing Chronicle Warnings.")
				await lib.warning.removeWarning(client, message)
			#Clear All Warnings Command
			elif (args[1] == cmd.clear_warning):
				await lib.message.edit(client, progressMessage, "Found Clear Warning Command. Clearing All Chronicle Warnings.")
				await lib.warning.clearWarnings(client, message)
      #Create a New Channel Command
			elif (args[1] == cmd.create_channel):
				await lib.message.edit(client, progressMessage, "Found Create Channel Command. Creating New Chronicler Channel.")
				await lib.create.createChroniclerChannel(client, message, createNew=True)
      #Ignore Posted Message Command
			elif (args[1] == cmd.ignore_message):
				await lib.message.edit(client, progressMessage, "Found Ignore Command. Ignoring Message.")
				await lib.ignore.sendIgnoreReaction(client, message)
      #Add User to Ignore List Command
			elif (args[1] == cmd.ignore_users):
				await lib.message.edit(client, progressMessage, "Found Add Ignore Users Command. Adding Users to Ignore List.")
				await lib.ignore.addUserToIgnoreList(client, message)
			#Remove Users from Ignored List Command
			elif (args[1] == cmd.remove_ignored_users):
				await lib.message.edit(client, progressMessage, "Found Remove Ignored Users Command. Removing Users from Ignore List.")
				await lib.ignore.removeIgnoredUsers(client, message)
      #Post Link to Chronicle Command
			elif (args[1] == cmd.story_link):
				await lib.message.edit(client, progressMessage, "Found Get Story Link Command. Getting Story Link.")
				await lib.link.getChronicle(client, message)
      #Blacklist Channel Command
			elif (args[1] == cmd.blacklist_channel):
				await lib.message.edit(client, progressMessage, "Found Blacklist Channel Command.")
				await lib.blacklist.blacklistChronicle(client, message)
      #Show Channel General Stats Command
			elif (args[1] == cmd.stats_general):
				await lib.message.edit(client, progressMessage, "Found General Stats Command. Getting Chronicle's General Stats.")
				await lib.stats.displayChannelStats(client, message)
			#Show Channel's Keywords Command
			elif (args[1] == cmd.stats_keywords):
				await lib.message.edit(client, progressMessage, "Found Get Keywords Command. Getting Chronicle's Keywords.")
				await lib.stats.displayKeywords(client, message)
			#Show Channel's Symbols Command
			elif (args[1] == cmd.stats_symbols):
				await lib.message.edit(client, progressMessage, "Found Get Symbols Command. Getting Chronicle's Symbols.")
				await lib.stats.displaySymbols(client, message)
			#Show All Stats for Channel
			elif (args[1] == cmd.stats_all):
				await lib.message.edit(client, progressMessage, "Found Get All Stats Command. Getting All of the Chronicle's Stats.")
				await lib.stats.displayAllStats(client, message)
      #Add a Channel to Database Command
			elif (args[1] == cmd.whitelist_channel):
				await lib.message.edit(client, progressMessage, "Found Whitelist Channel Command. Whitelisting This Channel.")
				await lib.create.addChannelToChronicler(client, message, createNew=False)
      #No Valid Command
			else:
				await lib.reaction.reactThumbsDown(client, message)
				await postInvalidComment(message)
			
			await lib.message.waitThenDelete(client, message, time=6.0)
		
		#No Command Found
		else:
			progressMessage = await lib.message.send(message.channel, "Did Not Find a Command. Checking Validation for Posting.", delete=False)
			#Make Sure The Chronicle Can Record
			if lib.validation.checkIfCanPost(client, message) is True:
				await lib.message.edit(client, progressMessage, "Validation Successful. Posting to Database.")
				await lib.record.postToDatabase(client, message)
			else:
				await lib.message.edit(client, progressMessage, "Validation Failed.")
			
			await lib.reaction.waitThenClearAll(client, message)
		
		await lib.message.waitThenDelete(client, progressMessage)

#Keep the Bot Alive
lib.keep_alive.keep_alive()
#Get the Token From .env File
token = os.environ.get("DISCORD_BOT_TOKEN")
#Log Bot In
client.run(token)