import discord
import lib.db

async def addKeyword(message, client):
  value = message.content.replace('!c add_keyword', '')
  keywordValues = value.split('|')

  cursor = lib.db.connectToDatabase()

  rowCount, result = lib.db.queryDatabase(cursor, ("SELECT keyword FROM %s_keywords WHERE keyword=%s", (message.channel.id, keywordValues[0].strip())), False, True)

  if rowCount == 0:
    lib.db.queryDatabase(cursor, ("INSERT INTO %s_keywords (keyword,replacement) VALUES (%s, %s)", (message.channel.id, keywordValues[0].strip(), keywordValues[1].strip())), True, False)
  else:
    lib.db.queryDatabase(cursor, ("UPDATE %s_keywords SET replacement = %s WHERE keyword = %s;", (message.channel.id, keywordValues[1].strip(), keywordValues[0].strip())), True, False)

  await client.add_reaction(message.channel, ":thumbup:")

async def removeKeyword(message, client):
  value = message.content.replace('!c add_keyword', '')

  cursor = lib.db.connectToDatabase()

  rowCount, retval = lib.db.queryDatabase(cursor, ("SELECT keyword FROM %s_keywords WHERE keyword = %s", (message.channel.id, value.strip())), False, True)

  if rowCount == 1:
    lib.db.queryDatabase(cursor, ("DELETE FROM %s_keywords WHERE keyword = %s", (message.channel.id, value.strip())), True, False)
    await client.add_reaction(message, ":thumbup:")
  elif rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find the keyword in its database for this channel. Did you spell it correctly?")

#Gets the List of Keywords, if any, of the Story from the Database
#channel: The Channel to pull the Keywords from
#Returns: An tuple array of {keyword, replacement_string}
def getKeywords(channel):
  wordList = []
  dict_word_keys = ['word', 'replacement']
  rowCount, retval = lib.db.connectAndQuery(("SELECT keyword,replacement_string FROM %s_keywords", (channel.id)), False, True)

  if rowCount == 0:
    return wordList
  else:
    for row in retval:
      combination = [row['keyword'], row['replacement']]
      wordList.append(dict(zip(dict_word_keys, combination)))
    return wordList

#Searches through the String, replacing all instances of 'keyword' with 'replacement'
#string: The String to Search Through
#keyword: The string to replace
#replacement: The string to replace 'keyword' with
#Returns: The New String with all replacements made
def replaceKeyword(string, keyword, replacement):
  newString = string.replace(keyword, replacement)
  return newString