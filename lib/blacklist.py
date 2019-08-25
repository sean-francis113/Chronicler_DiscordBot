#Import Statements
import lib.db
import lib.reaction
import commandList as cmd


async def blacklistChronicle(client, message):
		"""
		Function That Blacklists the Chronicle/Channel, Preventing Any Interaction Between it and The Chronicler again.

		Parameters:
		-----------
				message (discord.Message)
						The Message That Holds the Command.
				client (discord.Client)
						The Chronicler Client
		"""	

    #Remove Command From Message
		value = message.content.replace(
        cmd.blacklist_channel["command"], '')

    #Remove Leading and Ending Whitespace From Message
		value = value.strip()

		#If This is Not the Confirmation Command
		#User Confirmation is Made By Adding the Channel ID at the End of the Command.
		if value != str(message.channel.id):
				#Confirm With the Player That They Wish to Blacklist the Channel
				await lib.message.send(client, message.channel,
            "Are you sure you wish to Blacklist this channel? If you do, nothing will ever be recorded from this channel and it will not be seen or accessed on the site! If you are sure about it, type !c blacklist {id}"
            .format(id=str(message.channel.id)), time=25.0, feedback=True)


		elif(value != "" and value != str(message.channel.id)):
				#Confirm With the Player That They Wish to Blacklist the Channel
				await lib.message.send(client, message.channel,
            "The provided code is not correct for this channel. If you are sure about blacklisting this channel, type !c blacklist {id}"
            .format(id=str(message.channel.id)), time=25.0, feedback=True)

		#If This is the Confirmation Command
		else:
				#Set is_blacklisted in the Database to True.
				lib.db.queryDatabase(
            "UPDATE chronicles_info SET is_blacklisted = TRUE WHERE channel_id={id};"
            .format(id=str(message.channel.id)),
            client,
            message.channel,
            checkExists=True,
            tablename="chronicles_info",
            commit=True,
            closeConn=True)
						
				#Tell the User We're Done
				await lib.reaction.reactThumbsUp(client, message)