import os
import sys
import shutil

import questionary

MIN_LIBS = [
	"display.cpython-39-x86_64-linux-gnu.so",
	"font.cpython-39-x86_64-linux-gnu.so",
	"mixer.cpython-39-x86_64-linux-gnu.so",
	"mixer_music.cpython-39-x86_64-linux-gnu.so"
]

# Main colours
RED = "\u001b[1;31m"
ORANGE = "\u001b[1;38;5;202m"
YELLOW = "\u001b[33;1m"
GREEN = "\u001b[1;38;5;120m"
BLUE = "\u001b[38;5;87m"
PURPLE = "\u001b[1;35m"
SEAFOAM = "\u001b[1;38;5;85m"
RESET = "\u001b[0m"

# Extra colours
FILENAME = "\u001b[38;5;171m"
DISABLED = "\u001b[38;5;237m"

# Loggin' stuff
def _log(text:str):
	print(f"{PURPLE}[ParasiticInstaller:{RESET}INFO{PURPLE}] {RESET}{text}")

def _warn(text:str):
	print(f"{PURPLE}[ParasiticInstaller:{YELLOW}WARN{PURPLE}] {ORANGE}{text}{RESET}")

def _err(text:str):
	print(f"{PURPLE}[ParasiticInstaller:{RED}ERR{PURPLE}] {RED}{text}{RESET}")

def _installScript(PATH:str, ROOT:str):
	if os.path.exists(f"{ROOT}/lib/python3.9"):
		compatible = True

		_log(f"Installing Parasitic to {FILENAME}{ROOT}{RESET}")

	else:
		compatible = False
		_err("This game is not compatible with Parasitic")
		_err("Reason: does not use Python 3.9 -- probably an old RenPy game")

		force_anyways = questionary.select("How should we proceed?", choices=["Install anyways", "Abort"]).ask()

		if force_anyways == "Install anyways":
			compatible = True

			_warn("Forcing install on incompatible game!")
			_warn("Even if the install succeeds, Parasitic will most likely not work!")

	if compatible:
		try:
			os.mkdir(f"{ROOT}/_parasitic")
			_log("Made resources folder")

		except FileExistsError:
			_log("Resources folder already exists")

		except Exception as err:
			_warn("Couldn't make resources folder")

		try:
			for libfile in MIN_LIBS:
				try:
					shutil.copy(f"{PATH}/parasitic/lib/pygame_sdl2/{libfile}", f"{ROOT}/lib/python3.9/pygame_sdl2/")
					_log(f"Installed shared library {FILENAME}{libfile}{RESET}")

				except Exception as err:
					_warn(f"Failed to install {FILENAME}{libfile}{RESET}:{RED} " + str(err) + RESET)

		except Exception as err:
			_warn("")

		try:
			shutil.copy(f"{PATH}/parasitic/resources/lib/parasitic.py", f"{ROOT}/lib/python3.9/")
			_log("Installed ParasiticGUI")

		except Exception as err:
			_warn("Failed to install ParasiticGUI")

		try:
			shutil.copy(f"{PATH}/parasitic/resources/lib/parasitic_lib.py", f"{ROOT}/lib/python3.9/")
			_log("Installed Parsitic shared library")

		except Exception as err:
			_warn("Failed to install Parasitic shared library")

		for interface in os.listdir(f"{PATH}/parasitic/resources/interface"):
			try:
				shutil.copy(f"{PATH}/parasitic/resources/interface/{interface}", f"{ROOT}/game/")
				_log(f"Installed interface {FILENAME}{interface}{RESET}")

			except Exception as err:
				_warn(f"Failed to install interface {FILENAME}{interface}{RESET}")

		try:
			shutil.copy(f"{PATH}/parasitic/resources/BitcountPropSingle.ttf", f"{ROOT}/_parasitic/")
			_log(f"Copied fonts")

		except Exception as err:
			_warn(f"Failed to copy fonts")

		try:
			shutil.copy(f"{PATH}/parasitic/resources/menu.ogg", f"{ROOT}/_parasitic/")
			_log("Copied GUI music")

		except Exception as err:
			_warn(f"Failed to copy GUI music")

		try:
			shutil.copy(f"{PATH}/parasitic/resources/00accessibility.rpy", f"{ROOT}/renpy/common/")
			_log("Hooked 00accessibility.rpy")

		except Exception as err:
			_warn("Failed to hook 00accessibility.rpy")

		try:
			os.remove(f"{ROOT}/renpy/common/00accessibility.rpyc")
			_log("Cleared cached 00accessibility.rpy")

		except FileNotFoundError:
			NotImplemented #type:ignore

		except Exception as err:
			_warn("Failed to clear cached 00accessibility.rpy")

		print("Installer finished")
