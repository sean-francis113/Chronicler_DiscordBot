#Import Statements
import discord
import os
import mysql.connector

#From Statements
from blacklist import *
from create import *
from h import *
from ignore import *
from keep_alive import keep_alive
from keywords import *
from link import *
from privacy import *
from record import *
from stats import *
from story import *
from validation import *
from w import *
from warning import *

#Setting the Client
client = discord.Client()

#Post a Message Telling the User They Entered an Invalid Command
#message: The Message the User Sent.
async def postInvalidComment(message):
  await client.send_message(message.channel, "Did not find a valid command. Type '!c help' for a list of valid commands.")

#Discord Event Called When a Channel is Deleted
#Will Close the Chronicle
#Channel: The Channel Deleted.
@client.event
async def on_channel_delete(channel):
  #Close Channel (assuming it is not blacklisted)
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )
  cursor = mydb.cursor()
  cursor.execute("UPDATE chronicles_info SET is_closed = TRUE; WHERE channel_id=" + channel.id)

#Discord Event Called When a Message is Sent to the Server/Channel
#Will Control The Chronicler Based on Finding a Command or Not
#If a Command is Found, Act Based on Command. If Not, Attempt to Record the Message
#message: The Message Sent.
@client.event
async def on_message(message):
  #Confirm That the Message Was Sent By Someone Other Than Itself, or
  #Someone Not On the Channel's Ignored User List
  validUser = validateUser(message, client)
  #If the Message Author is Valid
  if validUser is True:
    #If a Command Was Typed In
    if(message.content.startswith('!c')):
      #Get the Arguments by Splitting on Spaces
      args = message.content.split(' ')
      #Show Welcome Command
      if(args[1] == 'welcome'):
        await showWelcome(message, client)
      #Show Help Command
      elif(args[1] == 'help'):
        await showHelp(message, client)
      #Rewrite Chronicle Command
      elif(args[1] == 'rewrite'):
        await startRewrite(message, client)
      #Set Channel Privacy Command
      elif(args[1] == 'set_private'):
        await setPrivacy(message, client)
      #Add a New Keyword Command
      elif(args[1] == 'add_keyword'):
        await addKeyword(message, client)
      #Remove an Old Keyword Command
      elif(args[1] == 'remove_keyword'):
        await removeKeyword(message, client)
      #Close the Chronicle Command
      elif(args[1] == 'close_story'):
        await closeStory(message, client)
      #Reopen the Chronicle Command
      elif(args[1] == 'open_story'):
        await openStory(message, client)
      #Set the Chronicle's Warnings Command
      elif(args[1] == 'set_warnings'):
        await setWarnings(message, client)
      #Add a New Chronicle Warning Command
      elif(args[1] == 'add_warning'):
        await addWarning(message, client)
      #Remove an Old Chronicle Warning Command
      elif(args[1] == 'remove_warning'):
        await removeWarning(message, client)
      #Create a New Channel Command
      elif(args[1] == 'create_channel'):
        await createChroniclerChannel(message, client)
      #Ignore Posted Message Command
      elif(args[1] == 'ignore'):
        await sendIgnoreReaction(message, client)
      #Add User to Ignore List Command
      elif(args[1] == 'ignore_user'):
        await addUserToIgnoreList(message, client)
      #Post Link to Chronicle Command
      elif(args[1] == 'get_link'):
        await getChronicle(message, client)
      #Blacklist Channel Command
      elif(args[1] == 'blacklist'):
        await blacklistChronicle(message, client)
      #Show Channel Stats Command
      elif(args[1] == 'stats'):
        await postChannelStats(message, client)
      #Add a Channel to Database Command
      elif(args[1] == 'add_to_database'):
        await addChannelToChronicler(message, client)
      #No Valid Command
      else:
        await postInvalidComment(message)
    #No Command Found
    else:
      #Make Sure The Chronicle Can Record
      canPost = checkIfCanPost(message, client)    
      if canPost is True:
        postToDatabase(message, client)

#Keep the Bot Alive
keep_alive()
#Get the Token From .env File
token = os.environ.get("DISCORD_BOT_TOKEN")
#Log Bot In
client.run(token)