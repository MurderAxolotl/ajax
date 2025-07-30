# Minor QoL tweaks for Silverstone, rolled into one lovely little patch

import os
import sys
import shutil

PATH = sys.path[0]

def _runPatch(root:str):
	search_pattern = "label splashscreen:"
	replac_pattern = """label splashscreen:
    return"""

	print("Removing splash animation...")

	with open(f"{root}/game/script.rpy", "r") as readfile:
		original_text = readfile.read()

	new_text = original_text.replace(search_pattern, replac_pattern)

	with open(f"{root}/game/script.rpy", "w") as writefile:
		writefile.truncate(0)
		writefile.seek(0)

		writefile.write(new_text)

	print("Replacing screen manager...")

	os.remove(f"{root}/game/screens.rpy")
	shutil.copy(f"{PATH}/payloads/silverstone/resources/screens.rpy", f"{root}/game/")

	try:
		os.remove(f"{root}/game/screens.rpyc")
	except FileNotFoundError:
		NotImplemented #type:ignore
