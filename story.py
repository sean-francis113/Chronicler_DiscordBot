import discord
import os
import mysql.connector

async def closeStory(message, client):
  await client.send_message(message.channel, "<Insert Close Story Message Here>")

async def openStory(message, client):
  await client.send_message(message.channel, "<Insert Open Story Message Here>")