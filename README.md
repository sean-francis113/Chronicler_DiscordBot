# Chronicler_DiscordBot

The Chronicler is a Discord Server Bot made for Pen and Paper Role Playing Game (PnPRPG) Servers that records all of the messages it sees into an online database. That database is available to view online at chronicler.seanmfrancis.net where the messages are arranged as a novel. From there, you can download not only your own 'Chronicle', but also any others on the database to read offline and/or later.

To get started, we suggest use the 'Create Channel' command to create a Chronicler channel with pre-set settings. This will add the channel to The Chronicler's database and allow it to start recording the channel. The Chronicler will not record any channel that is not in its database. If you have a channel you wish to add to the database, used the 'Whitelist' command to add the channel into the database.

Note, though, that The Chronicler can only record messages as they are sent, or edit messages that are already in the database. In order to catch special cases, such as recording previous messages or editing messages not in the database, use the 'Rewrite' command to have The Chronicler rewrite the Chronicle as it is when the command is sent.

Happy Chronicling!

**List of Commands**


__Command Prefix__

Command

  !c

Description

  The Command Prefix for all commands into The Chronicler. This is how The Chronicler reads a command. If it is not provided, it will determine the message sent as being something to record.


__Show Welcome__

Command

	!c show_welcome


Description

  	Posts the Welcome Menu into this channel. Introduces The Chronicler and gives a quick start for users to immediately start recording.


__Show Help____

Command

	!c show_help

Description

	Posts the Help Menu into this channel. Shows all of the commands for The Chronicler and a summary of what each command does.


__Rewrite Chronicler__

Command

  	!c rewrite

Description

  	The Chronicler will run through all of the messages in this channel and recreate the final Chronicle. It will take each message, edit it as normal (remove markdown, symbols, keywords, etc.) and prepare for all of the messages to be posted back into the database.


__Set Privacy__

Command

  	!c set_privacy <true or false>

Description

  	Sets this channel to Private (if true) or Public (if false). Private means that only those with the generated link can view the Chronicle. Public will allow anyone who visits The Chronicler Site to read the Chronicle.


__Add Keyword__

Command

  	!c add_keyword <Keyword> | <Replacement String>

Description

	Adds the specified <Keyword> and its <Replacement String> to the list of Keywords. This will make it so that everytime <Keyword> is in a message, it is replaced by the <Replacement String>. ‘|’ is how The Chronicler knows the separation between <Keyword> and <Replacement String> 

Example

	!c add_keyword dual strike | Baelic swings both of his blades


__Remove Keyword__

Command

	!c pull_keyword <Keyword>

Description

	Removes the specified <Keyword> and its associated <Replacement String> from The Chronicler. The <Replacement String> does not need to be included.

Example

	!c remove_keyword dual strike


__Close Story__

Command

	!c close_story

Description

	Tells The Chronicler to Close this channels Chronicle, preventing The Chronicler from writing to it until it is reopened. This is not a permanent closure, as you can always open the story back up.


__Open Story__

Command

	!c open_story

Description

	Tells The Chronicler to Open this channels Chronicle, allowing The Chronicler to write to it until it is closed. If you wish, you can always reclose the Chronicle.


__Set Warnings__

Command

	!c set_warning <List of Warnings>

Description

	Sets the List of Warnings for the Chronicle. These warnings will be posted at the top of this channel’s Chronicle, helping make sure readers know what may be in the Chronicle. NOTE: This will reset any warnings already set into the Chronicle! If you want to just add onto the list, then use the add_warning command below. 

Example

	!c set_warnings Sexual Content, Drug and Alcohol Reference, Violence


__Add Warning__

Command

	!c add_warning <Warning>

Description

	Adds the <Warning> to the list of Warnings.

Example
 
	!c add_warning Heavy Language


__Remove Warning__

Command

	!c pull_warning <Warning>

Description

	Removes <Warning> from the list of Warnings, if it exists in the list. 

Example

	!c pull_warning Sexual Content


__Clear Warning__

Command

	!c clear_warning

Description

	Clears all warnings from the channel in the database, if any.


__Ignore Message__

Command

	!c ignore

Description

	Tells The Chronicler to Ignore this message. Can be used to send a message that should not be recorded by The Chronicler.


__Ignore Users__

Command

	!c ignore_user <User Name>

Description

	Adds the specified <User Name> to the list of users The Chronicler will ignore. Any messages by the user will not be recorded by The Chronicler. This can also be used to ignore multiple users at once using the ‘|’ separator.

Examples

	!c ignore_user Miggnor
	!c ignore_user Miggnor | Calli | Billi_Bob


