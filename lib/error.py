import asyncio

async def postErrorAsync(client, channel, error):
	await client.send_message(channel, error)

def postError(client, channel, error):
	asyncio.run(postErrorAsync(client, channel, error))