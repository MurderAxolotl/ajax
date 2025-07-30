# Patch to fix broken names in RenPy games

import os
import sys
import shutil

PATH = sys.path[0]

def _runPatch(root:str):
	try:
		os.mkdir(f"{root}/game/plugins")
	except:
		NotImplemented

	shutil.copy(f"{PATH}/payloads/global/plugins/namefix.rpy", f"{root}/game/plugins/")

	print("Open the in-game console with shift+o and run `call namefix` to change your name")
	print("Alternatively, use Parasitic to run the script")
