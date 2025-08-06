import shutil
import os
import sys
import questionary
import json
import time
import json_patches
import argparse

from rich.console import Console
from questionary import Style

PATH = sys.path[0]
AJVX = "13"

FLAG_DEV = True if os.getenv("_parasitic_dev") == "1" else False

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--game")
parser.add_argument("-i", "--ignore_checks", action="store_true", default=False)
parser.add_argument("-b", "--backup", action="store_true", default=False)
parser.add_argument("-n", "--no_backup", action="store_true", default=False)

args = parser.parse_args()

GAME_OVERRIDE = args.game
IGNORE_CHECKS = args.ignore_checks
FORCE_BACKUP  = args.backup
NO_BACKUP     = args.no_backup

# COLOURS #
BLUE = "\u001b[38;5;87m"
DRIVES = "\u001b[1;38;5;202m"
SPECIALDRIVE = "\u001b[1;38;5;120m"
SEAFOAM = "\u001b[1;38;5;85m"
RED = "\u001b[1;31m"
MAGENTA = "\u001b[1;35m"
YELLOW = "\u001b[33;1m"
RESET = "\u001b[0m"
DISABLED = "\u001b[38;5;237m"

# COLOURS FOR RICH #
RRED  = "[bold red]"
RBLUE = "[bold blue]"
RGREEN = "[bold green]"
RYELLOW = "[yellow]"
RPURPLE = "[bold magenta]"
RRESET = "[/]"

KNOWN_BORKED_WITH_GLOBALS = ["raincheck"]

console = Console(log_time=False)

if IGNORE_CHECKS:
	print(RED + "Safety and sanity checks have been disabled!")
	print(RED + "These are in place for good reason!")
	print(RED + "Disabling them might break things!\n" + RESET)

	CheckboxStyle = Style([
    ('selected', 'fg:#ff6a00 noreverse'),         # style for a selected item of a checkbox
    ('text', 'fg:#ff0000'),             # plain text
    ('highlighted', 'fg:#ffe600'),
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])

else:
	CheckboxStyle = Style([
    ('selected', 'fg:#00ff1a noreverse'),      # style for a selected item of a checkbox
    ('text', 'fg:#ffcfcf'),             # plain text
    ('highlighted', 'fg:#ffe600'),
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])

