import asyncio

async def reactThumbsUp(client, message):
    await clearAll(client, message)
    await client.add_reaction(message, "\U0001F44D")


async def reactThumbsDown(client, message):
    await clearAll(client, message)
    await client.add_reaction(message, "\U0001F44E")


async def reactWrench(client, message):
		await clearAll(client, message)
		await client.add_reaction(message, "\U0001F527")

async def clearAll(client, message):
		await client.remove_reaction(message, "\U0001F44D", client.user)
		await client.remove_reaction(message, "\U0001F527", client.user)
		await client.remove_reaction(message, "\U0001F44E", client.user)

async def waitThenClearAll(client, message, timeToSleep):
		await asyncio.sleep(timeToSleep)
		await clearAll(client, message)