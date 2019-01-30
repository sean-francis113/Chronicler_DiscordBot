import asyncio


async def createProgressMessage(client, channel, progressStr):
    pMessage = await client.send_message(channel, progressStr)
    return pMessage


async def updateProgressMessage(client, pMessage, progressStr):
    if (pMessage.author != client.user):
        await client.send_message(
            pMessage.channel,
            "If you see this, The Chronicler just tried to edit a message it was not supposed to. Please contact us using our Contact Form (chronicler.seanmfrancis.net/contact.php) or directly email us at thechroniclerbot@gmail.com, telling us what you were doing when it happened."
        )
        return
    await client.edit_message(pMessage, progressStr)


async def deleteProgressMessage(client, pMessage, timeToSleep):
    if (pMessage.author != client.user):
        await client.send_message(
            pMessage.channel,
            "If you see this, The Chronicler just tried to delete a message it was not supposed to. Please contact us using our Contact Form (chronicler.seanmfrancis.net/contact.php) or directly email us at thechroniclerbot@gmail.com, telling us what you were doing when it happened."
        )
        return
    yield from asyncio.sleep(timeToSleep)
    await client.delete_message(pMessage)
