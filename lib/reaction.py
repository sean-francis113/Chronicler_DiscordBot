import asyncio

async def reactThumbsUp(client, message):
    await clearAll(client, message)
    await message.add_reaction("\U0001F44D")


async def reactThumbsDown(client, message):
    await clearAll(client, message)
    await message.add_reaction("\U0001F44E")


async def reactWrench(client, message):
		await clearAll(client, message)
		await message.add_reaction("\U0001F527")

async def clearAll(client, message):
		await message.remove_reaction("\U0001F44D", client.user)
		await message.remove_reaction("\U0001F527", client.user)
		await message.remove_reaction("\U0001F44E", client.user)

async def waitThenClearAll(client, message, timeToSleep=5.0):
		await asyncio.sleep(timeToSleep)
		await clearAll(client, message)