import discord

async def reactThumbsUp(message, client):
	await client.add_reaction(message, "\U0001F44D")

async def reactThumbsDown(message, client):
	await client.add_reaction(message, "\U0001F44E")

async def reactWrench(message, client):
	await client.add_reaction(message, "\U0001F527")