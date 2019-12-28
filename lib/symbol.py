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
		
		value = message.content.replace(cmd.add_symbol["command"], '')
		symbolValues = value.split('|')
		
		conn = lib.db.connectToDatabase()
		
		dictionary = lib.db.checkIfDataExists(client, message.channel, "%s_ignoredSymbols" %(message.channel.id), start=symbolValues[0])

		if (int(dictionary["start"]) == 0):
				lib.db.queryDatabase(
						"INSERT INTO {id}_ignoredSymbols (start,end) VALUES (\"{start}\", \"{end}\")"
						.format(
								id=str(message.channel.id),
								start=symbolValues[0].strip(),
								end=symbolValues[1].strip()),
						client,
						message.channel,
						connection=conn,
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
		
		value = message.content.replace(cmd.remove_symbol["command"], '')

		conn = lib.db.connectToDatabase()
		
		rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(
            id=str(message.channel.id), start=value.strip()),
        client,
        message.channel,
        connection=conn,
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
								tablename="{id}_ignoredSymbols".format(id=str(message.channel.id)),
								commit=True,
                closeConn=True)

						await lib.reaction.reactThumbsUp(client, message)
						
				elif rowCount == 0:

						#Show Player That The Chronicler Was Unsuccessful
						await lib.reaction.reactThumbsDown(client, message)

						lib.error.postError(client,
								message.channel,
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
		markdownSymbols = [("__***", "<span class=\"italics_bold_underline\">", "</span>"), ("***", "<span class=\"italics_bold\">", "</span>"), ("__**", "<span class=\"bold_underline\">", "</span>"), ("**", "<span class=\"bold\">", "</span>"), ("__*", "<span class=\"italics_underline\">", "</span>"), ("~~", "<span class=\"strikeout\">", "</span>"), ("*", "<span class=\"italics\">", "</span>"), ("__", "<span class=\"underline\">", "</span>")]
		
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
				mdSymbol = symbol[0]
				htmlSymbolLeft = symbol[1]
				htmlSymbolRight = symbol[2]
				while spoilerString.find(mdSymbol, lastPosChecked + 1) != -1:
						firstIndex = spoilerString.find(mdSymbol)
						nextIndex = spoilerString.find(mdSymbol, firstIndex + len(mdSymbol))
						lastPosChecked = firstIndex
						if nextIndex != -1:
								lastPosChecked = nextIndex + len(mdSymbol)
								spoilerStart.append(firstIndex)
								spoilerEnd.append(nextIndex)
								insideString = spoilerString[firstIndex + len(mdSymbol) : nextIndex]
								spoilerString = spoilerString[ : firstIndex] + symbol[1] + insideString + symbol[2] + spoilerString[nextIndex + len(mdSymbol) : ]

		codeString = spoilerString

		#Then Check Codeblocks
		for symbol in codeSymbols:
				lastPosChecked = 0
				mdSymbol = symbol[0]
				htmlSymbolLeft = symbol[1]
				htmlSymbolRight = symbol[2]
				#Run Functions for Multiline Code Blocks
				while codeString.find(mdSymbol, lastPosChecked + 1) != -1:
						firstIndex = codeString.find(mdSymbol)
						nextIndex = codeString.find(mdSymbol, firstIndex + len(mdSymbol))
						lastPosChecked = firstIndex
						if nextIndex != -1:
								lastPosChecked = nextIndex + len(mdSymbol)
								if len(spoilerStart) == 0 or len(spoilerEnd) == 0:
										insideString = codeString[firstIndex + len(mdSymbol) : nextIndex]
										codeString = codeString[:firstIndex] + symbol[1] + insideString + symbol[2] + codeString[nextIndex + len(mdSymbol):]
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
												insideString = codeString[firstIndex + len(mdSymbol) : nextIndex]
												codeString = codeString[:firstIndex] + symbol[1] + insideString + symbol[2] + codeString[nextIndex + len(mdSymbol):]

		markdownString = codeString

		#Finally Check Remaining Markdown
		for symbol in markdownSymbols:
				lastPosChecked = 0
				mdSymbol = symbol[0]
				htmlSymbolLeft = symbol[1]
				htmlSymbolRight = symbol[2]
				while markdownString.find(mdSymbol, lastPosChecked + 1) != -1:
						firstIndex = markdownString.find(mdSymbol)
						nextIndex = markdownString.find(mdSymbol, firstIndex + len(mdSymbol))
						lastPosChecked = firstIndex
						i = 0
						if nextIndex != -1:
							lastPosChecked = nextIndex + len(mdSymbol)
							if len(codeStart) == 0 or len(codeEnd) == 0:
									insideString = markdownString[firstIndex + len(mdSymbol) : nextIndex]
									markdownString = markdownString[:firstIndex] + symbol[1] + insideString + symbol[2] + markdownString[nextIndex + len(mdSymbol):]
							else:
								while i < len(codeStart) and i < len(codeEnd):
										#If Either symbol is Within the specified Code Block
										if (firstIndex > codeStart[i] and firstIndex < codeEnd[i]) and (nextIndex > codeStart[i] and nextIndex < codeEnd[i]):
												i += 1

										else:		
												if i == len(codeStart) or i == len(codeEnd):
														
														insideString = markdownString[firstIndex + len(mdSymbol) : nextIndex]
														markdownString = markdownString[:firstIndex] + symbol[1] + insideString + symbol[2] + markdownString[nextIndex + len(mdSymbol):]
														
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
				tablename="{id}_ignoredSymbols".format(id=channel.id),
        getResult=True,
        closeConn=True)
				
		if rowCount == 0:
				return symbolList
    
		else:
				for row in retval:
						symbolList.append((row[0], row[1]))
				return symbolList

async def clearList(client, message):
		lib.db.queryDatabase(
                "DELETE FROM {id}_ignoreSymbols".format(
                    id=str(message.channel.id)),
                client,
                message.channel, 
                commit=False,
								tablename="{id}_ignoredSymbols".format(id=str(message.channel.id)),
								closeConn=True)