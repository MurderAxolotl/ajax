import os
import json
import shutil

import modules.colour as colour

from rich.console import Console

from modules.colour import RED, RESET

def global_patch_inject(root:str, IGNORE_CHECKS:bool, PATH:str, AJAX_VERSION:str):
	""" Basic injection. No trailing slash """

	console = Console(log_time=False)

	if os.path.exists(f"{root}/.jxGlobals") and not IGNORE_CHECKS:
		print(RED + "Global patches have already been applied. Stop." + RESET)
		return

	with console.status(f"{colour.rich.YELLOW}Applying global patches{colour.rich.RESET}") as global_status:
		console.log(colour.rich.YELLOW + "Target path: " + colour.rich.PURPLE + root)

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
		nlicense = console_definitions["replacements"][2] % AJAX_VERSION

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
			global_status.update(f"{colour.rich.YELLOW}Extracting game resources{colour.rich.RESET}")

			# Extract game resources
			os.system(f"cd {root}/game/ && unrpa {RPA_NAME} > /dev/null 2> /dev/null")

			console.log(f"{colour.rich.YELLOW}Extracted game resources{colour.rich.RESET}")

			# Check if we need to convert the game scripts
			if not os.path.exists(f"{root}/{options_file}"):
				global_status.update(f"{colour.rich.YELLOW}Decompiling script files{colour.rich.RESET}")

				shutil.copy(f"{PATH}/payloads/global/un.rpy", f"{root}/game/")

				for file in os.listdir(f"{root}"):
					if ".sh" in file:
						os.system(f"{root}/{file}")

				os.remove(f"{root}/game/un.rpy")
				os.remove(f"{root}/game/un.rpyc")

				console.log(f"{colour.rich.YELLOW}Decompiled script files{colour.rich.RESET}")

			recoverable_RPA_name = RPA_NAME.split(".")[0]
			console.log(f"{colour.rich.YELLOW}Moving {RPA_NAME} to {recoverable_RPA_name}._rpa{colour.rich.RESET}")

			os.rename(f"{root}/game/{RPA_NAME}", f"{root}/game/{recoverable_RPA_name}._rpa")


		# Do annoying partial matches first
		global_status.update(f"{colour.rich.YELLOW}Patching {options_file}{colour.rich.RESET}")

		# Delete rpyc cache files
		try:
			os.remove(f"{root}/{options_file}c")
		except FileNotFoundError:
			console.log(colour.rich.RED + f"Cache MISS for {options_file}" + colour.rich.RESET)

		try:
			os.remove(f"{root}/{console_file}c")

		except FileNotFoundError:
			console.log(colour.rich.RED + f"Cache MISS for {console_file}" + colour.rich.RESET)

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

					console.log(colour.rich.YELLOW + f"Detected game version: {game_version}, will overwrite!")

					writeable_string = cfg_v_overwr % f"config.version = \"{game_version}:Ajax\""
					patchfile_output = original_text.replace(f"config.version = \"{game_version}\"", writeable_string)

					patchfile_output = patchfile_output.replace("init python:", startup_text_definition, 1)

					rwfile.seek(0)
					rwfile.write(patchfile_output)
					rwfile.truncate()

		console.log(f"{colour.rich.YELLOW}Patched {options_file}")
		global_status.update(f"{colour.rich.YELLOW}Patching {options_file}{colour.rich.RESET}")

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
