import shutil
import os
import sys
import questionary
import json
import time

PATH = sys.path[0]
AJVX = "12.1"

FLAG_DEV = True if os.getenv("_parasitic_dev") == "1" else False

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

KNOWN_BORKED_WITH_GLOBALS = ["raincheck"]

def _inject(root:str):
	""" Basic injection. No trailing slash """

	print(YELLOW + "Applying global patches" + RESET)
	print(YELLOW + "Target path: " + MAGENTA + root + RESET)

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
		print(f"{YELLOW}Extracting game resources from archive {MAGENTA}{RPA_NAME}{BLUE}")

		# Extract game resources
		os.system(f"cd {root}/game/ && unrpa {RPA_NAME}")

		# Check if we need to convert the game scripts
		if not os.path.exists(f"{root}/{options_file}"):
			print(YELLOW + "Converting script files to usable rpy files" + RESET)

			shutil.copy(f"{PATH}/payloads/global/un.rpy", f"{root}/game/")

			for file in os.listdir(f"{root}"):
				if ".sh" in file:
					os.system(f"{root}/{file}")

			os.remove(f"{root}/game/un.rpy")
			os.remove(f"{root}/game/un.rpyc")

		recoverable_RPA_name = RPA_NAME.split(".")[0]
		print(f"{MAGENTA}Moving {RPA_NAME} to {recoverable_RPA_name}._rpa{RESET}")

		os.rename(f"{root}/game/{RPA_NAME}", f"{root}/game/{recoverable_RPA_name}._rpa")


	# Do annoying partial matches first

	print(YELLOW + f"Patching {options_file}" + RESET)

	# Delete rpyc cache files
	try:
		os.remove(f"{root}/{options_file}c")
	except FileNotFoundError:
		print(RED + f"Cache MISS for {options_file}" + RESET)

	try:
		os.remove(f"{root}/{console_file}c")

	except FileNotFoundError:
		print(RED + f"Cache MISS for {console_file}" + RESET)

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

				print(YELLOW + f"Detected game version: {game_version}, will overwrite!")

				writeable_string = cfg_v_overwr % f"config.version = \"{game_version}:Ajax\""
				patchfile_output = original_text.replace(f"config.version = \"{game_version}\"", writeable_string)

				patchfile_output = patchfile_output.replace("init python:", startup_text_definition, 1)

				rwfile.seek(0)
				rwfile.write(patchfile_output)
				rwfile.truncate()

	print(YELLOW + f"Patching {console_file}" + RESET)

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

def _create_backup(game_root:str):
	if not os.path.exists(f"{PATH}/backups"):
		os.mkdir(f"{PATH}/backups")

	rrstamp = round(time.time())
	game_name = game_root.split("/")[len(game_root.split("/"))-1]

	backup_folder_path = f"{game_name}___{rrstamp}.bak"

	shutil.copytree(game_root, f"{PATH}/backups/{backup_folder_path}/")

	print(YELLOW + f"Backup of {MAGENTA}{game_name}{YELLOW} created ({SPECIALDRIVE}{backup_folder_path}{YELLOW}){RESET}")

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
				print(YELLOW + "Restoring backup..." + RESET)

				try:
					shutil.rmtree(f"{game_root}/")
					shutil.copytree(f"{backup_path}", f"{game_root}")

				except Exception as err:
					print(RED + "Failed to copy backup: " + str(err) + RESET)

			else:
				print(RED + "This backup is not valid and will not be restored" + RESET)

		else:
			print(RED + "No backups are available for this game" + RESET)
			time.sleep(5)

	else:
		print(RED + "No backups are available" + RESET)
		time.sleep(5)

game_root_directory = input(BLUE + "Game root directory (without trailing slash) > " + RESET)

# Create a backup immediately
backup_action = questionary.select(message="Pre-Run Actions", choices=["Create Backup", "Restore Backup", "Continue"]).ask()
if backup_action == "Create Backup":
	_create_backup(game_root_directory)

elif backup_action == "Restore Backup":
	_restore_backup(game_root_directory)

_games = os.listdir(f"{PATH}/payloads")
_game_list = []

for entry in _games:
	if entry != "global" and entry != "readme.md" and entry != "parasitic":
		_game_list.append(entry)

# Basic injection
do_not_inject_global_patches = False
for game in KNOWN_BORKED_WITH_GLOBALS:
	if game in game_root_directory.lower():
		do_not_inject_global_patches = True

if not do_not_inject_global_patches:
	inject_globals = questionary.select(message="Inject global patches?", choices=["Yes", "No"]).ask()

else:
	print(RED + "Global patches are known to break this game and are not available")
	inject_globals = "No"

if inject_globals == "Yes":
	_inject(game_root_directory)

if os.path.exists(f"{PATH}/parasitic"):
	if questionary.select(message="Install Parasitic?", choices=["Yes", "No"]).ask() == "Yes":
		from parasitic.parasitic_installer import _installScript

		_installScript(PATH, game_root_directory)

# if questionary.select(message="Install official plugins?", choices=["Yes", "No"]).ask() == "Yes":
if True:
	print(YELLOW + "Installing plugins..." + RESET)

	try:
		os.mkdir(f"{game_root_directory}/game/plugins/")

	except Exception as err:
		NotImplemented

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

_game_list.append("Exit Injector")

_game  = questionary.select(message="Select a game to patch", choices=_game_list).ask()

if _game ==  "Exit Injector":
	sys.exit(0)

_patches = os.listdir(f"{PATH}/payloads/{_game}/strings")
_patch_list = []

for entry in _patches:
	if (entry != "__pycache__") and (entry != "parasitic"):
		_patch_list.append(entry)

_patch_list.append("Exit Injector")

while True:
	_patch = questionary.select(message="Select a patch to install", choices=_patch_list).ask()

	if _patch == "Exit Injector":
		sys.exit(0)

	_patch = _patch.split(".")[0]

	if os.path.exists(game_root_directory):
		exec(compile(f"import payloads.{_game}.strings.{_patch} as script", "DynamicallyLoadedScript", "exec"))

		try:
			script._runPatch(game_root_directory)
		except Exception as err:
			print(RED + "Patch failed: " + str(err) + RESET)

		print(YELLOW + "Patch finished, no errors were returned" + RESET)

	else:
		print(RED + "Path does not exist!" + RESET)
