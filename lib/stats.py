import discord
import lib.db
import lib.reaction

async def displayChannelStats(message, client):
	rowCount, retval, exists = lib.db.queryDatabase("SELECT * FROM chronicles_info WHERE channel_id = {id}".format(id=message.channel.id), checkExists=True, tablename="chronicles_info", getResult=True, commit=False, closeConn=True)
	
	if exists == False:
		await lib.reaction.reactThumbsDown(message, client)
		await client.send_message(message.channel, "The Chronicler could not find the table. Please immediately either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue adding the following: ERROR 500: displayChannelStatus() QUERY: SELECT * FROM chronicles_info WHERE channel_id = {id}".format(id=message.channel.id))
		return		
	else:
		if rowCount == 0:
			await client.send_message(message.channel, "The Chronicler could not find this channel in its database. Has this channel been created for or added into the database?")
		else:
			if retval['is_blacklisted'] == True:
				await client.send_message(message.channel, "This channel has been blacklisted. You can no longer get its stats.")
			else:
				rowCount, contentData, exists = lib.db.queryDatabase("SELECT * FROM {id}_contents".format(id=message.channel.id), checkExists=True, tablename="{id}_contents".format(id=message.channel.id), closeConn=True)
				
				messageStr = ('Stats for ' + message.channel.name + '/n/n'
      	'Is Closed = ' + str(retval['is_closed']) + '\n'
      	'Is Private = ' + str(retval['is_private']) + '\n'
      	'Channel ID = ' + retval['channel_id'] + '\n'
      	'Channel Creator = ' + retval['channel_owner'] + '\n'
      	'Has Warnings = ' + str(retval['has_warnings']) + '\n'
      	'Warning List = ' + retval['warning_list'] + '\n'
      	'Date Last Modified = ' + retval['date_last_modified'] + '\n'
      	'Character Count = ' + str(contentData['char_count']) + '\n'
				'Word Count = ' + str(contentData['word_count']))
				
			await client.send_message(message.channel, messageStr)
			await lib.reaction.reactThumbsUp(message, client)