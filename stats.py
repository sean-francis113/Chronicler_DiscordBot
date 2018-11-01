import discord
import os
import mysql.connector

async def displayChannelStats(message, client):
  await client.send_message(message.channel, "<Insert Stats Message Here>")