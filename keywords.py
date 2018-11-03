import discord
import os
import mysql.connector

async def addKeyword(message, client):
  value = message.content.replace('!c add_keyword', '')
  keywordValues = value.split('|')

  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT keyword FROM " + message.channel.id + "_keywords WHERE keyword=" + keywordValues[0].strip())

  if cursor.rowcount == 0:
    cursor.execute("INSERT INTO %s_keywords (keyword,replacement) VALUES (%s, %s)", (message.channel.id, keywordValues[0].strip(), keywordValues[1].strip))
  else:
    cursor.execute("UPDATE %s_keywords SET replacement = %s WHERE keyword = %s;", (message.channel.id, keywordValues[1].strip(), keywordValues[0].strip()))

  await client.add_reaction(message.channel, ":thumbup:")

async def removeKeyword(message, client):
  value = message.content.replace('!c add_keyword', '')

  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  rowCount = cursor.execute("SELECT keyword FROM %s_keywords WHERE keyword = %s", (message.channel.id, value.strip()))

  if rowCount == 1:
    cursor.execute("DELETE FROM %s_keywords WHERE keyword = %s", (message.channel.id, value.strip()))
    await client.add_reaction(message, ":thumbup:")
  elif rowCount == 0:
    await client.send_message(message.channel, "The Chronicler could not find the keyword in its database for this channel. Did you spell it correctly?")

#Gets the List of Keywords, if any, of the Story from the Database
#channel: The Channel to pull the Keywords from
#Returns: An tuple array of {keyword, replacement_string}
def getKeywords(channel):
  wordList = []
  dict_word_keys = ['word', 'replacement']
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  rowCount = cursor.execute("SELECT keyword,replacement_string FROM %s_keywords", (channel.id))

  if rowCount == 0:
    return wordList
  else:
    selectedRows = cursor.fetchall()
    for row in selectedRows:
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