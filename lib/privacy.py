import lib.db
import lib.reaction
import commandList as cmd


async def setPrivacy(client, message):
		"""
		Set the Privacy of the Channel in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		value = message.content.replace('' + cmd.prefix + ' ' + cmd.set_privacy, '')
		lowerValue = value.lower()
		
		conn = lib.db.connectToDatabase()
		
		if lowerValue.strip() == "true":
        #Update Chronicle in Database
				lib.db.queryDatabase(
            "UPDATE chronicles_info SET is_private=TRUE WHERE channel_id={id};"
            .format(id=str(message.channel.id)),
            client,
            message.channel,
            connection=conn,
            checkExists=True,
            tablename="chronicles_info",
            commit=True,
            closeConn=True)
		elif lowerValue.strip() == "false":
        #Update Chronicle in Database
				lib.db.queryDatabase(
            "UPDATE chronicles_info SET is_private=FALSE WHERE channel_id={id};"
            .format(id=str(message.channel.id)),
            client,
            message.channel,
            connection=conn,
            checkExists=True,
            tablename="chronicles_info",
            commit=True,
            closeConn=True)
						
		await lib.reaction.reactThumbsUp(client, message)
