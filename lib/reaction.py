import asyncio
import lib.settings


async def reactThumbsUp(client, message):
		"""
		Function That Reacts to the Provided Message With a Thumbs Up

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to React To
		"""
		
		#settings = lib.settings.checkSettings(client, message.channel)

		#if settings[0][1] == "Full" or settings[0][1] == "Reactions":
		await clearAll(client, message)
		await message.add_reaction("\U0001F44D")


async def reactThumbsDown(client, message):
		"""
		Function That Reacts to the Provided Message With a Thumbs Down

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to React To
		"""
		
		#settings = lib.settings.checkSettings(client, message.channel)

		#if settings[0][1] == "Full" or settings[0][1] == "Reactions":
		await clearAll(client, message)
		await message.add_reaction("\U0001F44E")


async def reactWrench(client, message):
		"""
		Function That Reacts to the Provided Message With a Wrench

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to React To
		"""
		
		#settings = lib.settings.checkSettings(client, message.channel)

		#if settings[0][1] == "Full" or settings[0][1] == "Reactions":
		await clearAll(client, message)
		await message.add_reaction("\U0001F527")


async def clearAll(client, message):
		"""
		Function That Clears All Chronicler Reactions From the Provided Message

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to React To
		"""
		
		try:
				await message.remove_reaction("\U0001F44D", client.user)
				await message.remove_reaction("\U0001F527", client.user)
				await message.remove_reaction("\U0001F44E", client.user)
		except:
				return


async def waitThenClearAll(client, message, timeToSleep=5.0):
    """
		Function That Clears All Chronicler Reactions From the Provided Message After Waiting a Provided Length of Time

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message to React To
		"""

    await asyncio.sleep(timeToSleep)
    await clearAll(client, message)
