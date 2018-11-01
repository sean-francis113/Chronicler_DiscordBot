import discord
import os
import mysql.connector

async def sendIgnoreReaction(message, client):
  await client.add_reaction(message, ":thumbup:")

async def addUserToIgnoreList(message,client):
  ignoredUsers = []
  dict_user_keys = ["name", "id"]

  value = message.content.replace('!c ignoreUsers', '')
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
  
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  for user in ignoredUsers:
    cursor.execute("INSERT INTO " + message.channel.id + "_ignoredUsers (ignoredUser_name, ignoredUser_id) VALUES (" + user.name + ", " + user.id + ")")

  await client.add_reaction(message, ":thumbup:")