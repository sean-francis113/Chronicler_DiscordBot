#Command Prefix
prefix = "!c"

#General Commands

show_welcome = {
    "name" : "Show Welcome Message",
    
		"command" : prefix + " " + "welcome",

		"command_name" : "welcome",
    
		"summary" : "Posts the Welcome Menu into this channel.",
    
		"description" : "Posts the Welcome Menu into this channel. Introduces The Chronicler and gives a quick start for users to immediately start recording.",
    
		"options" : [],
    
		"can_post_in" : "Any Channel that is Not Ignored (see ignore_channel Command).",
		
		"examples": []
}

show_help = {
    "name" : "Show Help Message",
    
		"command" : prefix + " " + "help",

		"command_name" : "help",
    
		"summary" : "Posts the Help Menu into this channel.",
    
		"description" : "Posts the Help Menu into this channel. Shows all of the commands for The Chronicler and a can show the full description of each by specifying which one to look at.", 
		
		"options" : ["Add a different command's name from the list above onto this to get the full description of the specified command."],
    
		"can_post_in" : "Any Channel that is Not Ignored (see ignore_channel Command).",
    
		"examples" : [prefix + " " + "help", prefix + " " + "help" + " " + "create_channel"]
}

#----------------------------------------

#Change Visible Feedback Commands

change_feedback = {
    "name" : "Change Bot Feedback",
		
    "command" : prefix + " " + "change_feedback",
    
		"command_name" : "change_feedback",
		
		"summary" : "Changes how/if The Chronicler reports what it is doing within the channel.",
    
		"description" : "Changes how/if The Chronicler reports what it is doing within the channel. Can be set to show both reactions and messages, just reactions, just messages, or nothing.",
    
		"options" : ["all - Show all feedback", "messages - Show only messages", "reactions - Show only reactions", "none - Show no feedback"],
    
		"can_post_in" : "Any Channel that is Not Ignored (see ignore_channel Command).",
    
		"examples" : [prefix + " " + "change_feedback" + " " + "reactions"]
}

#----------------------------------------

#Channel Commands

create_channel = {
    "name" : "Create Channel",
    
		"command" : prefix + " " + "create_channel",

		"command_name" : "create_channel",
    
		"summary" : "Creates a new channel in the server set up for The Chronicler.",
    
		"description" : "Creates a new channel in the server set up for The Chronicler. <Options> are optional by adding the desired options (if not provided, it is set up with the default values) after the command. Options must be formatted with the following options (without quotes), separated by a semicolon (;).",
    
		"options" : ['"channel_name=<New Channel Name>" (What the new channel will be named) (Default:<Your UserName>\'s Chronicle)', '"is_private=true" or "is_private=false" (Is the Chronicle Private?) (Default: isPrivate=false)', '"keyword=<Keyword> | <ReplacementString>" (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)', '"warnings=<Warnings>" (Create List of Warnings) (Default: None)', '"ignore_users=<User Name> | <User Name>..." (Set up List of Ignored Users) (Default: None)', '"sole_ownership=true" or "sole_ownership=false" (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)', '"rewrite=true" or "rewrite=false" (If true, will immediately start to rewrite the Chronicle. If False, it will not start rewriting. NOTE: Depending on how many messages are in the channel, this may take a while. Do not post any messages until it is complete.) (Default: "rewrite=false")', '"show_welcome=true" or "show_welcome=false" (Shows the welcome message once the channel is created) (Default: showWelcome=true)', '"show_help=true" or "show_help=false" (Shows the help message once the channel is created) (Default: showHelp=true)', '"is_nsfw=true" or "is_nsfw=false" (Is the Channel Not Safe For Work) (Default: is_nsfw=false)'],
    
		"can_post_in" : "Any Channel that is Not Ignored (see ignore_channel Command).",
    
		"examples" : [prefix + " " + "create_channel" + ' is_private=false; keyword=dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missle; warnings=Sexual Content, Drug and Alchohol Reference, Violence; ignore_users=Miggnor | Calli | Billi_Bob; sole_ownership=true']
}

