import discord
import os
import mysql.connector
import datetime

from w import showWelcome
from h import showHelp
from record import startRewrite

async def createChroniclerChannel(message, client):
  #Initialize Variables
  isPrivate = False
  dict_word_keys = ['word', 'replacement']
  keywords = []
  hasWarnings = False
  warnings = ''
  dict_user_keys = ['name', 'id']
  ignoredUsers = []
  soleOwnership = True
  channelName = message.author.name + '\'s Chronicle'
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

  #Parse out options, if any
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
        keywords.append(dict(zip(dict_word_keys, finalCombination)))
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
            if serverUser.nick == strippedUser:
              combination = [serverUser.nick, serverUser.id]
              ignoredUsers.append(dict(zip(dict_user_keys, combination)))
            elif serverUser.name == strippedUser:
              combination = [serverUser.name, serverUser.id]
              ignoredUsers.append(dict(zip(dict_user_keys, combination)))
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

  #Create Channel Permissions
  everyone = discord.ChannelPermissions(target=message.server.default_role, overwrite=everyone_perms)
  channelCreator = discord.ChannelPermissions(target=message.author, overwrite=user_perms)
  chronicler = discord.ChannelPermissions(target=client.user, overwrite=user_perms)

  #Create the New Channel
  newChannel = await client.create_channel(message.server, channelName, everyone, channelCreator, chronicler)

  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  #Create Channel Tables
  cursor.execute("CREATE TABLE %s_contents (db_id INT NOT NULL PRIMARY KEY, channel_id VARCHAR(255) NOT NULL, word_count INT NOT NULL, story_content MEDIUMTEXT)", (newChannel.id))
  cursor.execute("CREATE TABLE %s_keywords (kw_id INT AUTO INCREMENT NOT NULL PRIMARY KEY, keyword VARCHAR(255) NOT NULL, replacement_string TEXT NOT NULL)", (newChannel.id))
  cursor.execute("CREATE TABLE %s_ignoredUsers (iu_id INT AUTO INCREMENT NOT NULL PRIMARY KEY, ignoredUser_name VARCHAR(255) NOT NULL, ignoredUser_id VARCHAR(255) NOT NULL)", (newChannel.id))

  #Add New Channel Into chronicles_info
  cursor.execute("INSERT INTO chronicles_info (is_blacklisted, is_closed, is_private, channel_name, channel_id, channel_owner, has_warning, warning_list, date_last_modified) VALUES (FALSE, FALSE, %s, %s, %s, %s, %s, %s, %s)", (isPrivate.upper(), newChannel.name, newChannel.id, message.author.name, hasWarnings.upper(), warnings, datetime.strptime("%c")))

  #Add Any Specified Keywords
  if(len(keywords) > 0):
    for index in keywords:
      cursor.execute("INSERT INTO %s_keywords (keyword, replacement_string) VALUES (%s, %s)", (newChannel.id, index['word'], index['replacement']))

  #Add Any Specified Users to Ignore
  if(len(ignoredUsers) > 0):
    for index in ignoredUsers:
      cursor.execute("INSERT INTO %s_ignoredUsers (ignoredUser_name, ignoredUser_id) VALUES (%s, %s)", (newChannel.id, index['name'], index['id']))

  #Send Welcome and Help Messages into New Channel
  if(showWelcomeMessage == True or showHelpMessage == True):
    openingMessage = await client.send_message(newChannel, 'Welcome to your new channel!')
    if(showWelcomeMessage == True):
      await showWelcome(openingMessage)
    if(showHelpMessage == True):
      await showHelp(openingMessage)

async def addChannelToDatabase(message, client):
  #Initialize Variables
  isPrivate = False
  dict_word_keys = ['word', 'replacement']
  keywords = []
  hasWarnings = False
  warnings = ''
  dict_user_keys = ['name', 'id']
  ignoredUsers = []
  willRewrite = False

  #Parse out options, if any
  channelOptionsStr = message.content.replace('!c create_channel ', '')
  if(channelOptionsStr.find('=') != -1):
    channelOptionsStr = channelOptionsStr.replace('; ', ';')
    channelOptionsArr = channelOptionsStr.split(';')
    for option in channelOptionsArr:
      if(option.startswith('isPrivate=')):
        value = option.replace('isPrivate=', '')
        value = value.lower()
        if(value.find('true') != -1):
          isPrivate = True
      elif(option.startswith('keyword=')):
        value = option.replace('keyword=', '')
        keywordValues = value.split('|')
        finalCombination = [keywordValues[0].strip(), keywordValues[1].strip()]
        keywords.append(dict(zip(dict_word_keys, finalCombination)))
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
            if serverUser.nick == strippedUser:
              combination = [serverUser.nick, serverUser.id]
              ignoredUsers.append(dict(zip(dict_user_keys, combination)))
            elif serverUser.name == strippedUser:
              combination = [serverUser.name, serverUser.id]
              ignoredUsers.append(dict(zip(dict_user_keys, combination)))
      elif(option.startswith('rewrite=')):
        value = option.replace('rewrite=', '')
        lowerValue = value.lower()
        if lowerValue.strip() == 'true':
          willRewrite = True
  
  #Connect to Database
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  #Create Channel Tables
  cursor.execute("CREATE TABLE %s_contents (db_id INT NOT NULL PRIMARY KEY, channel_id VARCHAR(255) NOT NULL, word_count INT NOT NULL, story_content MEDIUMTEXT)", (message.channel.id))
  cursor.execute("CREATE TABLE %s_keywords (kw_id INT AUTO INCREMENT NOT NULL PRIMARY KEY, keyword VARCHAR(255) NOT NULL, replacement_string TEXT NOT NULL)", (message.channel.id))
  cursor.execute("CREATE TABLE %s_ignoredUsers (iu_id INT AUTO INCREMENT NOT NULL PRIMARY KEY, ignoredUser_name VARCHAR(255) NOT NULL, ignoredUser_id VARCHAR(255) NOT NULL)", (message.channel.id))

  #Add New Channel Into chronicles_info
  cursor.execute("INSERT INTO chronicles_info (is_blacklisted, is_closed, is_private, channel_name, channel_id, channel_owner, has_warning, warning_list, date_last_modified) VALUES (FALSE, FALSE, %s, %s, %s, %s, %s, %s, %s)", (isPrivate.upper(), message.channel.name, message.channel.id, message.author.name, hasWarnings.upper(), warnings, datetime.strptime("%c")))

  #Add Any Specified Keywords
  if(len(keywords) > 0):
    for index in keywords:
      cursor.execute("INSERT INTO %s_keywords (keyword, replacement_string) VALUES (%s, %s)", (message.channel.id, index['word'], index['replacement']))

  #Add Any Specified Users to Ignore
  if(len(ignoredUsers) > 0):
    for index in ignoredUsers:
      cursor.execute("INSERT INTO %s_ignoredUsers (ignoredUser_name, ignoredUser_id) VALUES (%s, %s)", (message.channel.id, index['word'], index['replacement']))
  
  #Rewrite the Chroncile if User Wishes
  if willRewrite == True:
    await startRewrite(message, client)

  #Tell User We Are Done
  await client.add_reaction(message, ":thumbup:")