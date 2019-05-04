#Import Statements
import os
import pymysql.cursors
import pymysql.err
import lib.error
import lib.log
import datetime


def connectToDatabase():
    """
		Function That Connects to the Database
		"""

    #Connect to Database With Environment Values
    conn = pymysql.connect(
        os.environ.get("CHRONICLER_DATABASE_HOST"),
        os.environ.get("CHRONICLER_DATABASE_USER"),
        os.environ.get("CHRONICLER_DATABASE_PASSWORD"),
        os.environ.get("CHRONICLER_DATABASE_DB"))

    #Return the Connection
    return conn


def queryDatabase(query,
                  client,
                  channel,
                  connection=None,
                  checkExists=False,
                  tablename=None,
                  reportExistance=False,
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
				checkExists (boolean, OPTIONAL)
						If We Should Check That the Table Exists or Not. If Used, MUST Have Something in tablename.
				tablename (string, MOSTLY OPTIONAL)
						The Name of the Table That We Should Check the Existance of (Only Matters if checkExists is True)
				reportExistance (boolean, OPTIONAL)
						Should We Tell the User if the Table Does Not Exist
				commit (boolean, OPTIONAL)
						If We Should Commit the Query to the Database
				getResult (boolean, OPTIONAL)
						If We Should Get the Results of the Query
				closeConn (boolean, OPTIONAL)
						If We Should Close the Connection Once We Are Done With the Query
		"""

    if checkExists == True:
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

    queryDatabase(
        "UPDATE chronicles_info SET date_last_modified=\"{time}\" WHERE channel_id=\"{id}\";"
        .format(
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            id=channel.id),
        client,
        channel,
        checkExists=True,
        tablename="chronicles_info",
        reportExistance=True,
        commit=True,
        closeConn=True)
