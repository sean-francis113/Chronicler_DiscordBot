import os
import pymysql.cursors

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
#cursor: The Database Connection's Cursor
#checkExists: Do We Need to Check if the Table Exists?
#tablename: The Name of the Table We Want to Query. Necessary to Confirm Table Exists. Should Try to Find a More Elegant Solution.
#commit: Do We Want to Commit the Query?
#getResult: Do We Need to Get Some Sort of Result?
#Returns: A Tuple of How Many Rows Were Found, The Result of the Query and if Table Exists, rowCount = 0, result=None and exists=False Otherwise
def queryDatabase(query, connection=None, checkExists=True, tablename=None, commit=False, getResult=False, closeConn=True):
	if checkExists == True:
		if (tablename == "" or tablename is None) or checkIfTableExists(connectToDatabase().cursor(), tablename) == False:
			print("Table {tablename} Does Not Exist!".format(tablename=tablename))
			return 0, None, False

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
		print("At getResult: {result}".format(result=result))
	
	if commit == True:
		connection.commit()

	cursor.close()

	if closeConn == True:
		connection.close()
	
	return rowCount, result, True

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