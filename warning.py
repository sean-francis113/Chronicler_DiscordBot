import discord
import os
import mysql.connector

async def setWarnings(message, client):
  await client.send_message(message.channel, "<Insert Set Warning Message Here>")

async def addWarning(message, client):
  await client.send_message(message.channel, "<Insert Add Warning Message Here>")

async def removeWarning(message, client):
  await client.send_message(message.channel, "<Insert Remove Warning Message Here>")