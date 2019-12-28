import lib.db
import lib.reaction
import lib.error
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
        channel=message.channel,tablename="chronicles_info",
        commit=False,
        getResult=True,
        closeConn=True)

		if(retval is None):
				await lib.message.send(client, message.channel, "We could not find your Chronicle in our database. Has this channel been whitelisted?", feedback=True)
				return	

		retval = list(retval)[0]

		if rowCount > 0:
				if retval[2] == False:
						await lib.message.send(client, message.channel, "Link to Your Chronicle: ", delete=False)
						await lib.message.send(client, message.channel, "{url}/chronicle.php?id={id}&page=1".format(url=os.environ.get("CHRONICLER_WEBSITE_URL"),id=str(message.channel.id)), ignoreStyle=True, delete=False)
						await lib.reaction.reactThumbsUp(client, message)
				elif retval[2] == True:
						#Show Player That The Chronicler Was Unsuccessful
						await lib.reaction.reactThumbsDown(client, message)

						await lib.error.postError(client,		message.channel,
                "This Chronicle has been blacklisted. You cannot get its link ever again."
            )
		else:

				#Show Player That The Chronicler Was Unsuccessful
				await lib.reaction.reactThumbsDown(client, message)

				await lib.error.postError(
						client,
            message.channel,
            "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?"
        )