import discord
import os
from keep_alive import keep_alive

client = discord.Client()

async def showHelp(message):
  helpString_SectionOne = ('The Chronicler Help Menu:\n\n'
                '!c - The Command Prefix for all commands into The Chronicler\n\n')
  helpString_SectionTwo = ('!c welcome - Posts the Welcome Menu into this channel\n'
                '!c help - Posts the Help Menu into this channel\n'
                '!c rewrite - The Chronicler will run through all of the messages in this channel and recreate the final Chronicle\n'
                '!c set_private <true or false> - Sets this channel to \'Private\' (if true) or \'Public\' (if false). Private means that while you will be able to get the links to the Chronicle, it will not be publicly available for viewing online. Essentially, only those with the generated link can view the Chronicle. Public will allow anyone who visits The Chronicler Site to read the Chronicle.\n'
                '!c add_keyword <Keyword> | <Replacement String> - Adds the specified <Keyword> and its <Replacement String> to the list of Keywords. This will make it so that everytime <Keyword> is in a message, it is replaced by the <Replacement String>. \'|\' is how The Chronicler knows the separation between <Keyword> and <Replacement String> Example: !c add_keyword -dual strike | Baelic swings both of his blades\n'
                '!c remove_keyword <Keyword> - Removes the specified <Keyword> and its associated <Replacement String> from The Chronicler. Example: !c remove_keyword -dual strike\n')
  helpString_SectionThree = ('!c close_story - Tells The Chronicler to \'Close\' this channel\'s Chronicle, preventing The Chronicler from EVER writing to it until it is reopened.\n'
                '!c open_story - Tells The Chronicler to \'Open\' this channel\'s Chronicle, allowing The Chronicler to write to it until it is closed.\n'
                '!c set_warnings <List of Warnings> - Sets the List of Warnings for the Chronicle. These warnings will be posted at the top of this channel\'s Chronicle, helping make sure readers know what may be in the Chronicle. Example: !c set_warnings Sexual Content, Drug and Alchohol Reference, Violence\n'
                '!c add_warning <Warning> - Adds the <Warning> to the list of Warnings. Example: !c add_warning Heavy Language\n'
                '!c remove_warning <Warning> - Removes the Warning from the list of Warnings, if it exists in the list. Example: !c remove_warning Sexual Content\n')
  helpString_SectionFour = ('!c ignore - Tells The Chronicler to Ignore this message. Can be used to send a message that should not be recorded by The Chronicler.\n'
                '!c ignore_user <User Name> - Adds the specified <User Name> to the list of users The Chronicler will ignore. Any messages by the user will not be recorded by The Chronicler. This can also be used to ignore multiple users at once using the \'|\' seperator. Example: !c ignore_user Miggnor / !c ignore_user Miggnor | Calli | Billi_Bob\n'
                '!c get_link - This will tell The Chronicler to post a direct link to your Chronicle.\n'
                '!c stats = This will tell The Chronicler to post your channel\'s settings.\n'
                '!c blacklist - This will tell The Chronicler to completely remove this channel and its Chronicle from its database. BE CAREFUL: The moment you hit Enter and confirm it, The Chronicler will irreversably delete all record of the Chronicle from the site and nothing else in the blacklisted channel will be recorded ever again!\n'
                '!c create_channel <Options> - Creates a new channel in the server set up for The Chronicler. <Options> are optional (if not provided, it is set up for the default values). <Options> must be formatted as follows (without the quotes), seperated by a semicolon (;):\n'
                '* \'channelName=<New Channel Name>\' (What the new channel will be named) (Default:<Your UserName>\'s Chronicle)'
                '* \'isPrivate=true\' or \'isPrivate=false\' (Is the Chronicle Private?) (Default: isPrivate=false)\n'
                '* \'keyword=<Keyword> | <ReplacementString>\' (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)\n'
                '* \'warnings=<Warnings>\' (Create List of Warnings) (Default: None)\n'
                '* \'ignoreUsers=<User Name> | <User Name>...\' (Set up List of Ignored Users) (Default: None)\n'
                '* \'soleOwnership=true\' or \'soleOwnership=false\' (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)\n'
                )
  helpString_SectionFive = ('* \'showWelcome=true\' or \'showWelcome=false\' (Shows the welcome message once the channel is created) (Default: showWelcome=true)\n'
                '* \'showHelp=true\' or \'showHelp=false\' (Shows the help message once the channel is created) (Default: showHelp=true)'
    'Example: !c create_channel isPrivate=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missle; warnings=Sexual Content, Drug and Alchohol Reference, Violence; ignoreUsers=Miggnor | Calli | Billi_Bob; soleOwnership=true')
  
  await client.send_message(message.channel, helpString_SectionOne)
  await client.send_message(message.channel, helpString_SectionTwo)
  await client.send_message(message.channel, helpString_SectionThree)
  await client.send_message(message.channel, helpString_SectionFour)
  await client.send_message(message.channel, helpString_SectionFive)

