#Import Statements
import os
import pymysql.cursors
import pymysql.err
import lib.error
import lib.log
import datetime
from inspect import signature


def connectToDatabase():
    """
		Function That Connects to the Database
		"""

    #Connect to Database With Environment Values
    conn = pymysql.connect(
        host=os.environ.get("CHRONICLER_DATABASE_HOST"),
        user=os.environ.get("CHRONICLER_DATABASE_USER"),
        passwd=os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
        db=os.environ.get("CHRONICLER_DATABASE_DB"),
				charset="utf8mb4")

    #Return the Connection
    return conn


def queryDatabase(query,
                  client,
                  channel,
                  connection=None,
                  tablename=None,
                  reportExistance=False,
									ignoreExistance=False,
                  commit=False,
                  getResult=False,
                  closeConn=True):
		"""
		Execute a Query into Database, Connecting if Necessary, and Return the Result if Desired

		Parameters:
		-----------
				query (string)
						String of the MySQL Query
				client (discord.Client)
						The Chronicler Client
				channel (discord.TextChannel)
						The Channel of the Messasge That Sent the Query/Command
				connection (pymysql.connections.Connection, OPTIONAL)
						The Connection to the Database. If Not Provided, a Connection Will Be Made Before Making the Query
				tablename (string)
						The Name of the Table That We Should Check the Existance of
				reportExistance (boolean, OPTIONAL)
						Should We Tell the User if the Table Does Not Exist
				ignoreExistance (boolean, OPTIONAL)
						Should We Ignore the Result of Checking if the Table Exists
				commit (boolean, OPTIONAL)
						If We Should Commit the Query to the Database
				getResult (boolean, OPTIONAL)
						If We Should Get the Results of the Query
				closeConn (boolean, OPTIONAL)
						If We Should Close the Connection Once We Are Done With the Query
		"""
		
		if(ignoreExistance == False):
				if (tablename == "" or tablename is None) or checkIfTableExists(
									connectToDatabase().cursor(), tablename) == False:
						if (reportExistance):
								if (channel != None):

										lib.error.postError(
												client, channel,
												"ERROR #1021: If you are seeing this Error Message, please contact us immediately by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com. Include this Error Number and what you were doing right before the message."
										)
										
						return 0, None, False
						
		try:
			
				result = None
				rowCount = 0
				
				if connection == None:
						connection = connectToDatabase()
						
				cur = connection.cursor()			
				rowCount = cur.execute(query)
				
				if getResult == True and rowCount > 0:
						result = cur.fetchall()
						
				if commit == True:
						connection.commit()
						
				cur.close()
				
				if closeConn == True:
						connection.close()
				
				return rowCount, result, True
				
		except pymysql.MySQLError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then something happened with the database operation. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.InterfaceError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then something happened with the Database Interface. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.DatabaseError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then something happened with the Database itself. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.DataError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then what was sent to the database was not valid. In most cases, the message became too long. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.OperationalError:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then something happened that is beyond our control. Unfortunately, in this case, there is nothing that can be done except retry in a few minutes."
            )
						
		except pymysql.IntegrityError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then something has happened to the integrity of the Database. Please immediately email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.InternalError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then something has happened internally. Please immediately email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.ProgrammingError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then you managed to find a glitch in the system that we missed. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))
								
		except pymysql.NotSupportedError as e:
				if (channel != None):
						lib.error.postError(
                client, channel,
                "ERROR #{errorNum}: If you are seeing this Error Message, then we are trying to do something that is no longer supported by the Database. Please email us by either using our online form (chronicler.seanmfrancis.net/contact.php) or emailing directly to thechroniclerbot@gmail.com and we will get to it as soon as possible. Include the following in the email: '{errorMessage}'"
                .format(errorNum=e.args[0], errorMessage=e))


def checkIfTableExists(cursor, tablename):
    """
		Function That Checks to See if the Provided Table Exists

		Parameters:
		-----------
				cursor (pymysql.connections.Cursor)
						The MySQL Connection's Cursor
				tablename (string)
						The Name of the Table We Want to Check
		"""

    #Query the Database
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = \"{db}\" AND table_name = \"{table}\"
        """.format(
        db=os.environ.get("CHRONICLER_DATABASE_DB"),
        table=tablename.replace('\'', '\'\'')))

    #If We Find the Table
    if cursor.fetchone()[0] == 1:
        cursor.close()
        return True

    #Otherwise
    else:
        cursor.close()
        return False

#Check to See if Provided Data Exists. Data Keys Must Be Data Column Name, Their Values the Data We Are Checking. Returns Dictionary with Each Keyword's RowCount
def checkIfDataExists(client, channel, tablename, **kwargs):
		sig = signature(checkIfDataExists)

		#If No Keywords Were Added to Function
		if(len(sig.parameters) == 3):
				return

		dictionary = {}

		query = "SELECT * FROM %s WHERE" %(tablename)

		#Look Through Keyword Arguments
		for key, value in kwargs.items():

				#Format Strings Properly For DB Query
				if isinstance(value, str):
						value = "\"%s\"" %(value)

				fullQuery = query + " %s=%s;" %(key, value)
				
				rowCount, retval, exists = queryDatabase(fullQuery, client, channel, getResult=True, tablename=tablename)

				dictionary["%s" %(key)] = "%s" %(rowCount)

		return dictionary

def updateModifiedTime(client, channel):
		"""
		Function That Updates the Channel's Date Last Modified Field in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				channel (discord.TextChannel)
						The Channel That Will Have its Time Updated
		"""

		try:

				queryDatabase(
						"UPDATE chronicles_info SET date_last_modified=\"{time}\" WHERE channel_id=\"{id}\";"
						.format(
								time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
								id=channel.id),
						client,
						channel,
						tablename="chronicles_info",
						reportExistance=True,
						commit=True,
						closeConn=True)

		except:
				return

#Close All Connections to Database
def closeAll(cursor, connection):
		cursor.close()
		connection.close()