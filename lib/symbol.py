import lib.reaction
import commandList as cmd


async def addSymbol(client, message):
		"""
		Functions That Adds a Symbol in the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		value = message.content.replace('' + cmd.prefix + ' ' + cmd.add_symbol, '')
		symbolValues = value.split('|')
		
		conn = lib.db.connectToDatabase()
		
		rowCount, result, exists = lib.db.queryDatabase(
        "SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(
            id=str(message.channel.id), start=symbolValues[0].strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_ignoredSymbols".format(id=str(message.channel.id)),
        getResult=True,
        closeConn=False)
				
		if exists == False:
				conn.close()
				return
				
		else:
				if rowCount == 0:
						lib.db.queryDatabase(
                "INSERT INTO {id}_ignoredSymbols (start,end) VALUES (\"{start}\", \"{end}\")"
                .format(
                    id=str(message.channel.id),
                    start=symbolValues[0].strip(),
                    end=symbolValues[1].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_ignoredSymbols".format(id=str(message.channel.id)),
                commit=True,
                closeConn=True)
				else:
						lib.db.queryDatabase(
                "UPDATE {id}_ignoredSymbols SET end=\"{end}\" WHERE start=\"{start}\""
                .format(
                    id=str(message.channel.id),
                    start=symbolValues[0].strip(),
                    end=symbolValues[1].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_ignoredSymbols".format(id=str(message.channel.id)),
                commit=True,
                closeConn=True)
								
		await lib.reaction.reactThumbsUp(client, message)


async def removeSymbol(client, message):
		"""
		Functions That Removes a Symbol to Remove

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		value = message.content.replace('' + cmd.prefix + ' ' + cmd.remove_symbol, '')

		conn = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(
            id=str(message.channel.id), start=value.strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_ignoredSymbols".format(id=str(message.channel.id)),
        getResult=True,
        closeConn=False)

		if exists == False:
				conn.close()
				return
				
		else:
				if rowCount == 1:
						lib.db.queryDatabase(
                "DELETE FROM {id}_ignoredSymbols WHERE start=\"{start}\"".
                format(id=str(message.channel.id), start=value.strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                commit=True,
                closeConn=True)
						await lib.reaction.reactThumbsUp(client, message)
						
				elif rowCount == 0:
						await lib.reaction.reactThumbsDown(client, message)
						await lib.message.send(message.channel,
                "The Chronicler could not find the symbol in its database for this channel."
            )

def replaceMarkdown(string):
		"""
		Functions That Replaces the Markdown in the String with HTML tags

		Parameters:
		-----------
				string (string)
						The String to Remove the Markdown From
		"""

		# Current Markdown Known (as of 4/24/2019)
		# * = Italics
		# ** = Bold
		# *** = Bold Italics
		# _ = Underline
		# _* = Underline Italics
		# _** = Underline Bold
		# _*** = Underline Bold Italics
		# ~~ = Strikethrough
		# ` = One Line Code
		# ``` = Multiline Code
		# || = Spoiler

		#Ordered by Symbol Priority
		spoilerSymbols = [("||", "<span class=\"spoiler\">", "</span>")]
		codeSymbols = [("```", "<span class=\"multilinecode\">", "</span>"), ("`", "<span class=\"singlelinecode\">", "</span>")]
		markdownSymbols = [("_***", "<span class=\"italics_bold_underline\">", "</span>"), ("***", "<span class=\"italics_bold\">", "</span>"), ("_**", "<span class=\"bold_underline\">", "</span>"), ("**", "<span class=\"bold\">", "</span>"), ("_*", "<span class=\"italics_underline\">", "</span>"), ("~~", "<span class=\"strikeout\">", "</span>"), ("*", "<span class=\"italics\">", "</span>"), ("_", "<span class=\"underline\">", "</span>")]
		
		spoilerString = string
		codeString = ""
		markdownString = ""
		
		spoilerStart = []
		spoilerEnd = []
		codeStart = []
		codeEnd = []

		# First Check for Spoilers
		for symbol in spoilerSymbols:
				lastPosChecked = 0
				while spoilerString.find(symbol[0], lastPosChecked + 1) != -1:
						firstIndex = spoilerString.find(symbol[0])
						nextIndex = spoilerString.find(symbol[0], firstIndex + len(symbol[0]))
						lastPosChecked = firstIndex
						if nextIndex != -1:
								lastPosChecked = nextIndex + len(symbol[0])
								spoilerStart.append(firstIndex)
								spoilerEnd.append(nextIndex)
								insideString = spoilerString[firstIndex + len(symbol[0]) : nextIndex]
								spoilerString = spoilerString[ : firstIndex] + symbol[1] + insideString + symbol[2] + spoilerString[nextIndex + len(symbol[0]) : ]

		codeString = spoilerString

		#Then Check Codeblocks
		for symbol in codeSymbols:
				lastPosChecked = 0
				#Run Functions for Multiline Code Blocks
				while codeString.find(symbol[0], lastPosChecked + 1) != -1:
						firstIndex = codeString.find(symbol[0])
						nextIndex = codeString.find(symbol[0], firstIndex + len(symbol[0]))
						lastPosChecked = firstIndex
						if nextIndex != -1:
								lastPosChecked = nextIndex + len(symbol[0])
								if len(spoilerStart) == 0 or len(spoilerEnd) == 0:
										insideString = codeString[firstIndex + len(symbol[0]) : nextIndex]
										codeString = codeString[:firstIndex] + symbol[1] + insideString + symbol[2] + codeString[nextIndex + len(symbol[0]):]
								else:
										i = 0
										validSpot = False
										while i < len(spoilerStart) and i < len(spoilerEnd):
												# Ensure That All of the Symbols Are Either Within Or Without the Spoiler Tags
												if ((firstIndex > spoilerStart[i] and firstIndex < spoilerEnd[i]) and (nextIndex > spoilerStart[i] and nextIndex < spoilerEnd[i])) or (firstIndex < spoilerStart[i] and nextIndex < spoilerStart[i]) or (firstIndex > spoilerEnd[i] and nextIndex > spoilerEnd[i]):
														i += 1
														validSpot = True
												else:		
														i += 1

										if validSpot == True:
												insideString = codeString[firstIndex + len(symbol[0]) : nextIndex]
												codeString = codeString[:firstIndex] + symbol[1] + insideString + symbol[2] + codeString[nextIndex + len(symbol[0]):]

		markdownString = codeString

		#Finally Check Remaining Markdown
		for symbol in markdownSymbols:
				lastPosChecked = 0
				while markdownString.find(symbol[0], lastPosChecked + 1) != -1:
						firstIndex = markdownString.find(symbol[0])
						nextIndex = markdownString.find(symbol[0], firstIndex + len(symbol[0]))
						lastPosChecked = firstIndex
						i = 0
						if nextIndex != -1:
							lastPosChecked = nextIndex + len(symbol[0])
							if len(codeStart) == 0 or len(codeEnd) == 0:
									insideString = markdownString[firstIndex + len(symbol[0]) : nextIndex]
									markdownString = markdownString[:firstIndex] + symbol[1] + insideString + symbol[2] + markdownString[nextIndex + len(symbol[0]):]
							else:
								while i < len(codeStart) and i < len(codeEnd):
										#If Either symbol is Within the specified Code Block
										if (firstIndex > codeStart[i] and firstIndex < codeEnd[i]) and (nextIndex > codeStart[i] and nextIndex < codeEnd[i]):
												i += 1

										else:		
												if i == len(codeStart) or i == len(codeEnd):
														
														insideString = markdownString[firstIndex + len(symbol[0]) : nextIndex]
														markdownString = markdownString[:firstIndex] + symbol[1] + insideString + symbol[2] + markdownString[nextIndex + len(symbol[0]):]
														
														break
												else:
														i += 1

		return markdownString


def pluckSymbols(string, start, end, removeInside=True):
		"""
		Functions That Pulls the Symbols from the String

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Held the Command
		"""
		
		strToEdit = string
		startIndex = strToEdit.find(start)
		
		if startIndex > -1:
				endIndex = strToEdit.find(end)
				if endIndex > startIndex:
						if removeInside == True:
								strToEdit = strToEdit[:startIndex] + strToEdit[
                    (endIndex + len(end)):]
						else:
								strToEdit = strToEdit[:startIndex] + strToEdit[
                    (startIndex + len(start)):endIndex] + strToEdit[
                        (endIndex + len(end)):]
						strToEdit = pluckSymbols(' '.join(strToEdit.split()), start, end)
		return strToEdit


def getSymbols(client, channel):
		"""
		Functions That Gets the Symbols from the Database

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				channel (discord.Channel)
						The Channel to Get the Symbols For
		"""
		
		symbolList = []
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT start,end FROM {id}_ignoredSymbols".format(id=channel.id),
        client,
        channel,
        checkExists=True,
        tablename="{id}_ignoredSymbols".format(id=channel.id),
        getResult=True,
        closeConn=True)
				
		if rowCount == 0:
				return symbolList
    
		else:
				for row in retval:
						symbolList.append((row[0], row[1]))
				return symbolList