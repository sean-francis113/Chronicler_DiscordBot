import discord

async def showHelp(message, client):
  helpString = []

  helpString.append('The Chronicler Help Menu:\n\n'
                '!c - The Command Prefix for all commands into The Chronicler\n\n')
  helpString.append('!c welcome - Posts the Welcome Menu into this channel\n'
                '!c help - Posts the Help Menu into this channel\n'
                '!c rewrite - The Chronicler will run through all of the messages in this channel and recreate the final Chronicle\n'
                '!c set_private <true or false> - Sets this channel to \'Private\' (if true) or \'Public\' (if false). Private means that while you will be able to get the links to the Chronicle, it will not be publicly available for viewing online. Essentially, only those with the generated link can view the Chronicle. Public will allow anyone who visits The Chronicler Site to read the Chronicle.\n'
                '!c add_keyword <Keyword> | <Replacement String> - Adds the specified <Keyword> and its <Replacement String> to the list of Keywords. This will make it so that everytime <Keyword> is in a message, it is replaced by the <Replacement String>. \'|\' is how The Chronicler knows the separation between <Keyword> and <Replacement String> Example: !c add_keyword -dual strike | Baelic swings both of his blades\n'
                '!c remove_keyword <Keyword> - Removes the specified <Keyword> and its associated <Replacement String> from The Chronicler. Example: !c remove_keyword -dual strike\n')
  helpString.append('!c close_story - Tells The Chronicler to \'Close\' this channel\'s Chronicle, preventing The Chronicler from EVER writing to it until it is reopened.\n'
                '!c open_story - Tells The Chronicler to \'Open\' this channel\'s Chronicle, allowing The Chronicler to write to it until it is closed.\n'
                '!c set_warnings <List of Warnings> - Sets the List of Warnings for the Chronicle. These warnings will be posted at the top of this channel\'s Chronicle, helping make sure readers know what may be in the Chronicle. Example: !c set_warnings Sexual Content, Drug and Alchohol Reference, Violence\n'
                '!c add_warning <Warning> - Adds the <Warning> to the list of Warnings. Example: !c add_warning Heavy Language\n'
                '!c remove_warning <Warning> - Removes the Warning from the list of Warnings, if it exists in the list. Example: !c remove_warning Sexual Content\n')
  helpString.append('!c ignore - Tells The Chronicler to Ignore this message. Can be used to send a message that should not be recorded by The Chronicler.\n'
                '!c ignore_user <User Name> - Adds the specified <User Name> to the list of users The Chronicler will ignore. Any messages by the user will not be recorded by The Chronicler. This can also be used to ignore multiple users at once using the \'|\' seperator. Example: !c ignore_user Miggnor / !c ignore_user Miggnor | Calli | Billi_Bob\n'
                '!c get_link - This will tell The Chronicler to post a direct link to your Chronicle.\n'
                '!c stats = This will tell The Chronicler to post your channel\'s settings.\n'
                '!c blacklist - This will tell The Chronicler to completely remove this channel and its Chronicle from its database. BE CAREFUL: The moment you hit Enter and confirm it, The Chronicler will irreversably delete all record of the Chronicle from the site and nothing else in the blacklisted channel will be recorded ever again!\n'
                '!c create_channel <Options> - Creates a new channel in the server set up for The Chronicler. <Options> are optional (if not provided, it is set up for the default values). <Options> must be formatted as follows (without the quotes), seperated by a semicolon (;):\n'
                '* \'channelName=<New Channel Name>\' (What the new channel will be named) (Default:<Your UserName>\'s Chronicle)'
                '* \'isPrivate=true\' or \'isPrivate=false\' (Is the Chronicle Private?) (Default: isPrivate=false)\n'
                '* \'keyword=<Keyword> | <ReplacementString>\' (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)\n'
                '* \'warnings=<Warnings>\' (Create List of Warnings) (Default: None)\n'
                '* \'ignoreUsers=<User Name> | <User Name>...\' (Set up List of Ignored Users) (Default: None)\n'
                '* \'soleOwnership=true\' or \'soleOwnership=false\' (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)\n'
                )
  helpString.append('!c add_to_database <Options> - Adds the channel into The Chronicler\'s database. <Options> are optional (if not provided, it is set up for the default values). <Options> must be formatted as follows (without the quotes), seperated by a semicolon (;):\n'
                '* \'channelName=<New Channel Name>\' (What the new channel will be named) (Default:<Your UserName>\'s Chronicle)'
                '* \'isPrivate=true\' or \'isPrivate=false\' (Is the Chronicle Private?) (Default: isPrivate=false)\n'
                '* \'keyword=<Keyword> | <ReplacementString>\' (Set up Keywords and Replacement Strings) (Can Be Used Multiple Times) (Default: None)\n'
                '* \'warnings=<Warnings>\' (Create List of Warnings) (Default: None)\n'
                '* \'ignoreUsers=<User Name> | <User Name>...\' (Set up List of Ignored Users) (Default: None)\n'
                '* \'soleOwnership=true\' or \'soleOwnership=false\' (If true, the user who entered the command will be the only one to have permissions for the new channel) (Default: soleOwnership=true)\n')
  helpString.append('* \'showWelcome=true\' or \'showWelcome=false\' (Shows the welcome message once the channel is created) (Default: showWelcome=true)\n'
                '* \'showHelp=true\' or \'showHelp=false\' (Shows the help message once the channel is created) (Default: showHelp=true)'
    'Example: !c create_channel isPrivate=false; keyword=-dual strike | Baelic swings both of his blades; keyword=-magic_missle | Gilla casts magic missle; warnings=Sexual Content, Drug and Alchohol Reference, Violence; ignoreUsers=Miggnor | Calli | Billi_Bob; soleOwnership=true')
  
  for string in helpString:
    await client.send_message(message.channel, string)