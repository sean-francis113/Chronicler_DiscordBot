#Import Statements
import lib.db
import lib.reaction
import commandList as cmd


#Blacklists the Chronicle, preventing any interaction from it again
#message: The Message with the Command
#client: The Bot Client
async def blacklistChronicle(client, message):
    #Remove Command From Message
    value = message.content.replace(
        '' + cmd.prefix + ' ' + cmd.blacklist_channel, '')
    #Remove leading and ending whitespace from message
    value = value.strip()
    #If this is not the confirmation command
    #User confirmation is made by adding their channel id at the ned of the message
    if value != message.channel.id:
        await client.send_message(message.channel, (
            "Are you sure you wish to Blacklist this channel? If you do, nothing will ever be recorded from this channel and it will not be seen or accessed on the site! If you are sure about it, type !c blacklist {id}"
            .format(id=message.channel.id)))
    else:
        lib.db.queryDatabase(
            "UPDATE chronicles_info SET is_blacklisted = TRUE WHERE channel_id={id};"
            .format(id=message.channel.id),
            client,
            message.channel,
            checkExists=True,
            tablename="chronicles_info",
            commit=True,
            closeConn=True)

        #Tell the User We're Done
        await lib.reaction.reactThumbsUp(client, message)