whitelist_channel = {
    "name" : "Whitelist Channel",
    
		"command" : prefix + " " + "whitelist",

		"command_name" : "whitelist",
    
		"summary" : "Adds the already created channel into The Chronicler\'s database.",
    
		"description" : "Adds the channel into The Chroniclers database. <Options> are optional by replacing <Options> with the specified options (if not provided, it is set up for the default values). Any <Options> must be formatted as follows (without the quotes), separated by a semicolon (;).",
    
		"options" : ['"is_private=true" or "is_private=false" (Is the Chronicle Private?) (Default: isPrivate=false)', '"keyword=<Keyword> | <ReplacementString>" (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)', '"warnings=<Warnings>" (Create List of Warnings) (Default: None)', '"ignore_users=<User Name> | <User Name>..." (Set up List of Ignored Users) (Default: None)', '"sole_ownership=true" or "soleOwnership=false" (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)', '"rewrite=true" or "rewrite=false" (If true, will immediately start to rewrite the Chronicle. If False, it will not start rewriting. NOTE: Depending on how many messages are in the channel, this may take a while. Do not post any messages until it is complete.) (Default: "rewrite=false")', '"show_welcome=true" or "show_welcome=false" (Shows the welcome message once the channel is created) (Default: showWelcome=true)', '"show_help=true" or "show_help=false" (Shows the help message once the channel is created) (Default: showHelp=true)', '"is_nsfw=true" or "is_nsfw=false" (Is the Channel Not Safe For Work) (Default: is_nsfw=false)'],
    
		"can_post_in" : "Any Channel that is Not Ignored (see ignore_channel Command).",
    
		"examples" : [prefix + " " + "whitelist" + " is_private=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missile; warnings=Sexual Content, Drug and Alcohol Reference, Violence; ignore_users=Miggnor | Calli | Billi_Bob; sole_ownership=true"]
}

