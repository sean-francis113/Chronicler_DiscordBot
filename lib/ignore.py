import lib.db
import lib.reaction
import commandList as cmd


async def sendIgnoreReaction(client, message):
    await lib.reaction.reactThumbsUp(client, message)


async def addUserToIgnoreList(client, message):
    ignoredUsers = []
    dict_user_keys = ["name", "id"]

    value = message.content.replace('' + cmd.prefix + ' ' + cmd.ignore_users,
                                    '')
    usersFound = value.split('|')
    usersInServer = client.get_all_members()
    for user in usersFound:
        strippedUser = user.strip()
        for serverUser in usersInServer:
            if serverUser.nick == strippedUser:
                combination = [serverUser.nick, serverUser.id]
                ignoredUsers.append(dict(zip(dict_user_keys, combination)))
            elif serverUser.name == strippedUser:
                combination = [serverUser.name, serverUser.id]
                ignoredUsers.append(dict(zip(dict_user_keys, combination)))

    conn = lib.db.connectToDatabase()

    #Need to Make Sure Each Message

    for user in ignoredUsers:
        lib.db.queryDatabase(
            "INSERT INTO {channel_id}_ignoredUsers (name, id) VALUES (\"{user_name}\", \"{user_id}\")"
            .format(
                channel_id=message.channel.id,
                user_name=user["name"],
                user_id=user["id"]),
            client,
            message.channel,
            connection=conn,
            commit=False,
            checkExists=True,
            tablename="{channel_id}_ignoredUsers".format(
                channel_id=message.channel.id),
            closeConn=False)
    conn.commit()
    conn.close()

    await lib.reaction.reactThumbsUp(client, message)


#Deletes the Provided Users from the Ignored Users Table, if They Exists
async def removeIgnoredUsers(client, message):
    value = message.content.replace(
        '' + cmd.prefix + ' ' + cmd.remove_ignored_users, '')
    usersFound = value.split('|')

    conn = lib.db.connectToDatabase()

    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT name,id FROM {channel_id}_ignoredUsers".format(
            channel_id=message.channel.id),
        client,
        message.channel,
        connection=conn,
        commit=False,
        checkExists=True,
        tablename="{channel_id}_ignoredUsers".format(
            channel_id=message.channel.id),
        reportExistance=True,
        getResult=False,
        closeConn=False)

    if exists == False:
        return
    elif rowCount == 0:
        await client.send_message(
            message.channel,
            "The Chronicler could not find any users in your Ignored User List."
        )
        return

    serverUsers = client.get_all_members()

    for user in usersFound:
        for sUser in serverUsers:
            if user.strip() == sUser.nick or user.strip() == sUser.name:
                lib.db.queryDatabase(
                    "DELETE FROM {channel_id}_ignoredUsers WHERE id=\"{userID}\""
                    .format(channel_id=message.channel.id, userID=sUser.id),
                    client,
                    message.channel,
                    connection=conn,
                    commit=False,
                    getResult=False,
                    closeConn=False)
                break

    conn.commit()
    conn.close()

    await lib.reaction.reactThumbsUp(client, message)


#Gets the List of Ignored Users, if any, of the Story from the Database
#channel: The Channel to pull the Users from
#Returns: A tuple array of {username, userID}
def getIgnoredUsers(channel, client):
    userList = []
    dict_user_keys = ['name', 'id']
    rowCount, selectedRows, exists = lib.db.queryDatabase(
        "SELECT name,id FROM {id}_ignoredUsers".format(id=channel.id),
        client,
        channel,
        checkExists=True,
        tablename="{id}_ignoredUsers".format(id=channel.id),
        getResult=True,
        closeConn=True)

    if rowCount == 0 or exists == False:
        return userList
    else:
        for row in selectedRows:
            combination = [row[0], row[1]]
            userList.append(dict(zip(dict_user_keys, combination)))
        return userList
