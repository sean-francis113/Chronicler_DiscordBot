import asyncio

async def send(channel, messageStr, ignoreStyle=False, delete=True, time=5.0):
		finalStr = ""
		if ignoreStyle == False:
				finalStr = "```" + messageStr + "```"
		else:
				finalStr = messageStr

		if delete == True:
				message = await channel.send(finalStr, delete_after=time)
		else:
				message = await channel.send(finalStr)

		return message


async def edit(client, message, newStr):
		finalStr = "```" + newStr + "```"
		await message.edit(content=finalStr)


async def delete(client, message):
		await message.delete()

async def waitThenDelete(client, message, time=5.0):
		await asyncio.sleep(time)
		await delete(client, message)