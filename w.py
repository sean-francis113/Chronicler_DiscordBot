import discord
import os
import mysql.connector

async def showWelcome(message, client):
  welcomeString = []

  welcomeString.append('The Chronicler Says Hello!\n\n'
                          'The Chronicler is a Discord Server Bot made for Pen and Paper Role Playing Game (PnPRPG) Servers that records all of the messages it sees into an online database. That database is available to view online at chronicler.seanmfrancis.net where the messages are arranged as a novel. From there, you can download not only your own \'Chronicle\', but also any others on the database to read offline and/or later.\n\n')
  welcomeString.append('To get started, I suggest use the \'Create Channel\' command to create a Chronicler channel with pre-set settings. This will add the channel to The Chronicler\'s database and allow it to start recording the channel. The Chronicler will not record any channel that is not in its database. If you have a channel you wish to add to the database, used the \'Add to Database\' command to add the channel into the database.')
  welcomeString.append('Note, though, that The Chronicler only records messages as they are sent, not any messages sent previous to when it was added to the server. It also cannot handle messages editted after recording. In order to catch these special cases, use the \'Rewrite\' command to have The Chronicler rewrite the Chronicle as it is when the command is sent.')
  welcomeString.append('View the Help Menu (!c help) for more useful commands.\n\nHappy Chronicling!')

  for string in welcomeString:
    await client.send_message(message.channel, string)