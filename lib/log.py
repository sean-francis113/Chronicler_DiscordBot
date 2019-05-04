import datetime
import lib.db


def logEvent(client, channel, message=None, eType="General", string="", connection=None, close=True):
		"""
		CURRENTLY UNUSED!

		Parameters:
		-----------
		"""

		eventCreator = ""
		eventTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		eventStr = ""

		if message != None:
				eventCreator = message.author.name
				eventStr = str(message.content)
		else:
				eventCreator = "The Chronicler"
				eventStr = string

		lib.db.queryDatabase(
        "INSERT INTO {id}_logs (log_id, log_type, log_creator, log_time, log_content) VALUES ('{creator}', '{time}', '{content}')"
        .format(id=str(channel.id), creator=eventCreator, time=eventTime, content=eventStr),
        client,
        channel,
				conn=connection,
        checkExists=False,
        closeConn=close)