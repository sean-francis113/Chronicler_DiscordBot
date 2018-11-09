import discord
import os
import mysql.connector
import lib.db

#Posts the message into the database
#message: The message to post
#client: The bot's client
async def postToDatabase(message, client):
  lib.db.connectAndQuery(("UPDATE %s_contents SET story_content = CONCAT(IFNULL(story_content, ""), \"\\n\" + %s)", (message.channel.id, message.content)), True, False)

  client.add_reaction(message, ":thumbup:")  

async def startRewrite(message, client, finalString, lastMessageFound):
  messagesChecked = 0
  async for curMessage in client.logs_from(message.channel, after=lastMessageFound, limit=500):
    messagesChecked += 1    
    if messagesChecked == 1:
      finalString += curMessage.content
    else:
      finalString += '\n' + curMessage.content
    
    if messagesChecked == 500:
      lastMessageFound = curMessage
      if client.logs_from(message.channel, after=curMessage, limit=500):
        await startRewrite(message, client, finalString, lastMessageFound)

  lib.db.connectAndQuery(("UPDATE %s_contents SET story_content = %s", (message.channel.id, finalString)), True, False)

  client.add_reaction(message, ":thumbup:")