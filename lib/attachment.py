#Import Statements
import lib.db
import lib.reaction

def postAttachments(client, message):
		if(message.attachments == None and len(message.attachments) == 0):
				return

		for attach in message.attachments:
				lib.db.queryDatabase(
        "INSERT INTO {id}_contents (message_id, is_pinned, entry_type, char_count, word_count, entry_owner, entry_editted, entry_original) VALUES (\'{message_id}\', {pinned}, \'{type}\', {char_count}, {word_count}, \'{entry_owner}\', \'{entry_editted}\', \'{entry_original}\')"
        .format(
            id=str(message.channel.id),
            message_id=str(message.id),
            pinned=str(message.pinned).upper(),
            type="Image",
            char_count=0,
            word_count=0,
            entry_owner=message.author.name,
            entry_editted="<span class=\"discord_img\"><img src=\"" + attach.url + "\" alt=\"" + attach.filename + "\"></span>",
            entry_original="<span class=\"discord_img\"><img src=\"" + attach.url + "\" alt=\"" + attach.filename + "\"></span>"),
        client,
        message.channel,
        tablename="{id}_contents".format(id=str(message.channel.id)),
        commit=True,
        closeConn=True)