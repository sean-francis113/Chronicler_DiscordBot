#Import Statements
import lib.db
import commandList as cmd


def updateChannel(client, before, after):
		"""
		Function That Updates the Information Within the Database Based on Changes to the Channel.

		Parameters:
		-----------
				client (discord.Client): The Chronicler Client
				before (discord.abc.GuildChannel): The Channel Before Editting
				after (discord.abc.GuildChannel): The Channel After Editting
		"""

		#Update Channel Information in the Database
		lib.db.queryDatabase("UPDATE chronicles_info SET is_NSFW={NSFW} WHERE channel_id={id};". format(
				NSFW=after.is_nsfw(),
				id=str(after.id)
		), 
		client,
    before,
		tablename="chronicles_info",
    commit=True,
    closeConn=True)


def changeName(client, channel, message):
		"""
		Function That Updates the Channel's Name Within the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				channel (discord.TextChannel)
						The Channel to be Renamed
				message (discord.Message)
						The Message With the Command
		"""

		#Grab the Value of the Command
		value = message.content.replace(cmd.rename_channel["command"], '').strip()

		#Update the Channel in the Database
		lib.db.queryDatabase("UPDATE chronicles_info SET channel_name=\"{name}\" WHERE channel_id={id};". format(
				name=value,
				id=str(channel.id)
		), 
		client,
    channel,
    tablename="chronicles_info",
    commit=True,
    closeConn=True)