def _inject(root:str):
	""" Basic injection. No trailing slash """

	if os.path.exists(f"{root}/.jxGlobals") and not IGNORE_CHECKS:
		print(RED + "Global patches have already been applied. Stop." + RESET)
		return

	with console.status(f"{RYELLOW}Applying global patches{RRESET}") as global_status:
		console.log(RYELLOW + "Target path: " + RPURPLE + root)

		# Basic injection does the following things:
		# - Ensures that all archives are unpacked before the main script is run
		# - Changes the version information
		# - Overwrites the license text
		# - Enables the developer console
		# - Disables config locking

		# Load developer mode replacement information

		console_definitions = json.load(open(f"{PATH}/payloads/global/match/console.json", "r"))
		option_definitions  = json.load(open(f"{PATH}/payloads/global/match/options.json", "r"))

		console_file = console_definitions["file"]

		dm_check = console_definitions["searches"][0]
		dmc_over = console_definitions["replacements"][0]
		cl_check = console_definitions["searches"][1]
		clc_over = console_definitions["replacements"][1]
		license  = console_definitions["searches"][2]
		nlicense = console_definitions["replacements"][2] % AJVX

		options_file = option_definitions["file"]
		config_versi = option_definitions["searches"][0]
		cfg_v_overwr = option_definitions["replacements"][0]

		# Check for RenPy archives first. If they exist,
		# we can install the mods as an overlay

		if os.path.exists(f"{root}/game/archive.rpa"):
			USE_OVERLAY = True
			RPA_NAME    = "archive.rpa"

		elif os.path.exists(f"{root}/game/scripts.rpa"):
			USE_OVERLAY = True
			RPA_NAME    = "scripts.rpa"

		else:
			USE_OVERLAY = False
			RPA_NAME    = "none"

		if USE_OVERLAY:
			global_status.update(f"{RYELLOW}Extracting game resources{RRESET}")

			# Extract game resources
			os.system(f"cd {root}/game/ && unrpa {RPA_NAME} > /dev/null 2> /dev/null")

			console.log(f"{RYELLOW}Extracted game resources{RRESET}")

			# Check if we need to convert the game scripts
			if not os.path.exists(f"{root}/{options_file}"):
				global_status.update(f"{RYELLOW}Decompiling script files{RRESET}")

				shutil.copy(f"{PATH}/payloads/global/un.rpy", f"{root}/game/")

				for file in os.listdir(f"{root}"):
					if ".sh" in file:
						os.system(f"{root}/{file}")

				os.remove(f"{root}/game/un.rpy")
				os.remove(f"{root}/game/un.rpyc")

				console.log(f"{RYELLOW}Decompiled script files{RRESET}")

			recoverable_RPA_name = RPA_NAME.split(".")[0]
			console.log(f"{RYELLOW}Moving {RPA_NAME} to {recoverable_RPA_name}._rpa{RRESET}")

			os.rename(f"{root}/game/{RPA_NAME}", f"{root}/game/{recoverable_RPA_name}._rpa")


		# Do annoying partial matches first
		global_status.update(f"{RYELLOW}Patching {options_file}{RRESET}")

		# Delete rpyc cache files
		try:
			os.remove(f"{root}/{options_file}c")
		except FileNotFoundError:
			console.log(RRED + f"Cache MISS for {options_file}" + RRESET)

		try:
			os.remove(f"{root}/{console_file}c")

		except FileNotFoundError:
			console.log(RRED + f"Cache MISS for {console_file}" + RRESET)

		### Patch options.rpy ###
		with open(f"{root}/{options_file}", "r+") as rwfile:
			startup_text_definition = open(f"{PATH}/payloads/global/strings/btext_overlay", "r").read() if USE_OVERLAY else open(f"{PATH}/payloads/global/strings/btext_no_overlay", "r").read()

			original_text = rwfile.read()
			rwfile.seek(0)

			for line in rwfile.readlines():
				if config_versi in line:
					### Change the version ID ###

					config_versi = line
					game_version = config_versi.split("\"")[1]

					console.log(RYELLOW + f"Detected game version: {game_version}, will overwrite!")

					writeable_string = cfg_v_overwr % f"config.version = \"{game_version}:Ajax\""
					patchfile_output = original_text.replace(f"config.version = \"{game_version}\"", writeable_string)

					patchfile_output = patchfile_output.replace("init python:", startup_text_definition, 1)

					rwfile.seek(0)
					rwfile.write(patchfile_output)
					rwfile.truncate()

		console.log(f"{RYELLOW}Patched {options_file}")
		global_status.update(f"{RYELLOW}Patching {options_file}{RRESET}")

		with open(f"{root}/{console_file}", "r+") as rwfile:
			original_text = rwfile.read()
			rwfile.seek(0)

			# Inject modifications
			# Developer mode check, unlocks the config file, and overwrites the license
			working = original_text.replace(dm_check, dmc_over)
			working = working.replace(cl_check, clc_over)
			working = working.replace(license, nlicense)

			rwfile.truncate(0)
			rwfile.write(working)

		try:
			with open(f"{root}/.jxGlobals", "x") as jxGlobals:
				jxGlobals.write("Miku Miku BEAAAAAAAAAAAAAAAAAAAAAM-")
				jxGlobals.flush()

		except FileExistsError:
			console.log("[bold red underline]Why are you running this with sanity checks disabled?[/]")

def _create_backup(game_root:str):
	with console.status(f"{RYELLOW}Backing up game"):
		if not os.path.exists(f"{PATH}/backups"):
			os.mkdir(f"{PATH}/backups")

		rrstamp = round(time.time())
		game_name = game_root.split("/")[len(game_root.split("/"))-1]

		backup_folder_path = f"{game_name}___{rrstamp}.bak"

		shutil.copytree(game_root, f"{PATH}/backups/{backup_folder_path}/")

		console.log(RYELLOW + f"Backup of {RPURPLE}{game_name}{RYELLOW} created ({RGREEN}{backup_folder_path}{RYELLOW})")

