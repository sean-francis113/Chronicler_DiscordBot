import asyncio


async def postErrorAsync(client, channel, error):
    await client.send_message(channel, error)


def postError(client, channel, error):
    loop = asyncio.new_event_loop()
    yield from postErrorAsync(client, channel, error)
    loop.stop()