async def showWelcome(message):
  welcomeString_SectionOne = ('The Chronicler Says Hello!\n\n'
                          'The Chronicler is a Discord Server Bot made for Pen and Paper Role Playing Game (PnPRPG) Servers that records all of the messages it sees into an online database. That database is available to view online at chronicler.seanmfrancis.net where the messages are arranged as a novel. From there, you can download not only your own \'Chronicle\', but also any others on the database to read offline and/or later.\n\n')
  welcomeString_SectionTwo = ('To get started, I suggest blacklisting whichever channel is going to be your general chat or Out of Character Chat (OOC) if any. That way, you are not sending any messages from those channels to the database. Or you can make the channel \'Private\', meaning that there will be data sent to the database, but it will not be publicly viewed. However, you can still view it with a generated link. After that, you can use the \'Create Channel\' command to create a Chronicler channel with pre-set settings. However, it is not necessary to use the \'Create Channel\' command for the Chronicler to record messages. Any channel, as long as it is not blacklisted or closed, will be recorded.')
  welcomeString_SectionThree = ('Note, though, that The Chronicler only records messages as they are sent, not any messages sent previous to when it was added to the server. It also cannot handle messages editted after recording. In order to catch these special cases, use the \'Rewrite\' command to have The Chronicler rewrite the Chronicle as it is when the command is sent.')
  welcomeString_SectionFour = ('View the Help Menu (!c help) for more useful commands.\n\nHappy Chronicling!')

  await client.send_message(message.channel, welcomeString_SectionOne)
  await client.send_message(message.channel, welcomeString_SectionTwo)
  await client.send_message(message.channel, welcomeString_SectionThree)
  await client.send_message(message.channel, welcomeString_SectionFour)

async def startRewrite(message):
  await client.send_message(message.channel, "<Insert Rewrite Message Here>")

async def setPrivacy(message, args):
  await client.send_message(message.channel, "<Insert Privacy Message Here>")

async def addKeyword(message, args):
  await client.send_message(message.channel, "<Insert Add Keyword Message Here>")

async def removeKeyword(message, args):
  await client.send_message(message.channel, "<Insert Remove Keyword Message Here>")

async def closeStory(message):
  await client.send_message(message.channel, "<Insert Close Story Message Here>")

async def openStory(message):
  await client.send_message(message.channel, "<Insert Open Story Message Here>")

async def setWarnings(message, args):
  await client.send_message(message.channel, "<Insert Set Warning Message Here>")

async def addWarning(message, args):
  await client.send_message(message.channel, "<Insert Add Warning Message Here>")

async def removeWarning(message, args):
  await client.send_message(message.channel, "<Insert Remove Warning Message Here>")

