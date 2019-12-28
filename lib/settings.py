import lib.db
import lib.message

def checkSettings(client, channel):
		conn = lib.db.connectToDatabase()

		rowCount, result, exists = lib.db.queryDatabase("SELECT * FROM chronicler_settings WHERE channel_id={id}".format(id=str(channel.id)), client, channel, connection=conn, getResult=True, tablename="chronicler_settings", closeConn=False)

		if rowCount == 0 or result == None:
				lib.db.queryDatabase("INSERT INTO chronicler_settings (channel_id, feedback, channel_ignore) VALUES (\"{id}\", \"Full\", \"FALSE\")".format(id=channel.id), client, channel, connection=conn, getResult=True, tablename="chronicler_settings", closeConn=False)
				
				rowCount, result, exists = lib.db.queryDatabase("SELECT * FROM chronicler_settings WHERE channel_id = {id}".format(id=channel.id), client, channel, connection=conn, getResult=True, tablename="chronicler_settings", closeConn=True)
				
				return result
		
		else:
				conn.close()
				return result

def setFeedback(client, channel, value):
		checkSettings(client, channel)
		
		lib.db.queryDatabase("UPDATE chronicler_settings SET feedback=\"{val}\" WHERE channel_id={id}".format(val=value, id=channel.id), client, channel)

def setIgnore(client, channel, value):
		checkSettings(client, channel)

		lib.db.queryDatabase("UPDATE chronicler_settings SET channel_ignore={val} WHERE channel_id={id}".format(val=value, id=channel.id), client, channel)