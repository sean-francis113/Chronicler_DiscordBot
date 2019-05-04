#Import Statements
import asyncio
import lib.message


async def postErrorAsync(client, channel, error):
    await lib.message.send(channel, error, time=20.0)


def postError(client, channel, error):
		"""
		Posts a Provided Error to the User

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				channel (discord.TextChannel)
						The Channel That the Error Will be Posted To
				error (string)
						The Error That Will be Posted

		"""
		loop = asyncio.new_event_loop()
		yield from postErrorAsync(client, channel, error)
		loop.stop()