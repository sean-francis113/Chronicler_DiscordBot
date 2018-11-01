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
    cursor.execute("INSERT INTO " + message.channel.id + "_keywords (keyword,replacement) VALUES (" + keywordValues[0].strip() + ", " + keywordValues[1].strip() + ")")
  else:
    cursor.execute("UPDATE " + message.channel.id + "_keywords SET replacement = " + keywordValues[1].strip() + " WHERE keyword = " + keywordValues[0].strip() + ";")

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

  cursor.execute("SELECT keyword FROM " + message.channel.id + "_keywords WHERE keyword = " + value.strip())

  if cursor.rowcount == 1:
    cursor.execute("DELETE FROM " + message.channel.id + "_keywords WHERE keyword = " + value.strip())
    await client.add_reaction(message, ":thumbup:")
  elif cursor.rowcount == 0:
    await client.send_message(message.channel, "The Chronicler could not find the keyword in its database for this channel. Did you spell it correctly?")