__Remove Ignored Users__

Command

	!c pull_ignored_user <User Name>

Description

	Removes the specified <User Name> from the list of ignored users. This can also be used to remove multiple ignored users at once using the ‘|’ separator.

Examples

	!c pull_ignored_user Miggnor
	!c pull_ignored_user Miggnor | Calli | Billi_Bob


__Get Story Link__

Command

	!c get_link

Description

	This will tell The Chronicler to post a direct link to your Chronicle.


__Get General Stats__

Command

	!c stats_general

Description

	This will tell The Chronicler to post your channel's general statistics.


__Get Keyword Stats__

Command

	!c stats_keywords

Description

	This will tell The Chronicler to post your channel's keywords.


__Get Symbol Stats__

Command

	!c stats_symbols

Description

	This will tell The Chronicler to post your channel's start and end symbols.

__Get All Stats__

Command

	!c stats_all

Description

	This will tell The Chronicler to post all of your channel's statistics.


__Blacklist Channel__

Command

	!c blacklist_channel

Description

	This will tell The Chronicler to completely lock this channel and its Chronicle from its database after a single warning. BE CAREFUL: The moment you Confirm it, The Chronicler will irreversibly prevent you from seeing any data of the Chronicle, read any record of the Chronicle from the site and nothing else in the blacklisted channel will be recorded ever again!

__Create Channel__
	
Command

	!c create_channel <Options>

Description

	Creates a new channel in the server set up for The Chronicler. <Options> are optional (if not provided, it is set up with the default values). <Options> must be formatted as follows (without quotes), separated by a semicolon (;):
		channel_name=<New Channel Name> (What the new channel will be named) (Default:<Your UserName>s Chronicle)
		is_private=true or is_private=false (Is the Chronicle Private?) (Default: is_private=false)
		keyword=<Keyword> | <ReplacementString> (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)
		warnings=<Warnings> (Create List of Warnings) (Default: None)
		ignore_users=<User Name> | <User Name>... (Set up List of Ignored Users) (Default: None)
		sole_ownership=true or sole_ownership=false (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: sole_ownership=true)
		rewrite=true or rewrite=false (If true, will immediately start to rewrite the Chronicle. If False, it will not start rewriting. NOTE: Depending on how many messages are in the channel, this may take a while. Do not post any messages until it is complete.) (Default: rewrite=false)
		show_welcome=true or show_welcome=false (Shows the welcome message once the channel is created) (Default: show_welcome=true)
		show_help=true or show_help=false (Shows the help message once the channel is created) (Default: show_help=true)
		is_nsfw=true or is_nsfw=false (Is the Channel Not Safe For Work) (Default: is_nsfw=false)

Example

	!c create_channel is_private=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missile; warnings=Sexual Content, Drug and Alcohol Reference, Violence; ignore_users=Miggnor | Calli | Billi_Bob; sole_ownership=true


__Whitelist Channel__

Command

	!c whitelist <Options>

Description

	Adds the channel into The Chroniclers database. <Options> are optional (if not provided, it is set up for the default values). <Options> must be formatted as follows (without the quotes), separated by a semicolon (;):
				is_private=true or is_private=false (Is the Chronicle Private?) (Default: is_private=false)
				keyword=<Keyword> | <ReplacementString> (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)
				warnings=<Warnings> (Create List of Warnings) (Default: None)
				ignore_users=<User Name> | <User Name>... (Set up List of Ignored Users) (Default: None)
				sole_ownership=true or sole_ownership=false (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: sole_ownership=true)
				rewrite=true or rewrite=false (If true, will immediately start to rewrite the Chronicle. If False, it will not start rewriting. NOTE: Depending on how many messages are in the channel, this may take a while. Do not post any messages until it is complete.) (Default: rewrite=false)
				show_welcome=true or show_welcome=false (Shows the welcome message once the channel is created) (Default: show_welcome=true)
				show_help=true or show_help=false (Shows the help message once the channel is created) (Default: show_help=true)
				is_nsfw=true or is_nsfw=false (Is the Channel Not Safe For Work) (Default: is_nsfw=false)

Example

	!c whitelist is_private=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missile; warnings=Sexual Content, Drug and Alcohol Reference, Violence; ignore_users=Miggnor | Calli | Billi_Bob; sole_ownership=true


__Rename Channel__

Command

	!c rename_channel <New Name>

Description

	Renames the channel in the database to the <New Name>. NOTE: This will only rename the channel in The Chronicler Database. You will need to manually change the name in Discord if you wish to have the names consistent.

Example

	!c rename_channel Let’s Do This


Copyright: Sean Francis 2019
