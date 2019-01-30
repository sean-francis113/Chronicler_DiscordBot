import lib.db
import lib.reaction


async def getChronicle(client, message):
    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT is_blacklisted FROM chronicles_info WHERE channel_id={id}".
        format(id=message.channel.id),
        client,
        channel=message.channel,
        checkExists=True,
        tablename="chronicles_info",
        commit=False,
        getResult=True,
        closeConn=True)

    if rowCount == 1:
        if retval[0] == False:
            await client.send_message(message.channel, (
                "Link to Your Chronicle: http://chronicler.seanmfrancis.net/chronicle.php?id={id}&page=1"
                .format(id=message.channel.id)))
            await lib.reaction.reactThumbsUp(client, message)
        elif retval[0] == True:
            await client.send_message(
                message.channel,
                "This Chronicle has been blacklisted. You cannot get its link ever again."
            )
            await lib.reaction.reactThumbsDown(client, message)
    elif rowCount == 0:
        await client.send_message(
            message.channel,
            "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?"
        )
        await lib.reaction.reactThumbsDown(client, message)
