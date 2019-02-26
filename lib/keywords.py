import lib.db
import lib.reaction
import commandList as cmd


async def addKeyword(client, message):
    value = message.content.replace('' + cmd.prefix + ' ' + cmd.add_keyword,
                                    '')
    keywordValues = value.split('|')

    conn = lib.db.connectToDatabase()

    rowCount, result, exists = lib.db.queryDatabase(
        "SELECT word FROM {id}_keywords WHERE word=\"{word}\"".format(
            id=message.channel.id, word=keywordValues[0].strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_keywords".format(id=message.channel.id),
        getResult=True)

    if exists == False:
        conn.close()
        return
    else:
        if rowCount == 0:
            lib.db.queryDatabase(
                "INSERT INTO {id}_keywords (word,replacement) VALUES (\"{word}\", \"{replacement}\")"
                .format(
                    id=message.channel.id,
                    word=keywordValues[0].strip(),
                    replacement=keywordValues[1].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_keywords".format(id=message.channel.id),
                commit=True)
        else:
            lib.db.queryDatabase(
                "UPDATE {id}_keywords SET replacement=\"{replacement}\" WHERE word=\"{word}\";"
                .format(
                    id=message.channel.id,
                    replacement=keywordValues[1].strip(),
                    word=keywordValues[0].strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                tablename="{id}_keywords".format(id=message.channel.id),
                commit=True)

    conn.close()
    await lib.reaction.reactThumbsUp(client, message)


async def removeKeyword(client, message):
    value = message.content.replace('' + cmd.prefix + ' ' + cmd.remove_keyword,
                                    '')

    conn = lib.db.connectToDatabase()

    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT word FROM {id}_keywords WHERE word=\"{word}\"".format(
            id=message.channel.id, word=value.strip()),
        client,
        message.channel,
        connection=conn,
        checkExists=True,
        tablename="{id}_keywords".format(id=message.channel.id),
        getResult=True)

    if exists == False:
        conn.close()
        return
    else:
        if rowCount == 1:
            lib.db.queryDatabase(
                "DELETE FROM {id}_keywords WHERE word=\"{word}\"".format(
                    id=message.channel.id, word=value.strip()),
                client,
                message.channel,
                connection=conn,
                checkExists=False,
                commit=True)
            await lib.reaction.reactThumbsUp(client, message)
        elif rowCount == 0:
            await lib.reaction.reactThumbsDown(client, message)
            await client.send_message(
                message.channel,
                "The Chronicler could not find the keyword in its database for this channel. Did you spell it correctly? If you are, make sure it is a keyword that was added to the Chronicle. If you are still having issues, please either use our contact form at chronicler.seanmfrancis.net/contact.php or email us at thechroniclerbot@gmail.com detailing your issue."
            )

    conn.close()


#Gets the List of Keywords, if any, of the Story from the Database
#channel: The Channel to pull the Keywords from
#Returns: An tuple array of {keyword, replacement_string}
def getKeywords(client, channel):
    wordList = []
    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT word,replacement FROM {id}_keywords".format(id=channel.id),
        client,
        channel,
        checkExists=True,
        tablename="{id}_keywords".format(id=channel.id),
        getResult=True,
        closeConn=True)

    if rowCount == 0:
        return wordList
    else:
        i = 0
        if (rowCount == 1):
            while i < len(retval):
                combination = (retval[i], retval[i + 1])
                wordList.append(combination)
                i += 2
        else:
            while i < rowCount:
                wordList.append(retval[i])
                i += 1
        return wordList


#Searches through the String, replacing all instances of 'keyword' with 'replacement'
#string: The String to Search Through
#keyword: The string to replace
#replacement: The string to replace 'keyword' with
#Returns: The New String with all replacements made
def replaceKeyword(string, keyword, replacement):
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
