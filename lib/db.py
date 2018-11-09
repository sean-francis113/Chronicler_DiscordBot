import settings as s
import pymysql.cursors

#Connect to the Database
#Returns: The Database Connection's Cursor
def connectToDatabase():
	conn = pymysql.connect(host=s.database["HOST"], user=s.database["USER"], password=s.database["PASS"], db=s.database["DB"])
							 
	return conn.cursor()
	
#Execute a Query into Database and Return the Result
#cursor: The Database Connection's Cursor
#query: String of the MySQL Query
#wantToCommit: Do We Want to Commit the Query?
#needResult: Do We Need to Get Some Sort of Result?
#Returns: A Tuple of How Many Rows Were Found and The Result of the Query
def queryDatabase(cursor, query, wantToCommit, needResult):
	rowCount = cursor.execute(query)
	
	if wantToCommit == True:
		cursor.commit()
	
	if needResult == True:
		result = cursor.fetchall()
	
	return rowCount, result

#Connects to the Database and Immediately Querys it, Returning the Result.
#query: String Query to send to the database
#wantToCommit: Do We Want to Commit the Query?
#needResult: Do We Need to Get Some Sort of Result?
#Returns: A Tuple of How Many Rows Were Found and The Result of the Query
def connectAndQuery(query, wantToCommit, needResult):
	conn = connectToDatabase()
	c = conn.cursor()
	
	rowCount = c.execute(query)
	
	if wantToCommit == True:
		c.commit()
	
	if needResult == True:
		result = c.fetchall()
	
	return rowCount, result