import os
import pymysql.cursors
import pymysql.err
import lib.error

#Connect to the Database
#Returns: The Database Connection's Cursor
def connectToDatabase():
	conn = pymysql.connect(
    os.environ.get("CHRONICLER_DATABASE_HOST"), 
    os.environ.get("CHRONICLER_DATABASE_USER"), 
    os.environ.get("CHRONICLER_DATABASE_PASSWORD"), 
    os.environ.get("CHRONICLER_DATABASE_DB")
    )
							 
	return conn
	
#Execute a Query into Database, Connecting if Necessary, and Return the Result
#query: String of the MySQL Query
#client: The Discord Client.
#message: The Message That Caused This Query, if Applicable
#channel: The Channel That Cuased This Query, if Applicable
#connection: The Connection That We Will Use for This Query, if Applicable
#checkExists: Do We Need to Check if the Table Exists?
#tablename: The Name of the Table We Want to Query. Necessary to Confirm Table Exists. Should Try to Find a More Elegant Solution.
#commit: Do We Want to Commit the Query?
#getResult: Do We Need to Get Some Sort of Result?
#Returns: A Tuple of How Many Rows Were Found, The Result of the Query and if Table Exists, rowCount = 0, result=None and exists=False Otherwise
def queryDatabase(query, client, channel=None, connection=None, checkExists=False, tablename=None, reportExistance=False, commit=False, getResult=False, closeConn=True):
	if checkExists == True:
		if (tablename == "" or tablename is None) or checkIfTableExists(connectToDatabase().cursor(), tablename) == False:
			if(reportExistance):
				if(channel != None):
					lib.error.postError(client, channel, "ERROR #1021: If you are seeing this Error Message, please email us immediately by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com. Include this Error Number and what you were doing right before the message.")
			return 0, None, False

	try:

		result = None
		rowCount = 0

		if connection is None:
			connection = connectToDatabase()

		cursor = connection.cursor()
		rowCount = cursor.execute(query)
	
		if getResult == True and rowCount > 0:
			if rowCount == 1:
				result = cursor.fetchone()
			elif rowCount > 1:
				result = cursor.fetchall()

		if commit == True:
			connection.commit()

		cursor.close()

		if closeConn == True:
			connection.close()
	
		return rowCount, result, True

	except pymysql.MySQLError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then something happened with the database operation. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.InterfaceError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then something happened with the Database Interface. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.DatabaseError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then something happened with the Database itself. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.DataError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then what was sent to the database was not valid. In most cases, the message became too long. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.OperationalError:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then something happened that is beyond our control. Unfortunately, in this case, there is nothing that can be done except retry in a few minutes.")

	except pymysql.IntegrityError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then something has happened to the integrity of the Database. Please immediately email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.InternalError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then something has happened internally. Please immediately email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.ProgrammingError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then you managed to find a glitch in the system that we missed. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))

	except pymysql.NotSupportedError as e:
		if(channel != None):
			lib.error.postError(client, channel, "ERROR #{errorNum}: If you are seeing this Error Message, then we are trying to do something that is no longer supported by the Database. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'".format(errorNum=e.args[0], errorMessage=e))


#Checks to See if the Provided Table Exists
#cursor: The Database Connection's Cursor
#tablename: The Name of the Table We Want to Confirm Exists
def checkIfTableExists(cursor, tablename):
	cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = \"{db}\" AND table_name = \"{table}\"
        """.format(db=os.environ.get("CHRONICLER_DATABASE_DB"), table=tablename.replace('\'', '\'\'')))
	if cursor.fetchone()[0] == 1:
		cursor.close()
		return True
	else:
		cursor.close()	
		return False