def _restore_backup(game_root:str):
	if os.path.exists(f"{PATH}/backups"):
		all_backups = os.listdir(f"{PATH}/backups")
		gme_backups = []
		game_name = game_root.split("/")[len(game_root.split("/"))-1]

		for backup in all_backups:
			if game_name in backup:
				gme_backups.append(backup)

		if len(gme_backups) > 0:
			gme_backups.append("Exit")

			selected_backup = questionary.select("Select a backup to restore", choices=gme_backups).ask()

			backup_path = f"{PATH}/backups/{selected_backup}"

			if os.path.exists(f"{backup_path}/game"):
				with console.status(f"{RYELLOW}Restoring backup"):
					try:
						shutil.rmtree(f"{game_root}/")
						shutil.copytree(f"{backup_path}", f"{game_root}")

					except Exception as err:
						console.log(RRED + "Failed to copy backup: " + str(err))

			else:
				print(RED + "This backup is not valid and will not be restored" + RESET)

		else:
			print(RED + "No backups are available for this game" + RESET)
			time.sleep(5)

	else:
		print(RED + "No backups are available" + RESET)
		time.sleep(5)

if GAME_OVERRIDE == None:
	game_root_directory = input(BLUE + "Game root directory (without trailing slash) > " + RESET)
else:
	game_root_directory = GAME_OVERRIDE

# Create a backup immediately
if (not NO_BACKUP) and (not FORCE_BACKUP):
	backup_action = questionary.select(message="Pre-Run Actions", choices=["Create Backup", "Restore Backup", "Continue"]).ask()
	if backup_action == "Create Backup":
		_create_backup(game_root_directory)

	elif backup_action == "Restore Backup":
		_restore_backup(game_root_directory)

elif FORCE_BACKUP:
	_create_backup(game_root_directory)

_games = os.listdir(f"{PATH}/payloads")
_game_list = []

for entry in _games:
	if entry != "global" and entry != "readme.md" and entry != "parasitic":
		_game_list.append(entry)

# Installation selection
available_for_install = []

# Basic injection
inject_global_patches = True
for game in KNOWN_BORKED_WITH_GLOBALS:
	if game in game_root_directory.lower():
		inject_global_patches = False

# Strings
lang_are_you_insane = ". SANITY CHECKS ARE DISABLED"
lang_global_patches = "Patches available on most games"
lang_starttwks = "Tweaks applied on game startup. Does not require Parasitic"
lang_parasitic = "The core Parasitic runtime"
lang_paraplugs = "Plugins extending Parasitic's features"

match [inject_global_patches, os.path.exists(f"{game_root_directory}/.jxGlobals"), IGNORE_CHECKS]:
	case [_, _, True]:
		available_for_install.append(questionary.Choice("Global patches", checked=True, description=lang_global_patches + lang_are_you_insane))

	case [True, False, _]:
		available_for_install.append(questionary.Choice("Global patches", checked=True, description=lang_global_patches))

	case [True, True, _]:
		available_for_install.append(questionary.Choice("Global patches", checked=False, disabled="Game is already patched"))

	case [False, _, _]:
		available_for_install.append(questionary.Choice("Global patches", checked=False, disabled="Global patches are known to break this game"))

available_for_install.append(questionary.Choice("Startup tweaks", checked=True, description=lang_starttwks))

if os.path.exists(f"{PATH}/parasitic") or IGNORE_CHECKS:
	if IGNORE_CHECKS:
		available_for_install.append(questionary.Choice("Parasitic", checked=True, description=lang_parasitic + lang_are_you_insane))
		available_for_install.append(questionary.Choice("Parasitic plugins", checked=True, description=lang_paraplugs + lang_are_you_insane))

	elif os.path.exists(f"{game_root_directory}/lib/python3.9") or os.path.exists(f"{game_root_directory}/lib/python3.12"):
		available_for_install.append(questionary.Choice("Parasitic", checked=True, description=lang_parasitic))
		available_for_install.append(questionary.Choice("Parasitic plugins", checked=True, description=lang_paraplugs))

	else:
		available_for_install.append(questionary.Choice("Parasitic", checked=False, disabled="Unsupported game"))
		available_for_install.append(questionary.Choice("Parasitic plugins", checked=False, disabled="Unsupported game"))

