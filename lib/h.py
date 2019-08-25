#Import Statements
import commandList as cmd
import lib.message

async def showHelp(client, message):
		"""
		Function That Posts the Help Messages to the Player

		Parameters:
		-----------
				client (discord.Client)
						The Chronicler Client
				message (discord.Message)
						The Message That Had the Command
		"""

		value = message.content.replace(cmd.show_help["command"], "").strip()

		if value == "":
				helpStr = ["Welcome to The Chronicler Help!\n\nBelow is a list of the commands that The Chronicler can read and understand. If you wish to learn more about a specific command, type the help command, followed by the command name that you wish to know about (for example: " + (cmd.show_help["command"]) + " " + (cmd.create_channel["command_name"]) + ").\n\nIf you wish to learn more about how to format text such as making text bold or italicized, you can find that information here: https://support.discordapp.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-\n\n"]

				i = 0
				cNum = 0

				while cNum < len(cmd.command_list):
						if len(helpStr[i] + cmd.command_list[cNum]["command_name"]) >= 1975:
								i += 1

								#If the Last Command in List
								if cNum == len(cmd.command_list) - 1:
										helpStr.append(cmd.command_list[cNum]["command_name"])
										break
								else:
										helpStr.append(cmd.command_list[cNum]["command_name"] + ", ")
										cNum += 1
						else:
								#If the Last Command in List
								if cNum == len(cmd.command_list) - 1:
										helpStr[i] += cmd.command_list[cNum]["command_name"]
										break
								else:
										helpStr[i] += cmd.command_list[cNum]["command_name"] + ", "
										cNum += 1

				k = 0
				while k < len(helpStr):
						await lib.message.send(client, message.channel, helpStr[k], delete=False)
						k += 1


		else:
				helpStr = ""
				for command in cmd.command_list:
						if command["command_name"] == value:
								helpStr = "__**" + command["name"] + "**__\n\n"
								helpStr += "__Command:__ " + command["command"] + "\n\n"
								helpStr += "__Description:__ " + command["description"] + "\n\n"
								helpStr += "__Can Be Posted In:__ " + command["can_post_in"] + "\n\n"

								optionStr = ""

								if command["options"] != None and len(command["options"]) > 0:
										optionStr += "__Options:__\n"
										for option in command["options"]:
												optionStr += "\n\t" + "* " + option
										optionStr += "\n\n"

								exampleStr = ""

								if command["examples"] != None and len(command["examples"]) > 0:
										exampleStr += "\n\n__Examples:__\n\n"
										for example in command["examples"]:
												exampleStr += "\t" + example + "\n"

								if len(helpStr + optionStr + exampleStr) <= 2000:
										await lib.message.send(client, message.channel, helpStr + optionStr + exampleStr, ignoreStyle=True, delete=False)
								elif len(helpStr + optionStr) <= 2000:
										await lib.message.send(client, message.channel, helpStr + optionStr, ignoreStyle=True, delete=False)
										await lib.message.send(client, message.channel, exampleStr, ignoreStyle=True, delete=False)
								elif len(optionStr + exampleStr) <= 2000:
										await lib.message.send(client, message.channel, helpStr, ignoreStyle=True, delete=False)
										await lib.message.send(client, message.channel, optionStr + exampleStr, ignoreStyle=True, delete=False)
								else:
										await lib.message.send(client, message.channel, helpStr, ignoreStyle=True, delete=False)
										await lib.message.send(client, message.channel, optionStr, ignoreStyle=True, delete=False)
										await lib.message.send(client, message.channel, exampleStr, ignoreStyle=True, delete=False)

								return

				await lib.reaction.reactThumbsDown(client, message)
				await lib.message.send(client, message.channel, "We could not find the command that you provided. Type '!c help' for a full list of available commands that The Chronicler can read.", feedback=True)