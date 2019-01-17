async def reactThumbsUp(client, message):
	#Remove Wrench Reaction
	await client.remove_reaction(message, "\U0001F527", client.user)
	await client.add_reaction(message, "\U0001F44D")

async def reactThumbsDown(client, message):
	#Remove Wrench Reaction
	await client.remove_reaction(message, "\U0001F527", client.user)
	await client.add_reaction(message, "\U0001F44E")

async def reactWrench(client, message):
	await client.add_reaction(message, "\U0001F527")