#Import Statements
import discord
import lib.db

#Blacklists the Chronicle, preventing any interaction from it again
#message: The Message with the Command
#client: The Bot Client
async def blacklistChronicle(message, client):
  #Remove Command From Message
  value = message.content.replace("!c blacklist", '')
  #Remove leading and ending whitespace from message
  value = value.strip()
  #If this is not the confirmation command
  #User confirmation is made by adding their channel id at the ned of the message
  if value != message.channel.id:
    await client.send_message(message.channel, ("Are you sure you wish to Blacklist this channel? If you do, nothing will ever be recorded from this channel and it will not be seen or accessed on the site! If you are sure about it, type !c blacklist %s", (message.channel.id)))
  else:
    lib.db.connectAndQuery(("UPDATE chronicles_info SET is_blacklisted = TRUE; WHERE channel_id=%s", (message.channel.id)), True, False)

    #Tell the User We're Done
    await client.add_reaction(message.channel, ":thumbup:")