async def createChroniclerChannel(message):
  #Parse out options, if any
  channelName = ''
  isPrivate = False
  dict_keys = ['word', 'replacement']
  keywords = []
  warnings = ''
  ignoredUsers = [ '' ]
  soleOwnership = True
  everyone_perms = discord.PermissionOverwrite(
    create_instant_invite=False, 
    manage_channels=False, 
    manage_permissions=False, 
    manage_webhooks=False, 
    read_message_history=True, 
    read_messages=True, 
    send_messages=False, 
    manage_messages=False, 
    send_tts_messages=False, 
    embed_links=False, 
    attach_files=False, 
    mention_everyone=False
    )
  user_perms = discord.PermissionOverwrite(
    create_instant_invite=True, 
    manage_channels=True, 
    manage_permissions=True, 
    manage_webhooks=True, 
    read_message_history=True, 
    read_messages=True,
    send_messages=True, 
    manage_messages=True, 
    send_tts_messages=True, 
    embed_links=True, 
    attach_files=True, 
    mention_everyone=True
    )
  showWelcomeMessage = True
  showHelpMessage = True

  channelOptionsStr = message.content.replace('!c create_channel ', '')
  if(channelOptionsStr.find('=') != -1):
    channelOptionsStr = channelOptionsStr.replace('; ', ';')
    channelOptionsArr = channelOptionsStr.split(';')
    for option in channelOptionsArr:
      if(option.startswith('channelName=')):
        value = option.replace('channelName=', '')
        channelName = value
      if(option.startswith('isPrivate=')):
        value = option.replace('isPrivate=', '')
        value = value.lower()
        if(value.find('true') != -1):
          isPrivate = True
      elif(option.startswith('keyword=')):
        value = option.replace('keyword=', '')
        keywordValues = value.split('|')
        finalCombination = [keywordValues[0].strip(), keywordValues[1].strip()]
        keywords.append(dict(zip(dict_keys, finalCombination)))
      elif(option.startswith('warnings=')):
        value = option.replace('warnings=', '')
        warnings = value
      elif(option.startswith('ignoreUsers=')):
        value = option.replace('ignoreUsers=', '')
        usersFound = value.split('|')
        usersInServer = client.get_all_members()
        for user in usersFound:
          strippedUser = user.strip()
          for serverUser in usersInServer:
            if serverUser.nick == strippedUser or serverUser.name == strippedUser:
              if(ignoredUsers[0] == ''):
                ignoredUsers[0] == serverUser.id
              else:
                ignoredUsers.append(serverUser.id)
      elif(option.startswith('soleOwnership=')):
        value = option.replace('soleOwnership=', '')
        value = value.lower()
        if(value.find('false') != -1):
          everyone_perms = discord.PermissionOverwrite(
            create_instant_invite=True, 
            manage_channels=True, 
            manage_permissions=True, 
            manage_webhooks=True, 
            read_message_history=True, 
            read_messages=True,
            send_messages=True, 
            manage_messages=True, 
            send_tts_messages=True, 
            embed_links=True, 
            attach_files=True, 
            mention_everyone=True
            )
      elif(option.startswith('showWelcome=')):
        value = option.replace('showWelcome=', '')
        value = value.lower()
        if(value.find('false') != -1):
          showWelcomeMessage = False
      elif(option.startswith('showHelp=')):
        value = option.replace('showHelp=', '')
        value = value.lower()
        if(value.find('false') != -1):
          showHelpMessage = False

  keywordString = ''
  warningString = ''
  if(len(keywords) == 0):
    keywordString = 'None'
  else:
    for kword in keywords:
      keywordString += kword['word'] + ', '

  if(len(warnings) == 0):
    warningString = 'None'

  if(channelName == ''):
    channelName = message.author.name + '\'s Chronicle'

  everyone = discord.ChannelPermissions(target=message.server.default_role, overwrite=everyone_perms)
  channelCreator = discord.ChannelPermissions(target=message.author, overwrite=user_perms)
  chronicler = discord.ChannelPermissions(target=client.user, overwrite=user_perms)

  newChannel = await client.create_channel(message.server, channelName, everyone, channelCreator, chronicler)

  await client.send_message(message.channel, "Created new channel with these settings:\n\nchannelName=" + channelName + "\nisPrivate=" + str(isPrivate) + "\nkeywords=" + keywordString + "\nwarnings=" + warningString + "\nsoleOwnership=" + str(soleOwnership) + "\nshowWelcome=" + str(showWelcome) + "\nshowHelp=" + str(showHelp) + "\n\nMake sure that the channel's permissions are correct. The Chronicler is not yet able to access every single permission yet.") 

  #Send Welcome and Help Messages into New Channel
  if(showWelcomeMessage == True or showHelpMessage == True):
    openingMessage = await client.send_message(newChannel, 'Welcome to your new channel!')
    if(showWelcomeMessage == True):
      await showWelcome(openingMessage)
    if(showHelpMessage == True):
      await showHelp(openingMessage)
  #Insert New Channel Data into Database

