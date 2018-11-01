import discord
import os
import mysql.connector

def validateUser(message, client):
  ignoredUsers = { client.user }
  
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT user_name,user_id FROM " + message.channel.id + "_ignoredUsers")

  usersFound = cursor.fetchall()

  for found in usersFound:
    ignoredUsers.append(client.get_user_info(found['id']))

  for user in ignoredUsers:
    if message.author == user:
      return False
  return True

async def checkIfCanPost(message, client):
  mydb = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("CHRONICLER_DATABASE_USER"),
    passwd = os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
    database = os.environ.get("CHRONICLER_DATABASE_DB")
  )

  cursor = mydb.cursor()

  cursor.execute("SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel.id=" + message.channel.id)
    
  retval = cursor.fetchone()

  if retval['is_blacklisted'] == False and retval['is_closed'] == False:
    valid = validateUser(message)
    if valid == True:
      return True
    else:
      return False
  else:
    return False