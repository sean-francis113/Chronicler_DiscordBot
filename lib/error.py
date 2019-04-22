import asyncio
import lib.message


async def postErrorAsync(client, channel, error):
    await lib.message.send(channel, error, time=20.0)


def postError(client, channel, error):
    loop = asyncio.new_event_loop()
    yield from postErrorAsync(client, channel, error)
    loop.stop()