blacklist_channel = {
    "name": "Blacklist Channel",
    
		"command": prefix + " " + "blacklist",
    
		"command_name" : "blacklist", 
		
		"summary": "IRREVERSIBLY delete channel from The Chronicler.",
    
		"description": "This will tell The Chronicler to completely lock this channel and its Chronicle from its database after a single warning. BE CAREFUL: The moment you Confirm it, The Chronicler will irreversibly prevent you from seeing any data of the Chronicle, read any record of the Chronicle from the site and nothing else in the blacklisted channel will be recorded ever again!",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

rename_channel = {
    "name": "Rename Channel",
    
		"command": prefix + " " + "rename_channel",
    
		"command_name" : "rename_channel", 
		
		"summary": "Renames the channel in the database to a new name supplied after the command.",
    
		"description": "Renames the channel in the database to the <New Name>. NOTE: This will only rename the channel in The Chronicler Database. You will need to manually change the name in Discord if you wish to have the names consistent.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Story Commands

rewrite_story = {
    "name": "Rewrite Story",
    
		"command": prefix + " " + "rewrite",
    
		"command_name" : "rewrite", 
		
		"summary": "Recreate the story with all of the messages in the channel.",
    
		"description": "The Chronicler will run through all of the messages in this channel and recreate the final Chronicle. It will take each message, edit it as normal (remove markdown, symbols, keywords, etc.) and prepare for all of the messages to be posted back into the database.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

open_story = {
    "name": "Open Story",
    
		"command": prefix + " " + "open_story",
    
		"command_name" : "open_story", 
		
		"summary": "Open up the story, allowing The Chronicler to write to its database.",
    
		"description": "Tells The Chronicler to Open this channels Chronicle, allowing The Chronicler to write to it until it is closed. If you wish, you can always reclose the Chronicle.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

close_story = {
    "name": "Close Story",
    
		"command": prefix + " " + "close_story",
    
		"command_name" : "close_story", 
		
		"summary": "Close the story, preventing The Chronicler from writing to its database.",
    
		"description": "Tells The Chronicler to Close this channels Chronicle, preventing The Chronicler from writing to it until it is reopened. This is not a permanent closure, as you can always open the story back up.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Privacy Commands

set_privacy = {
    "name": "Set Privacy",
    
		"command": prefix + " " + "set_privacy",
    
		"command_name" : "set_privacy", 
		
		"summary": "Changes the public visibility of the story.",
    
		"description": "Sets this channel to Private (if true) or Public (if false). Private means that only those with the generated link can view the Chronicle. Public will allow anyone who visits The Chronicler Site to read the Chronicle.",
    
		"options": ["true - Privitizes the story", "false - Publicizes the story"],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "set_privacy" + " true"]
}

#----------------------------------------

#Ignore Commands

ignore_message = {
    "name": "Ignore Message",
    
		"command": prefix + " " + "ignore",
    
		"command_name" : "ignore", 
		
		"summary": "Tells The Chronicler to Ignore this message.",
    
		"description": "Tells The Chronicler to Ignore this message. Can be used to send a message that should not be recorded by The Chronicler.",
    
		"options": [],
    
		"can_post_in": "Any channel that is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

ignore_users = {
    "name": "Ignore Users",
    
		"command": prefix + " " + "ignore_user",
    
		"command_name" : "ignore_user", 
		
		"summary": "Adds the specified user name to the list of users The Chronicler will ignore.",
    
		"description": "Adds the specified user name to the list of users The Chronicler will ignore. Any messages by the user will not be recorded by The Chronicler. This can also be used to ignore multiple users at once using the ‘|’ separator.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "ignore_user" + " Miggnor", prefix + " " + "ignore_user" + " Miggnor | Calli | Billi_Bob"]
}

remove_ignored_users = {
    "name": "Remove Ignored Users",
    
		"command": prefix + " " + "pull_ignored_user",
    
		"command_name" : "pull_ignored_user", 
		
		"summary": "Removes the specified user name from the list of ignored users.",
    
		"description": "Removes the specified <User Name> from the list of ignored users. This can also be used to remove multiple ignored users at once using the ‘|’ separator.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "pull_ignored_user" + " Miggnor", prefix + " " + "pull_ignored_user" + " Miggnor | Calli | Billi_Bob"]
}

clear_ignored_users = {
    "name": "Clear Ignored Users",
    
		"command": prefix + " " + "clear_ignored_users",
    
		"command_name" : "clear_ignored_users", 
		
		"summary": "Completely clear the list of ignored users from the database.",
    
		"description": "Completely clear the list of ignored users from the database.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

ignore_channel = {
    "name": "Ignore Channel",
    
		"command": prefix + " " + "ignore_channel",
    
		"command_name" : "ignore_channel", 
		
		"summary": "Tells The Chronicler to ignore anything in the channel.",
    
		"description": "Tells The Chronicler to ignore anything in the channel. The only command that The Chronicler will look for and act on is the restore_channel command. This can be used on any channel, even those not in the database.",
    
		"options": [],
    
		"can_post_in": "Any channel that is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

restore_channel = {
		"name": "Restore Channel",
    
		"command": prefix + " " + "restore_channel",
    
		"command_name" : "restore_channel", 
		
		"summary": "Tells The Chronicler to stop ignoring a channel.",
    
		"description": "Tells The Chronicler to stop ignoring a channel.",
    
		"options": [],
    
		"can_post_in": "Any channel",
    
		"examples": []

}

#----------------------------------------

#Warning Commands

add_warning = {
    "name": "Add New Warning",
    
		"command": prefix + " " + "add_warning",
    
		"command_name" : "add_warning", 
		
		"summary": "Adds a new warning to the list of Warnings.",
    
		"description": "Adds the warning to the list of Warnings. The Warning(s) that you wish to add should be put in the command after 'add_warning.'",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "add_warning" + " Heavy Language"]
}

remove_warning = {
    "name": "Remove Warning",
    
		"command": prefix + " " + "pull_warning",
    
		"command_name" : "pull_warning", 
		
		"summary": "Removes a warning from the list of Warnings, if it exists in the list.",
    
		"description": "Removes a warning from the list of Warnings, if it exists in the list.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "pull_warning" + " Sexual Content"]
}

set_warning = {
    "name": "Set Warnings",
    
		"command": prefix + " " + "set_warning",
    
		"command_name" : "set_warning", 
		
		"summary": "Sets the List of Warnings for the Chronicle.",
    
		"description": "Sets the List of Warnings for the Chronicle. These warnings will be posted at the top of this channel’s Chronicle, helping make sure readers know what may be in the Chronicle. NOTE: This will reset any warnings already set into the Chronicle! If you want to just add onto the list, then use the add_warning command.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "set_warning" + " Sexual Content, Drug and Alcohol Reference, Violence"]
}

clear_warning = {
    "name": "Clear Warnings",
    
		"command": prefix + " " + "clear_warning",
    
		"command_name" : "clear_warning", 
		
		"summary": "Clears all warnings from the channel in the database, if any.",
    
		"description": "Clears all warnings from the channel in the database, if any.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Keyword Commands

add_keyword = {
    "name": "Add New Keyword",
    
		"command": prefix + " " + "add_keyword",
    
		"command_name" : "add_keyword", 
		
		"summary": "Adds the specified keyword and its replacement string to the list of Keywords.",
    "description": "Adds the specified keyword and its replacement string to the list of Keywords. This will make it so that everytime the keyword is in a message, it is replaced by the replacement string. The pipe character ( | ) is how The Chronicler knows the separation between keyword and replacement string",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "add_keyword" + " dual strike | Baelic swings both of his blades"]
}

remove_keyword = {
    "name": "Remove Keyword",
    
		"command": prefix + " " + "pull_keyword",
    
		"command_name" : "pull_keyword",
		
		"summary": "Removes the specified keyword and its associated replacement string from The Chronicler.",
    
		"description": "Removes the specified keyword and its associated replacement string from The Chronicler. The replacement string does not need to be included.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "pull_keyword" + " dual strike"]
}

clear_keywords = {
    "name": "Clear Keywords",
    
		"command": prefix + " " + "clear_keywords",
    
		"command_name" : "clear_keywords", 
		
		"summary": "Clears all keywords and associated replacement strings from the channel in the database, if any.",
    
		"description": "Clears all keywords and associated replacement strings from the channel in the database, if any.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Symbol Commands

add_symbol = {
    "name": "Add New Symbol",
    
		"command": prefix + " " + "add_symbol",
    
		"command_name" : "add_symbol", 
		
		"summary": "Adds the specified symbol's start and endings to the list of symbols.",

    "description": "Adds the specified keyword and its replacement string to the list of Keywords. This will make it so that everything between the symbols (and including the symbols) are completely removed from the message. The pipe character ( | ) is how The Chronicler knows the separation between the start and ending symbols.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "add_symbol" + " (( | ]]"]
}

remove_symbol = {
    "name": "Remove Symbol",
    
		"command": prefix + " " + "pull_symbol",
    
		"command_name" : "pull_symbol",
		
		"summary": "Removes the specified start symbol and its respective ending symbol from The Chronicler.",
    
		"description": "Removes the specified start symbol and its respective ending symbol from The Chronicler. The end symbol does not need to be included.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": [prefix + " " + "pull_symbol" + "(("]
}

clear_symbols = {
    "name": "Clear Symbols",
    
		"command": prefix + " " + "clear_symbols",
    
		"command_name" : "clear_symbols", 
		
		"summary": "Clears all start and end symbols from the channel in the database, if any.",
    
		"description": "Clears all start and end symbols from the channel in the database, if any.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Display Link Commands

story_link = {
    "name": "Get Story Link",
    
		"command": prefix + " " + "get_link",
    
		"command_name" : "get_link", 
		
		"summary": "This will tell The Chronicler to post a direct link to your Chronicle.",
    
		"description": "This will tell The Chronicler to post a direct link to your Chronicle.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Display Stats Commands

stats_general = {
    "name": "Get General Stats",
    
		"command": prefix + " " + "get_general_stats",
    
		"command_name" : "get_general_stats", 
		
		"summary": "This will tell The Chronicler to post your channel's general statistics.",
    
		"description": "This will tell The Chronicler to post your channel's general statistics.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

stats_keywords = {
    "name": "Get Keyword Stats",
    
		"command": prefix + " " + "get_keywords",
    
		"command_name" : "get_keywords", 
		
		"summary": "This will tell The Chronicler to post your channel's keywords.",
    
		"description": "This will tell The Chronicler to post your channel's keywords.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

stats_symbols = {
    "name": "Get Symbol Stats",
    
		"command": prefix + " " + "get_symbols",
    
		"command_name" : "get_symbols", 
		
		"summary": "This will tell The Chronicler to post your channel's start and end symbols.",
    
		"description": "This will tell The Chronicler to post your channel's start and end symbols.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

stats_all = {
    "name": "Get All Stats",
    
		"command": prefix + " " + "get_all_stats",
    
		"command_name" : "get_all_stats", 
		
		"summary": "This will tell The Chronicler to post all of your channel's statistics.",
    
		"description": "This will tell The Chronicler to post all of your channel's statistics.",
    
		"options": [],
    
		"can_post_in": "A channel that has been added to The Chronicler's Database and is not being ignored (see ignore_channel Command).",
    
		"examples": []
}

#----------------------------------------

#Complete List of Commands

command_list = [
    show_welcome, show_help, create_channel, whitelist_channel, blacklist_channel, rename_channel, rewrite_story, open_story, close_story, set_privacy, ignore_message, ignore_users, remove_ignored_users, clear_ignored_users, add_warning, remove_warning, set_warning, clear_warning, add_keyword, remove_keyword, add_symbol, remove_symbol, story_link, stats_general, stats_keywords,
    stats_symbols, stats_all]