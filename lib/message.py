import asyncio

async def send(channel, messageStr, delete=True, time=5.0):
		finalStr = "```" + messageStr + "```"
		if delete == True:
				message = await channel.send(finalStr, delete_after=time)
		else:
				message = await channel.send(finalStr)
		return message


async def edit(client, message, newStr):
		if (message.author != client.user):
				await message.channel.send(
            "If you see this, The Chronicler just tried to edit a message it was not supposed to. Please contact us using our Contact Form (chronicler.seanmfrancis.net/contact.php) or directly email us at thechroniclerbot@gmail.com, telling us what you were doing when it happened.",
				time=20.0)
				return
		finalStr = "```" + newStr + "```"
		await message.edit(content=finalStr)


async def delete(client, message):
		if (message.author != client.user):
				await message.channel.send(
            "If you see this, The Chronicler just tried to delete a message it was not supposed to. Please contact us using our Contact Form (chronicler.seanmfrancis.net/contact.php) or directly email us at thechroniclerbot@gmail.com, telling us what you were doing when it happened."
				)
				return
		await message.delete()

async def waitThenDelete(client, message, time=5.0):
		await asyncio.sleep(time)
		await delete(client, message)