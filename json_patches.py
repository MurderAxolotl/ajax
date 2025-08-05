import json

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

def apply_json_patch(game_root:str, PATH:str, patch_name:str, patch_file:str):
	""" Loads JSON patch rules and applies them """

	print(f"{YELLOW}Loading JSON patch from file {MAGENTA}{patch_name}{RESET}")

	patch = json.loads(open(patch_file, "r").read())

	# Load patch definitions
	PATCH_NAME = patch["patchName"]
	PATCH_AUTH = patch["patchAuth"]
	PATCH_DESC = patch["patchDesc"]

	PATCH_RULES = patch["rules"]

	print(f"{SPECIALDRIVE}Loaded patch: {MAGENTA}{PATCH_NAME}{SPECIALDRIVE} by {YELLOW}{PATCH_AUTH}{RESET}")
	print(f"{YELLOW}{PATCH_DESC}{RESET}\n")

	# Supported rule types:
	# REPLACE - replace matched text
	# INSERT_AFTER  - insert on new line after text
	# INSERT_BEFORE - insert on new line before text

	for rule in PATCH_RULES:
		rule_file = rule["file"]
		rule_name = rule["ruleName"]
		rule_type = rule["ruleType"]
		search    = rule["search"]

		match rule_type:
			case "REPLACE":
				replace = rule["replace"]
				print(YELLOW + f"{YELLOW}Applying rule {MAGENTA}{rule_name}{YELLOW} to {DRIVES}{rule_file}{RESET}")

				try:
					with open(f"{game_root}/game/{rule_file}", "r") as rf_read:
						fileText = rf_read.read()

					pf_patched = fileText.replace(search, replace)

					with open(f"{game_root}/game/{rule_file}", "w") as rf_write:
						rf_write.truncate(0)
						rf_write.seek(0)

						rf_write.write(pf_patched)
						rf_write.flush()

				except FileNotFoundError:
					print(f"{RED}Failed to apply rule {MAGENTA}{rule_name}{RED}: File not found{RESET}")

				except Exception as err:
					print(f"{RED}Failed to apply rule {MAGENTA}{rule_name}{RED}: {str(err)}{RESET}")

			case "INSERT_AFTER":
				insert = rule["insert"]

				print(YELLOW + f"{YELLOW}Applying rule {MAGENTA}{rule_name}{YELLOW} to {DRIVES}{rule_file}{RESET}")

				try:
					pf_patch_text = f"""{search}
{insert}"""
					with open(f"{game_root}/game/{rule_file}", "r") as rf_read:
						fileText = rf_read.read()

					pf_patched = fileText.replace(search, pf_patch_text)

					with open(f"{game_root}/game/{rule_file}", "w") as rf_write:
						rf_write.truncate(0)
						rf_write.seek(0)

						rf_write.write(pf_patched)
						rf_write.flush()

				except FileNotFoundError:
					print(f"{RED}Failed to apply rule {MAGENTA}{rule_name}{RED}: File not found{RESET}")

				except Exception as err:
					print(f"{RED}Failed to apply rule {MAGENTA}{rule_name}{RED}: {str(err)}{RESET}")

			case "INSERT_BEFORE":
				insert = rule["insert"]

				print(YELLOW + f"{YELLOW}Applying rule {MAGENTA}{rule_name}{YELLOW} to {DRIVES}{rule_file}{RESET}")

				try:
					pf_patch_text = f"""{insert}
{search}"""
					with open(f"{game_root}/game/{rule_file}", "r") as rf_read:
						fileText = rf_read.read()

					pf_patched = fileText.replace(search, pf_patch_text)

					with open(f"{game_root}/game/{rule_file}", "w") as rf_write:
						rf_write.truncate(0)
						rf_write.seek(0)

						rf_write.write(pf_patched)
						rf_write.flush()

				except FileNotFoundError:
					print(f"{RED}Failed to apply rule {MAGENTA}{rule_name}{RED}: File not found{RESET}")

				except Exception as err:
					print(f"{RED}Failed to apply rule {MAGENTA}{rule_name}{RED}: {str(err)}{RESET}")

			case _:
				print(YELLOW + f"{YELLOW}Rule {MAGENTA}{rule_name}{YELLOW}: unknown rule type {MAGENTA}{rule_type}{RESET}")
