# Utility functions

class colours:
	BLUE = "\u001b[38;5;87m"
	DRIVES = "\u001b[1;38;5;202m"
	SPECIALDRIVE = "\u001b[1;38;5;120m"
	SEAFOAM = "\u001b[1;38;5;85m"
	RED = "\u001b[1;31m"
	MAGENTA = "\u001b[1;35m"
	YELLOW = "\u001b[33;1m"
	RESET = "\u001b[0m"
	DISABLED = "\u001b[38;5;237m"

def _log(text:str): _log_info(text)

def _log_info(text:str):
	print(colours.MAGENTA + "[Parasitic] " + colours.YELLOW + "INFO: " + str(text) + colours.RESET)

def _log_warn(text:str):
	print(colours.MAGENTA + "[Parasitic] " + colours.DRIVES + "WARN: " + str(text) + colours.RESET)

def _log_err(text:str):
	print(colours.MAGENTA + "[Parasitic] " + colours.RED + "ERR: " + str(text) + colours.RESET)

if __name__ == "__main__":
	print(colours.RED + "Do not directly run this module" + colours.RESET)