# Cleans up TB's UI by removing all custom on-screen elements

import os
import sys
import shutil

PATH = sys.path[0]
PATCHED_SCREEN = f"{PATH}/payloads/temptations_ballad/resources/screens.rpy"

def _runPatch(root:str):
	print("Patching TB install: " + root)
	print(f"Using patched screens: {PATCHED_SCREEN}")

	os.remove(f"{root}/game/screens.rpy")

	try:
		os.remove(f"{root}/game/screens.rpyc")

	except FileNotFoundError:
		print("Cache miss!")

	shutil.copy(PATCHED_SCREEN, f"{root}/game/")

	print("Screen patched")
