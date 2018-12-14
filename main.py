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
import lib.record
import lib.stats
import lib.story
import lib.validation
import lib.w
import lib.warning

#Setting the Client
client = discord.Client()


#Post a Message Telling the User They Entered an Invalid Command
#message: The Message the User Sent.
async def postInvalidComment(message):
    await client.send_message(
        message.channel,
        "Did not find a valid command. Type '!c help' for a list of valid commands."
    )


#Discord Event Called When a Message Has Been Editted
#Will Try to Find the Old Message in the Chronicle and Replace it With the New Message
#before: The Message Before it Was Editted
#after: The Message After it Was Editted
@client.event
async def on_message_edit(before, after):
    lib.story.editChronicle(client, before, after)


#Discord Event Called When a Channel is Deleted
#Will Close the Chronicle
#Channel: The Channel Deleted.
@client.event
async def on_channel_delete(channel):
    #Close Channel (assuming it is not blacklisted)
    lib.db.queryDatabase(
        "UPDATE chronicles_info SET is_closed=TRUE WHERE channel_id={id};".
        format(id=channel.id),
        commit=True,
        checkExists=True,
        tablename="chronicles_info")


#Discord Event Called When a Message is Sent to the Server/Channel
#Will Control The Chronicler Based on Finding a Command or Not
#If a Command is Found, Act Based on Command. If Not, Attempt to Record the Message
#message: The Message Sent.
@client.event
async def on_message(message):
    #Confirm That the Message Was Sent By Someone Other Than Itself, or
    #Someone Not On the Channel's Ignored User List
    validUser = lib.validation.validateUser(message, client)
    #If the Message Author is Valid
    if validUser is True:
        #If a Command Was Typed In
        if (message.content.startswith('!c')):
            #Get the Arguments by Splitting on Spaces
            args = message.content.split(' ')
            #Show Welcome Command
            if (args[1] == 'welcome'):
                await lib.w.showWelcome(message, client)
            #Show Help Command
            elif (args[1] == 'help'):
                await lib.h.showHelp(message, client)
            #Rewrite Chronicle Command
            elif (args[1] == 'rewrite'):
                await lib.record.startRewrite(message, client)
            #Set Channel Privacy Command
            elif (args[1] == 'set_private'):
                await lib.privacy.setPrivacy(message, client)
            #Add a New Keyword Command
            elif (args[1] == 'add_keyword'):
                await lib.keywords.addKeyword(message, client)
            #Remove an Old Keyword Command
            elif (args[1] == 'remove_keyword'):
                await lib.keywords.removeKeyword(message, client)
            #Close the Chronicle Command
            elif (args[1] == 'close_story'):
                await lib.story.closeStory(message, client)
            #Reopen the Chronicle Command
            elif (args[1] == 'open_story'):
                await lib.story.openStory(message, client)
            #Set the Chronicle's Warnings Command
            elif (args[1] == 'set_warnings'):
                await lib.warning.setWarnings(message, client)
            #Add a New Chronicle Warning Command
            elif (args[1] == 'add_warning'):
                await lib.warning.addWarning(message, client)
            #Remove an Old Chronicle Warning Command
            elif (args[1] == 'remove_warning'):
                await lib.warning.removeWarning(message, client)
            #Create a New Channel Command
            elif (args[1] == 'create_channel'):
                await lib.create.createChroniclerChannel(message, client)
            #Ignore Posted Message Command
            elif (args[1] == 'ignore'):
                await lib.ignore.sendIgnoreReaction(message, client)
            #Add User to Ignore List Command
            elif (args[1] == 'ignore_user'):
                await lib.ignore.addUserToIgnoreList(message, client)
            #Post Link to Chronicle Command
            elif (args[1] == 'get_link'):
                await lib.link.getChronicle(message, client)
            #Blacklist Channel Command
            elif (args[1] == 'blacklist'):
                await lib.blacklist.blacklistChronicle(message, client)
            #Show Channel Stats Command
            elif (args[1] == 'stats'):
                await lib.stats.postChannelStats(message, client)
            #Add a Channel to Database Command
            elif (args[1] == 'whitelist'):
                await lib.create.addChannelToChronicler(
                    message, client, createNew=False)
            #No Valid Command
            else:
                await lib.reaction.reactThumbsDown(message, client)
                await postInvalidComment(message)
        #No Command Found
        else:
            #Make Sure The Chronicle Can Record
            canPost = lib.validation.checkIfCanPost(message, client)
            if canPost is True:
                lib.record.postToDatabase(message, client)


#Keep the Bot Alive
lib.keep_alive.keep_alive()
#Get the Token From .env File
token = os.environ.get("DISCORD_BOT_TOKEN")
#Log Bot In
client.run(token)
