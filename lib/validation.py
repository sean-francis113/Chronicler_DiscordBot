import lib.db


def validateUser(client, message):
    print("Message Author ID: " + message.author.id)

    ignoredID = [client.user]

    rowCount, usersFound, exists = lib.db.queryDatabase(
        "SELECT name,id FROM {id}_ignoredID".format(id=message.channel.id),
        client,
        message.channel,
        checkExists=True,
        tablename="{id}_ignoredID".format(id=message.channel.id),
        getResult=True,
        closeConn=True)

    if exists == True and usersFound != None:
        for found in usersFound:
            print("Ignored User ID: " + found[1])
            ignoredID.append(found[1])

        for user in ignoredID:
            print("Checking User")
            if message.author.id == user:
                print("This Message was written by an ignored user")
                return False

    return True


def checkIfCanPost(client, message):
    rowCount, retval, exists = lib.db.queryDatabase(
        "SELECT is_blacklisted,is_closed FROM chronicles_info WHERE channel_id={id}"
        .format(id=message.channel.id),
        client,
        message.channel,
        checkExists=True,
        tablename="chronicles_info",
        getResult=True,
        closeConn=True)

    if exists == True:
        if retval[0] == False and retval[1] == False:
            return True
        else:
            return False
    else:
        return False
