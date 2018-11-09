import discord
import lib.db

async def setWarnings(message, client):
  value = message.content.replace("!c set_warnings", '')

  #Connect to Database
  cursor = lib.db.connectToDatabase()

  if value == '':
    lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET has_warning = FALSE WHERE channel_id=%s", (message.channel.id)), True, False)
  else:
    lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET has_warning = TRUE WHERE channel_id=%s", (message.channel.id)), True, False)

  lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET warning_list = %s", (value.strip())), True, False)

  await client.add_reaction(message, ":thumbup:")

async def addWarning(message, client):
  value = message.content.replace("!c add_warning", '')

  #Connect to Database
  cursor = lib.db.connectToDatabase()

  rowCount, retval = lib.db.queryDatabase(cursor, ("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id)), False, True)

  addition = ''

  if retval['warning_list'].endswith(',') or retval['warning_list'] == '':
    addition = value.strip()
  else:
    addition = ', ' + value.strip()

  lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET has_warning = TRUE WHERE channel_id = %s", (message.channel.id)), False, False)
  lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET warning_list = CONCAT(IFNULL(warning_list, ''), %s)", (addition.strip())), True, False)

  await client.add_reaction(message, ":thumbup:")

async def removeWarning(message, client):
  value = message.content.replace("!c remove_warning", '')

  #Connect to Database
  cursor = connectToDatabase()

  rowCount, retval = lib.db.queryDatabase(cursor, ("SELECT * FROM chronicles_info WHERE channel_id = %s", (message.channel.id)), False, True)

  warningList = retval['warning_list']
  index = warningList.find(value)

  if index != -1:
    #Need to Check for Comma
    endOfWord = index + len(value.strip())
    finalList = ''
    if value[endOfWord] == ',':
      finalList = warningList.replace((value + ', '), '')
    else:
      finalList = warningList.replace(value, '')

    if finalList.strip() == '':
      lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET has_warning = FALSE WHERE channel_id = %s", (message.channel.id)), False, False)
    else:
      lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET has_warning = TRUE WHERE channel_id = %s", (message.channel.id)), False, False)

    lib.db.queryDatabase(cursor, ("UPDATE chronicles_info SET warning_list = %s", (finalList.strip())), True, False)

    await client.add_reaction(message, ":thumbup:")
  else:
    await client.sendMessage(message.channel, "The Chronicler did not find the warning you wish to remove. Are you sure you spelled it right?")