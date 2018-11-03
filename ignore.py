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
    cursor.execute("INSERT INTO %s_ignoredUsers (ignoredUser_name, ignoredUser_id) VALUES (%s, %s)", (message.channel.id, user.name, user.id))

  await client.add_reaction(message, ":thumbup:")

#Gets the List of Ignored Users, if any, of the Story from the Database
#channel: The Channel to pull the Users from
#Returns: A tuple array of {username, userID}
def getIgnoredUsers(channel):
  userList = []
  dict_user_keys = ['name', 'id']
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  rowCount = cursor.execute("SELECT ignoredUser_name,ignoredUser_id FROM %s_ignoredUsers", (channel.id))

  if rowCount == 0:
    return userList
  else:
    selectedRows = cursor.fetchall()
    for row in selectedRows:
      combination = [row['ignoredUser_name'], row['ignoredUser_id']]
      userList.append(dict(zip(dict_user_keys, combination)))
    return userList