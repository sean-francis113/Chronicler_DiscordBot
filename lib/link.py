import lib.db
import lib.reaction
import os


async def getChronicle(client, message):
		"""
		Function That Generates and Returns a Link to the Story on the Website

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""

		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT * FROM chronicles_info WHERE channel_id={id}".
        format(id=str(message.channel.id)),
        client,
        channel=message.channel,
        checkExists=True,
        tablename="chronicles_info",
        commit=False,
        getResult=True,
        closeConn=True)

		retval = list(retval)[0]

		if rowCount > 0:
				if retval[2] == False:
						await lib.message.send(message.channel, "Link to Your Chronicle: ", delete=False)
						await lib.message.send(message.channel, "{url}/chronicle.php?id={id}&page=1".format(url=os.environ.get("CHRONICLER_WEBSITE_URL"),id=str(message.channel.id)), ignoreStyle=True, delete=False)
						await lib.reaction.reactThumbsUp(client, message)
				elif retval[2] == True:
						await lib.message.send(
                message.channel,
                "This Chronicle has been blacklisted. You cannot get its link ever again."
            )
						await lib.reaction.reactThumbsDown(client, message)
		else:
				await lib.message.send(
            message.channel,
            "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?"
        )
				await lib.reaction.reactThumbsDown(client, message)