else:
	available_for_install.append(questionary.Choice("Parasitic", checked=False, disabled="Parasitic not in Ajax folder"))
	available_for_install.append(questionary.Choice("Parasitic plugins", checked=False, disabled="Parasitic not in Ajax folder"))

install_selection = questionary.checkbox("Select components to install", choices=available_for_install, style=CheckboxStyle).ask()

if "Global patches" in install_selection:
	try:
		_inject(game_root_directory)
	except Exception as err:
		print(RED + "Failed to inject global patches: " + str(err) + RESET)

if "Startup tweaks" in install_selection:
	try:
		os.mkdir(f"{game_root_directory}/game/startup")
	except:
		NotImplemented

	for startup_plugin in os.listdir(f"{PATH}/payloads/global/plugins_startup"):
		try:
			shutil.copy(f"{PATH}/payloads/global/plugins_startup/{startup_plugin}", f"{game_root_directory}/game/startup/")
			print(SPECIALDRIVE + "Plugin installed: " + MAGENTA + "startup/" + startup_plugin + RESET)

		except Exception as err:
			print(str(err))

if "Parasitic" in install_selection:
	try:
		os.mkdir(f"{game_root_directory}/game/plugins/")

	except Exception as err:
		NotImplemented

	if "Parasitic plugins" in install_selection:
		if FLAG_DEV:
			for dev_plugin in os.listdir(f"{PATH}/payloads/global/plugins_dev"):
				try:
					shutil.copy(f"{PATH}/payloads/global/plugins_dev/{dev_plugin}", f"{game_root_directory}/game/plugins/")
					print(MAGENTA + "Plugin installed: dev/" + dev_plugin + RESET)

				except Exception as err:
					print(str(err))

		for script in os.listdir(f"{PATH}/payloads/global/plugins"):
			try:
				shutil.copy(f"{PATH}/payloads/global/plugins/{script}", f"{game_root_directory}/game/plugins/")
				print(SPECIALDRIVE + "Plugin installed: " + MAGENTA + script + RESET)

			except FileExistsError:
				print(YELLOW + "Plugin already installed: " + MAGENTA + script + RESET)

			except Exception:
				print(RED + "Plugin not installed: " + MAGENTA + script + RESET)

	from parasitic.parasitic_installer import _installScript

	_installScript(PATH, game_root_directory)


_game_list.append("Exit Injector")

while True:
	_selectingPatch = True
	_game  = questionary.select(message="Select a game to patch", choices=_game_list).ask()

	if _game == "Exit Injector":
		sys.exit(0)

	_patches = os.listdir(f"{PATH}/payloads/{_game}/strings")
	_patch_list = []

	for entry in _patches:
		if (entry != "__pycache__") and (entry != "parasitic"):
			_patch_list.append(entry)

	_patch_list.append("Back")

	while _selectingPatch:
		_patch = questionary.select(message="Select a patch to install", choices=_patch_list).ask()

		if _patch == "Back":
			_selectingPatch = False

		elif ".json" in _patch:
			json_patches.apply_json_patch(game_root_directory, PATH, _patch, f"{PATH}/payloads/{_game}/strings/{_patch}", _inject)
			print("")

		else:
			_patch = _patch.split(".")[0]

			if os.path.exists(game_root_directory):
				exec(compile(f"import payloads.{_game}.strings.{_patch} as script", "DynamicallyLoadedScript", "exec"))

				try:
					script._runPatch(game_root_directory)
					print(YELLOW + "Patch finished, no errors were returned" + RESET)

				except Exception as err:
					print(RED + "Patch failed: " + str(err) + RESET)

			else:
				print(RED + "Path does not exist!" + RESET)
