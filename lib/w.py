import lib.message

async def showWelcome(client, message):
		"""
		Functions That Posts The Welcome Message to the Channel

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		welcomeString = []
		
		welcomeString.append(
        'The Chronicler Says Hello!\n\n'
        'The Chronicler is a Discord Server Bot made for Pen and Paper Role Playing Game (PnPRPG) Servers that records all of the messages it sees into an online database. That database is available to view online at chronicler.seanmfrancis.net where the messages are arranged as a novel. From there, you can download not only your own \'Chronicle\', but also any others on the database to read offline and/or later.\n\n'
				'To get started, we suggest using the \'Create Channel\' command to create a Chronicler channel with pre-set settings. This will add the channel to The Chronicler\'s database and allow it to start recording the channel. The Chronicler will not record any channel that is not in its database. If you have a channel you wish to add to the database, used the \'Whitelist\' command to add the channel into the database.\n\n'
				'Note, though, that The Chronicler can only record messages as they are sent, or edit messages that are already in the database. In order to catch special cases, such as recording previous messages or editing messages not in the database, use the \'Rewrite\' command to have The Chronicler rewrite the Chronicle as it is when the command is sent. \n\nView the Help Menu (!c help) for more useful commands.\n\nHappy Chronicling!'
    )
		
		for string in welcomeString:
				await lib.message.send(client, message.channel, string, delete=False)
