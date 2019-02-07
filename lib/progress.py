import asyncio


async def createProgressMessage(client, channel, progressStr):
		finalStr = "```" + progressStr + "```"
		pMessage = await client.send_message(channel, finalStr)
		return pMessage


async def updateProgressMessage(client, pMessage, progressStr):
		if (pMessage.author != client.user):
				await client.send_message(
            pMessage.channel,
            "If you see this, The Chronicler just tried to edit a message it was not supposed to. Please contact us using our Contact Form (chronicler.seanmfrancis.net/contact.php) or directly email us at thechroniclerbot@gmail.com, telling us what you were doing when it happened."
				)
				return
		finalStr = "```" + progressStr + "```"
		await client.edit_message(pMessage, finalStr)


async def deleteProgressMessage(client, pMessage):
		if (pMessage.author != client.user):
				await client.send_message(
            pMessage.channel,
            "If you see this, The Chronicler just tried to delete a message it was not supposed to. Please contact us using our Contact Form (chronicler.seanmfrancis.net/contact.php) or directly email us at thechroniclerbot@gmail.com, telling us what you were doing when it happened."
				)
				return
		await client.delete_message(pMessage)

async def waitThenDeleteProgressMessage(client, pMessage, timeToSleep):
		await asyncio.sleep(timeToSleep)
		await deleteProgressMessage(client, pMessage)
