import commandList as cmd
import lib.message

async def showHelp(client, message):
	helpString = []
	
	helpString.append(
		'The Chronicler Help Menu:\n\n'
		'' + cmd.prefix + ' - The Command Prefix for all commands into The Chronicler\n\n'
		'' + cmd.prefix + ' ' + cmd.show_welcome + ' - Posts the Welcome Menu into this channel\n'
		'' + cmd.prefix + ' ' + cmd.show_help + ' - Posts the Help Menu into this channel\n'
		'' + cmd.prefix + ' ' + cmd.rewrite_story + ' - The Chronicler will run through all of the messages in this channel and recreate the final Chronicle\n'
		'' + cmd.prefix + ' ' + cmd.set_privacy + ' <true or false> - Sets this channel to "Private" (if true) or "Public" (if false). Private means that while you will be able to get the links to the Chronicle, it will not be publicly available for viewing online. Essentially, only those with the generated link can view the Chronicle. Public will allow anyone who visits The Chronicler Site to read the Chronicle.\n'
		'' + cmd.prefix + ' ' + cmd.add_keyword + ' <Keyword> | <Replacement String> - Adds the specified <Keyword> and its <Replacement String> to the list of Keywords. This will make it so that everytime <Keyword> is in a message, it is replaced by the <Replacement String>. "|" is how The Chronicler knows the separation between <Keyword> and <Replacement String> Example: !c add_keyword -dual strike | Baelic swings both of his blades\n'
		'' + cmd.prefix + ' ' + cmd.remove_keyword + ' <Keyword> - Removes the specified <Keyword> and its associated <Replacement String> from The Chronicler. Example: !c remove_keyword -dual strike\n'
		'' + cmd.prefix + ' ' + cmd.close_story + ' - Tells The Chronicler to "Close" this channel"s Chronicle, preventing The Chronicler from writing to it until it is reopened.\n'
		'' + cmd.prefix + ' ' + cmd.open_story + ' - Tells The Chronicler to "Open" this channel"s Chronicle, allowing The Chronicler to write to it until it is closed.\n'
	)
	
	helpString.append(
		'' + cmd.prefix + ' ' + cmd.set_warning + ' <List of Warnings> - Sets the List of Warnings for the Chronicle. These warnings will be posted at the top of this channel"s Chronicle, helping make sure readers know what may be in the Chronicle. NOTE: This will reset any warnings already set into the Chronicle! If you want to just add onto the list, then use the "add_warning" command below. Example: !c set_warnings Sexual Content, Drug and Alchohol Reference, Violence\n'
		'' + cmd.prefix + ' ' + cmd.add_warning + ' <Warning> - Adds the <Warning> to the list of Warnings. Example: !c add_warning Heavy Language\n'
		'' + cmd.prefix + ' ' + cmd.remove_warning + ' <Warning> - Removes the Warning from the list of Warnings, if it exists in the list. Example: !c remove_warning Sexual Content\n'
		'' + cmd.prefix + ' ' + cmd.ignore_message + ' - Tells The Chronicler to Ignore this message. Can be used to send a message that should not be recorded by The Chronicler.\n'
		'' + cmd.prefix + ' ' + cmd.ignore_users + ' <User Name> - Adds the specified <User Name> to the list of users The Chronicler will ignore. Any messages by the user will not be recorded by The Chronicler. This can also be used to ignore multiple users at once using the "|" seperator. Example: !c ignore_user Miggnor / !c ignore_user Miggnor | Calli | Billi_Bob\n'
		'' + cmd.prefix + ' ' + cmd.story_link + ' - This will tell The Chronicler to post a direct link to your Chronicle.\n'
	)

	helpString.append(
		'' + cmd.prefix + ' ' + cmd.stats_general + ' - This will tell The Chronicler to post your channel"s general statistics.\n'
		'' + cmd.prefix + ' ' + cmd.stats_keywords + ' - This will tell The Chronicler to post your channel"s keywords.\n'
		'' + cmd.prefix + ' ' + cmd.stats_symbols + ' - This will tell The Chronicler to post your channel"s start and end symbols.\n'
		'' + cmd.prefix + ' ' + cmd.stats_all + ' - This will tell The Chronicler to post all of your channel"s statistics.\n'
		'' + cmd.prefix + ' ' + cmd.blacklist_channel + ' - This will tell The Chronicler to completely lock this channel and its Chronicle from its database after a single warning. BE CAREFUL: The moment you Confirm it, The Chronicler will irreversably prevent you from seeing any data of the Chronicle, read any record of the Chronicle from the site and nothing else in the blacklisted channel will be recorded ever again!\n'
	)

	helpString.append(
		'' + cmd.prefix + ' ' + cmd.create_channel + ' <Options> - Creates a new channel in the server set up for The Chronicler. <Options> are optional (if not provided, it is set up with the default values). <Options> must be formatted as follows (without quotes), seperated by a semicolon (;):\n'
		'* "channel_name=<New Channel Name>" (What the new channel will be named) (Default:<Your UserName>"s Chronicle)'
		'* "is_private=true" or "is_private=false" (Is the Chronicle Private?) (Default: isPrivate=false)\n'
		'* "keyword=<Keyword> | <ReplacementString>" (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)\n'
		'* "warnings=<Warnings>" (Create List of Warnings) (Default: None)\n'
		'* "ignore_users=<User Name> | <User Name>..." (Set up List of Ignored Users) (Default: None)\n'
		'* "sole_ownership=true" or "sole_ownership=false" (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)\n'
		'* "rewrite=true" or "rewrite=false" (If true, will immediately start to rewrite the Chronicle. If False, it will not start rewriting. NOTE: Depending on how many messages are in the channel, this may take a while. Do not post any messages until it is complete.) (Default: "rewrite=false")'
		'* "show_welcome=true" or "show_welcome=false" (Shows the welcome message once the channel is created) (Default: showWelcome=true)\n'
		'* "show_help=true" or "show_help=false" (Shows the help message once the channel is created) (Default: showHelp=true)'
		'Example: ' + cmd.prefix + ' ' + cmd.create_channel + ' isPrivate=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missle; warnings=Sexual Content, Drug and Alchohol Reference, Violence; ignoreUsers=Miggnor | Calli | Billi_Bob; soleOwnership=true'
	)

	helpString.append(
		'' + cmd.prefix + ' ' + cmd.whitelist_channel + ' <Options> - Adds the channel into The Chronicler"s database. <Options> are optional (if not provided, it is set up for the default values). <Options> must be formatted as follows (without the quotes), seperated by a semicolon (;):\n'
		'* "is_private=true" or "is_private=false" (Is the Chronicle Private?) (Default: isPrivate=false)\n'
		'* "keyword=<Keyword> | <ReplacementString>" (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)\n'
		'* "warnings=<Warnings>" (Create List of Warnings) (Default: None)\n'
		'* "ignore_users=<User Name> | <User Name>..." (Set up List of Ignored Users) (Default: None)\n'
		'* "sole_ownership=true" or "soleOwnership=false" (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)\n'
		'* "rewrite=true" or "rewrite=false" (If true, will immediately start to rewrite the Chronicle. If False, it will not start rewriting. NOTE: Depending on how many messages are in the channel, this may take a while. Do not post any messages until it is complete.) (Default: "rewrite=false")'
		'* "show_welcome=true" or "show_welcome=false" (Shows the welcome message once the channel is created) (Default: showWelcome=true)\n'
		'* "show_help=true" or "show_help=false" (Shows the help message once the channel is created) (Default: showHelp=true)'
		'Example: ' + cmd.prefix + ' ' + cmd.whitelist_channel + ' isPrivate=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missle; warnings=Sexual Content, Drug and Alchohol Reference, Violence; ignoreUsers=Miggnor | Calli | Billi_Bob; soleOwnership=true'
	)
	
	for string in helpString:
		await lib.message.createMessage(message.channel, string, deleteSelf=False)