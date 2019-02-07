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

def findMarkdown(string):
		#Current Markdown (as of 2/7/2019)
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
		markdownSymbols = ["*", "**","***", "_", "_*", "_**", "_***", "~~"]
		codeSymbols = ["`", "```"]
		codeStart = -1
		codeEnd = -1

		for symbol in codeSymbols:
				codeStart = string.find(symbol)
				if codeStart > -1:
					codeEnd = string.find(string[codeStart:])
					if codeEnd > -1:
						string.replace(string[codeStart:codeStart + (len(symbol) - 1)], "<code>")
						string.replace(string[codeEnd:codeEnd + (len(symbol - 1))], "</code>")

						



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
