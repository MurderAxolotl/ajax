import shutil
import os
import sys
import questionary
import time
import argparse
import dotenv

import modules.colour       as colour
import modules.json_patches as json_patches

from rich.console import Console
from questionary  import Style

from modules.colour         import RED, YELLOW, SPECIALDRIVE, MAGENTA, RESET
from modules.global_patches import global_patch_inject

dotenv.load_dotenv(".env")

DEFAULT_DIR = os.getenv("GAME_DIR", "")

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

def _create_backup(game_root:str):
	with console.status(f"{colour.rich.YELLOW}Backing up game"):
		if not os.path.exists(f"{PATH}/backups"):
			os.mkdir(f"{PATH}/backups")

		rrstamp = round(time.time())
		game_name = game_root.split("/")[len(game_root.split("/"))-1]

		backup_folder_path = f"{game_name}___{rrstamp}.bak"

		shutil.copytree(game_root, f"{PATH}/backups/{backup_folder_path}/")

		console.log(colour.rich.YELLOW + f"Backup of {colour.rich.PURPLE}{game_name}{colour.rich.YELLOW} created ({colour.rich.GREEN}{backup_folder_path}{colour.rich.YELLOW})")

def _get_num_backups(game_root:str):
	if os.path.exists(f"{PATH}/backups"):
		all_backups = os.listdir(f"{PATH}/backups")
		gme_backups = []
		game_name = game_root.split("/")[len(game_root.split("/"))-1]

		for backup in all_backups:
			if game_name in backup:
				gme_backups.append(backup)

		return len(gme_backups)

	return 0

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
				with console.status(f"{colour.rich.YELLOW}Restoring backup"):
					try:
						shutil.rmtree(f"{game_root}/")
						shutil.copytree(f"{backup_path}", f"{game_root}")

					except Exception as err:
						console.log(colour.rich.RED + "Failed to copy backup: " + str(err))

			else:
				print(RED + "This backup is not valid and will not be restored" + RESET)

		else:
			print(RED + "No backups are available for this game" + RESET)
			time.sleep(5)

	else:
		print(RED + "No backups are available" + RESET)
		time.sleep(5)

if GAME_OVERRIDE is None:
	# game_root_directory = input(BLUE + "Game root directory (without trailing slash) > " + RESET)
	wd = DEFAULT_DIR if DEFAULT_DIR != "" else os.getcwd()
	game_root_directory = questionary.path("Game root directory", only_directories=True, default=wd).ask()
else:
	game_root_directory = GAME_OVERRIDE

if game_root_directory is None:
	sys.exit(0)

# Create a backup immediately
if (not NO_BACKUP) and (not FORCE_BACKUP):
	num_backups = _get_num_backups(game_root_directory)

	bops = [
		questionary.Choice("Create backup", description="Creates a backup of the selected game")
	]

	if num_backups > 0:
		bops.append(questionary.Choice("Restore backup", description=f"Restore a backup. {num_backups} backups available"))
	else:
		bops.append(questionary.Choice("Restore backup", description="Restore a backup", disabled="No backups exist"))

	bops.append(questionary.Choice("Continue", description="Continue to Ajax"))

	backup_action = questionary.select(message="Backup Manager", choices=bops).ask()
	if backup_action == "Create backup":
		_create_backup(game_root_directory)

	elif backup_action == "Restore backup":
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

if install_selection is None:
	sys.exit(0)

if "Global patches" in install_selection:
	try:
		global_patch_inject(game_root_directory, IGNORE_CHECKS, PATH, AJVX)
	except Exception as err:
		print(RED + "Failed to inject global patches: " + str(err) + RESET)

if "Startup tweaks" in install_selection:
	try:
		os.mkdir(f"{game_root_directory}/game/startup")

	except Exception:
		NotImplemented #type:ignore

	for startup_plugin in os.listdir(f"{PATH}/payloads/global/plugins_startup"):
		try:
			shutil.copy(f"{PATH}/payloads/global/plugins_startup/{startup_plugin}", f"{game_root_directory}/game/startup/")
			print(SPECIALDRIVE + "Plugin installed: " + MAGENTA + "startup/" + startup_plugin + RESET)

		except Exception as err:
			print(str(err))

if "Parasitic" in install_selection:
	try:
		os.mkdir(f"{game_root_directory}/game/plugins/")

	except Exception:
		NotImplemented #type:ignore

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

	_patches = os.listdir(f"{PATH}/payloads/{_game}/patches")
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
			json_patches.apply_json_patch(game_root_directory, PATH, _patch, f"{PATH}/payloads/{_game}/patches/{_patch}", global_patch_inject, IGNORE_CHECKS, AJVX)
			print("")

		else:
			_patch = _patch.split(".")[0]

			if os.path.exists(game_root_directory):
				exec(compile(f"import payloads.{_game}.strings.{_patch} as script", "DynamicallyLoadedScript", "exec"))

				try:
					script._runPatch(game_root_directory) #type:ignore
					print(YELLOW + "Patch finished, no errors were returned" + RESET)

				except Exception as err:
					print(RED + "Patch failed: " + str(err) + RESET)

			else:
				print(RED + "Path does not exist!" + RESET)