async def sendIgnoreMessage(message):
  await client.send_message(message.channel, "The Above Message Will Be Ignored By Me!")

async def addUserToIgnoreList(message, args):
  await client.send_message(message.channel, "<Insert Ignore User Message Here>")

async def getChronicle(message):
  await client.send_message(message.channel, "<Insert Chronicle Link Here>")

async def displayChannelStats(message):
  await client.send_message(message.channel, "<Insert Stats Message Here>")

async def blacklistChronicle(message):
  await client.send_message(message.channel, "<Insert Blacklist Message Here>")

async def postInvalidComment(message):
  await client.send_message(message.channel, "Did not find a valid command. Type '!c help' for a list of valid commands.")

def validateUser(message):
  ignoredUsers = { client.user }
  for user in ignoredUsers:
    if message.author == user:
      return False
  return True

async def checkIfCanPost(message):
  await client.send_message(message.channel, "Checking if Message Can Be Posted...")

async def postToDatabase(message):
  await client.send_message(message.channel, "Posting Message to Database...")

@client.event
async def on_channel_delete(channel):
  #Close Channel (assuming it is not blacklisted)
  pass

@client.event
async def on_message(message):
  validUser = validateUser(message)
  if validUser is True:
    if(message.content.startswith('!c')):
      args = message.content.split(' ')
      if(args[1] == 'welcome'):
        await showWelcome(message)
      elif(args[1] == 'rewrite'):
        await startRewrite(message)
      elif(args[1] == 'help'):
        await showHelp(message)
      elif(args[1] == 'set_private'):
        await setPrivacy(message)
      elif(args[1] == 'add_keyword'):
        await addKeyword(message)
      elif(args[1] == 'remove_keyword'):
        await removeKeyword(message)
      elif(args[1] == 'close_story'):
        await closeStory(message)
      elif(args[1] == 'open_story'):
        await openStory(message)
      elif(args[1] == 'set_warnings'):
        await setWarnings(message)
      elif(args[1] == 'add_warning'):
        await addWarning(message)
      elif(args[1] == 'remove_warning'):
        await removeWarning(message)
      elif(args[1] == 'create_channel'):
        await createChroniclerChannel(message)
      elif(args[1] == 'ignore'):
        await sendIgnoreMessage(message)
      elif(args[1] == 'ignore_user'):
        await addUserToIgnoreList(message, args)
      elif(args[1] == 'get_link'):
        await getChronicle(message)
      elif(args[1] == 'blacklist'):
        await blacklistChronicle(message)
      elif(args[1] == 'stats'):
        await displayChannelStats(message)
      else:
        await postInvalidComment(message)
    else:
      canPost = checkIfCanPost(message)    
      if canPost is True:
        postToDatabase(message)

keep_alive()
token = os.environ.get("DISCORD_BOT_TOKEN")
client.run(token)