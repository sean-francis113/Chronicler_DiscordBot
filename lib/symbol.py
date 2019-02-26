import lib.reaction
import commandList as cmd


async def addSymbol(client, message):
    value = message.content.replace('' + cmd.prefix + ' ' + cmd.add_symbol, '')
    symbolValues = value.split('|')

    conn = lib.db.connectToDatabase()

    rowCount, result, exists = lib.db.queryDatabase(
        "SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(
            id=message.channel.id, start=symbolValues[0].strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_ignoredSymbols".format(id=message.channel.id),
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
                    id=message.channel.id,
                    start=symbolValues[0].strip(),
                    end=symbolValues[1].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_ignoredSymbols".format(id=message.channel.id),
                commit=True,
                closeConn=True)
        else:
            lib.db.queryDatabase(
                "UPDATE {id}_ignoredSymbols SET end=\"{end}\" WHERE start=\"{start}\""
                .format(
                    id=message.channel.id,
                    start=symbolValues[0].strip(),
                    end=symbolValues[1].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_ignoredSymbols".format(id=message.channel.id),
                commit=True,
                closeConn=True)

    await lib.reaction.reactThumbsUp(client, message)


async def removeSymbol(client, message):
    value = message.content.replace('' + cmd.prefix + ' ' + cmd.remove_keyword,
                                    '')

    conn = lib.db.connectToDatabase()

    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT start FROM {id}_ignoredSymbols WHERE start=\"{start}\"".format(
            id=message.channel.id, start=value.strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_ignoredSymbols".format(id=message.channel.id),
        getResult=True,
        closeConn=False)

    if exists == False:
        conn.close()
        return
    else:
        if rowCount == 1:
            lib.db.queryDatabase(
                "DELETE FROM {id}_ignoredSymbols WHERE start=\"{start}\"".
                format(id=message.channel.id, start=value.strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                commit=True,
                closeConn=True)
            await lib.reaction.reactThumbsUp(client, message)
        elif rowCount == 0:
            await lib.reaction.reactThumbsDown(client, message)
            await client.send_message(
                message.channel,
                "The Chronicler could not find the symbol in its database for this channel. Did you type it correctly? If you are, make sure it is a symbol that was added to the Chronicle. If you are still having issues, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue."
            )

def replaceMarkdown(string):
		#Current Markdown Known (as of 2/7/2019)
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
		codeSymbols = [('```', "<span class=\"multilinecode\">", "</span>"), ('`', "<span class=\"singlelinecode\">", "</span>")]
		markdownSymbols = [('_***', "<span class=\"italics_bold_underline\">", "</span>"), ('***', "<span class=\"italics_bold\">", "</span>"), ('_**', "<span class=\"bold_underline\">", "</span>"), ('**', "<span class=\"bold\">", "</span>"), ('_*', "<span class=\"italics_underline\">", "</span>"), ('~~', "<span class=\"strikeout\">", "</span>"), ('||', "<span class=\"spoiler\">", "</span>"), ('*', "<span class=\"italics\">", "</span>"), ('_', "<span class=\"underline\">", "</span>")]
		
		codeString = string
		markdownString = ""
		
		codeStart = []
		codeEnd = []

		print("String To Check Markdown: " + codeString)

		for symbol in codeSymbols:
				#Run Functions for Multiline Code Blocks
				while codeString.find(symbol[0]) > -1:
						print("Found Code Symbol")
						firstSymbol = codeString.find(symbol[0])
						nextSymbol = codeString.find(symbol[0], firstSymbol + len(symbol[0]))
						if nextSymbol > -1:
								codeStart.append(firstSymbol)
								codeEnd.append(nextSymbol)
								insideString = codeString[firstSymbol + len(symbol[0]) : nextSymbol]
								codeString = codeString[:firstSymbol] + symbol[1] + insideString + symbol[2] + codeString[firstSymbol + len(symbol[0]) : nextSymbol + len(symbol[0])]						

		print("String After Code Markdown: " + codeString)

		markdownString = codeString

		for symbol in markdownSymbols:
				while markdownString.find(symbol[0]) != -1:
						print("Found \'" + symbol[0] + "\' in string: " + markdownString)
						symbolStart = markdownString.find(symbol[0])
						symbolEnd = markdownString.find(symbol[0], symbolStart + len(symbol[0]))
						#If We Found Symbol AND It is Not Within a Code Block
						i = 0
						while i < len(codeStart) and i < len(codeEnd):
								#If Either Symbol is Within the specified Code Block
								if (symbolStart > codeStart[i] and symbolStart < codeEnd[i]) or (symbolEnd > codeStart[i] and symbolEnd < codeEnd[i]):
										i += 1
								else:
										insideString = markdownString[symbolStart + len(symbol[0]) : symbolEnd]
										markdownString = markdownString[:symbolStart] + symbol[1] + insideString + symbol[2] + markdownString[symbolStart + len(symbol[0]) : symbolEnd + len(symbol[0])]
										break

		print("String After Other Markdown: " + markdownString)

		return markdownString


def pluckSymbols(string, start, end, removeInside=True):
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
        i = 0
        if (rowCount == 1):
            while i < len(retval):
                combination = (retval[i], retval[i + 1])
                symbolList.append(combination)
                i += 2
        else:
            while i < rowCount:
                symbolList.append(retval[i])
                i += 1
        return symbolList
