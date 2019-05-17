import lib.db
import lib.reaction
import commandList as cmd


async def addKeyword(client, message):
		"""
		Function That Adds a Keyword and Replacement for the Keyword Into the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message With Keywords to Add
		"""

		#Grab the Keywords and Replacement Strings
		value = message.content.replace('' + cmd.prefix + ' ' + cmd.add_keyword, '')
		keywordValues = value.split('|')
		
		#Connect to Database
		conn = lib.db.connectToDatabase()
		
		#See if We Already Have the Word in the Database
		rowCount, result, exists =  lib.db.queryDatabase(
        "SELECT word FROM {id}_keywords WHERE word=\"{word}\"".format(
            id=str(message.channel.id), word=keywordValues[0].strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_keywords".format(id=str(message.channel.id)),
        getResult=True,
				closeConn=False)
				
		#If the Table Does Not Exist
		if exists == False:
				conn.close()
				return

		#Otherwise
		else:
				#If the Word is Not in the Table
				if rowCount == 0:
						lib.db.queryDatabase(
                "INSERT INTO {id}_keywords (word,replacement) VALUES (\"{word}\", \"{replacement}\")"
                .format(
                    id=str(message.channel.id),
                    word=keywordValues[0].strip(),
                    replacement=keywordValues[1].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_keywords".format(id=str(message.channel.id)),
                commit=True,
								closeConn=False)

				#Otherwise
				else:
						lib.db.queryDatabase(
                "UPDATE {id}_keywords SET replacement=\"{replacement}\" WHERE word=\"{word}\";"
                .format(
                    id=str(message.channel.id),
                    replacement=keywordValues[1].strip(),
                    word=keywordValues[0].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_keywords".format(id=str(message.channel.id)),
                commit=True,
								closeConn=False)
		
		conn.close()
		await lib.reaction.reactThumbsUp(client, message)


async def removeKeyword(client, message):
		"""
		Function That Removes Keyword(s) From the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command and Keywords
		"""

		#Grab the Keyword to Remove From Message
		value = message.content.replace('' + cmd.prefix + ' ' + cmd.remove_keyword, '')

		#Connect to Database
		conn = lib.db.connectToDatabase()

		#Find the Word in the Database
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT word FROM {id}_keywords WHERE word=\"{word}\"".format(
            id=str(message.channel.id), word=value.strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_keywords".format(id=str(message.channel.id)),
        getResult=True,
				closeConn=False)

		#If the Table Does Not Exist
		if exists == False:
				conn.close()
				return
		else:
				if rowCount == 1:
						lib.db.queryDatabase(
                "DELETE FROM {id}_keywords WHERE word=\"{word}\"".format(
                    id=str(message.channel.id), word=value.strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                commit=True,
								closeConn=False)
						await lib.reaction.reactThumbsUp(client, message)
				elif rowCount == 0:
						await lib.reaction.reactThumbsDown(client, message)
						await lib.message.send(
                message.channel,
                "The Chronicler could not find the keyword in its database for this channel. Did you spell it correctly? If you are, make sure it is a keyword that was added to the Chronicle. If you are still having issues, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue.", delete=False
            )
						
				conn.close()


def getKeywords(client, channel):
		"""
		Function That Gets the List of Keywords, if any, of the Channel from the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				channel (discord.TextChannel)
						The Channel to Recieve Keywords From
		"""

		#The List of Words to be Returned
		wordList = []

		#Grab All of the Words in the Database
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT word,replacement FROM {id}_keywords".format(id=channel.id),
        client,
        channel,
        checkExists=True,
        tablename="{id}_keywords".format(id=channel.id),
        getResult=True,
        closeConn=True)
				
		#If There Are No Words In the Database
		if rowCount == 0:
				return wordList

		#Otherwise
		else:
				for row in retval:
						print(row)
						wordList.append((row[0], row[1]))
				return wordList


#Searches through the String, replacing all instances of 'keyword' with 'replacement'
#string: The String to Search Through
#keyword: The string to replace
#replacement: The string to replace 'keyword' with
#Returns: The New String with all replacements made
def replaceKeyword(string, keyword, replacement):
		"""
		Function That Searches Through the String, Replacing All Instances of 'keyword' with 'replacement'

		Parameters:
		-----------
				string (string)
						The String That the Words Will be Replaced From
				keyword (string)
						The Word That Will Be Searched For and Replaced
				replacement (string)
						The String That Will Replaced the keyword
		"""
		
		word = " {word} ".format(word=keyword)
		replace = " {replacement} ".format(replacement=replacement)
		#If We Found the Word With Spaces
		if string.find(word) != -1:
				return string.replace(word, replace)
    #If the String is A Single Word
		elif string.find(" ") == -1:
				return string.replace(keyword, replacement)
    #If We Found the Word Without Spaces
		elif string.find(keyword) != -1:
				return string.replace(keyword, replacement)
    #If We Found Nothing, Return the String Untouched
		else:
				return string
