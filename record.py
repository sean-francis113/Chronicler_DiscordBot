import discord
import os
import mysql.connector

async def postToDatabase(message, client):
  await client.send_message(message.channel, "Posting Message to Database...")

async def startRewrite(message, client):
  await client.send_message(message.channel, "<Insert Rewrite Message Here>")