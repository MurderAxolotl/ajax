import os
import sys
import shutil

import questionary

from rich.console import Console

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

pcon = Console(log_time=False, highlight=False)

# Loggin' stuff
def _log(text:str):
	pcon.log(f"[bold purple]ParasiticInstaller:[/]INFO : {text}")
	# print(f"{PURPLE}[ParasiticInstaller:{RESET}INFO{PURPLE}] {RESET}{text}")

def _warn(text:str):
	pcon.log(f"[bold purple]ParasiticInstaller:[/][bold yellow]WARN[bold orange] : {text}")
	# print(f"{PURPLE}[ParasiticInstaller:{YELLOW}WARN{PURPLE}] {ORANGE}{text}{RESET}")

def _err(text:str):
	pcon.log(f"[bold purple]ParasiticInstaller:[/][bold red]ERR : {text}")
	# print(f"{PURPLE}[ParasiticInstaller:{RED}ERR{PURPLE}] {RED}{text}{RESET}")

def _installScript(PATH:str, ROOT:str):
	if os.path.exists(f"{ROOT}/lib/python3.9"):
		detected_lib_version = "python3.9"

		_log(f"Installing Parasitic:39 to [bold pink]{ROOT}")

	elif os.path.exists(f"{ROOT}/lib/python3.12"):
		detected_lib_version = "python3.12"

		_log(f"Installing Parasitic:312 to [bold pink]{ROOT}")

	else:
		detected_lib_version = 0
		_err("This game is not compatible with Parasitic!")
		_err("No supported version of Python -- probably an old RenPy game")

		force_anyways = questionary.select("How should we proceed?", choices=["Install anyways", "Abort"]).ask()

		if force_anyways == "Install anyways":
			detected_lib_version = "python3.9"

			_warn("Forcing install on incompatible game!")
			_warn("Even if the install succeeds, Parasitic will most likely not work!")

	if detected_lib_version != 0:
		with pcon.status("Installing Parasitic") as pstatus:
			_log(f"Will use libs for [bold yellow]{detected_lib_version}[/]")

			try:
				os.mkdir(f"{ROOT}/_parasitic")
				_log("Made resources folder")

			except FileExistsError:
				NotImplemented

			except Exception:
				_warn("Couldn't make resources folder")

			try:
				pstatus.update("Installing PygameSDL2 libraries")
				for libfile in MIN_LIBS:
					try:
						shutil.copy(f"{PATH}/parasitic/lib/{detected_lib_version}/pygame_sdl2/{libfile}", f"{ROOT}/lib/{detected_lib_version}/pygame_sdl2/")
						_log(f"Installed shared library [bold pink]{libfile}")

					except Exception as err:
						if "No such file or directory" in str(err) and f"{detected_lib_version}/pygame_sdl2/" in str(err):
							_warn(f"Failed to install [bold pink]{libfile}")
						else:
							_warn(f"Failed to install [bold pink]{libfile}[/]:[bold red] " + str(err) + RESET)

			except Exception:
				_warn("")

			pstatus.update("Installing Parasitic libraries")

			try:
				shutil.copy(f"{PATH}/parasitic/resources/lib/parasitic.py", f"{ROOT}/lib/{detected_lib_version}/")
				_log("Installed ParasiticGUI")

			except Exception:
				_err("Failed to install ParasiticGUI")

			try:
				shutil.copy(f"{PATH}/parasitic/resources/lib/parasitic_lib.py", f"{ROOT}/lib/{detected_lib_version}/")
				_log("Installed Parsitic shared library")

			except Exception:
				_err("Failed to install Parasitic shared library")

			pstatus.update("Copying RenPy interfaces")

			for interface in os.listdir(f"{PATH}/parasitic/resources/interface"):
				try:
					shutil.copy(f"{PATH}/parasitic/resources/interface/{interface}", f"{ROOT}/game/")
					_log(f"Installed interface [bold pink]{interface}")

				except Exception:
					_warn(f"Failed to install interface [bold pink]{interface}")

			pstatus.update("Copying resources")

			try:
				shutil.copy(f"{PATH}/parasitic/resources/BitcountPropSingle.ttf", f"{ROOT}/_parasitic/")
				_log("Copied fonts")

			except Exception:
				_warn("Failed to copy fonts")

			try:
				shutil.copy(f"{PATH}/parasitic/resources/menu.ogg", f"{ROOT}/_parasitic/")
				_log("Copied GUI music")

			except Exception:
				_warn("Failed to copy GUI music")

			pstatus.update("Hooking RenPy")

			try:
				shutil.copy(f"{PATH}/parasitic/resources/00accessibility.rpy", f"{ROOT}/renpy/common/")
				_log("Hooked 00accessibility.rpy")

			except Exception:
				_warn("Failed to hook 00accessibility.rpy")

			try:
				ZZKM_SEARCH = "director = director.Start(),"
				ZZKM_REPLAC = 'director = renpy.curried_call_in_new_context("_parasitic_menu"),'

				ZZKM_SEARCH_2 = "director = [ 'noshift_K_d' ]"
				ZZKM_REPLAC_2 = "director = [ 'K_F5' ]"

				# Hatsune Miku?!
				with open(f"{ROOT}/renpy/common/00keymap.rpy", "r") as rin:
					zzkm_read = rin.read()

				zzkm_patched = zzkm_read.replace(ZZKM_SEARCH, ZZKM_REPLAC).replace(ZZKM_SEARCH_2, ZZKM_REPLAC_2)

				with open(f"{ROOT}/renpy/common/00keymap.rpy", "w") as leek:
					leek.truncate(0)
					leek.seek(0)

					leek.write(zzkm_patched)
					leek.flush()

				_log("Hooked 00keymap.rpy")

			except Exception:
				_warn("Failed to hook 00keymap.rpy")

			pstatus.update("Hooking script.rpy")

			# try:
			# 	SEARCH_PATTERN = "label start:"
			# 	REPLACE_PATTERN = """label start:
   #  show screen parasitic_input_eater nopredict"""

			# 	if os.path.exists(f"{ROOT}/game/script.rpy"):
			# 		file_to_write_to = f"{ROOT}/game/script.rpy"

			# 	else:
			# 		pstatus.update("Searching for start label")

			# 		file_to_write_to = ""

			# 		detected_files = []
			# 		for root, dirs, files in os.walk(f"{ROOT}/game/"):
			# 			for name in files:
			# 				if ".rpy" in name:
			# 					detected_files.append(os.path.join(root, name))

			# 		for file in detected_files:
			# 			pstatus.update("Searching for start label (trying " + file.split("/")[len(file.split("/"))-1] + ")")

			# 			try:
			# 				with open(file, "r") as readfile:
			# 					if SEARCH_PATTERN in readfile.read():
			# 						file_to_write_to = file
			# 						break

			# 			except Exception:
			# 				NotImplemented

			# 		if file_to_write_to == "":
			# 			_warn("Failed to find start label!")

			# 		else:
			# 			pstatus.update("Hooking " + file_to_write_to.split("/")[len(file_to_write_to.split("/"))-1])

			# 			with open(file_to_write_to, "r") as rf:
			# 				original_file = rf.read()

			# 			patched = original_file.replace(SEARCH_PATTERN, REPLACE_PATTERN)

			# 			with open(file_to_write_to, "w") as wf:
			# 				wf.truncate(0)
			# 				wf.seek(0)

			# 				wf.write(patched)
			# 				wf.flush()

			# 			_log("Hooked start label")

			# except Exception:
			# 	NotImplemented

			pstatus.update("Cleaning up")

			try:
				os.remove(f"{ROOT}/renpy/common/00accessibility.rpyc")
				_log("Cleared cached 00accessibility.rpy")

			except FileNotFoundError:
				NotImplemented #type:ignore

			except Exception:
				_warn("Failed to clear cached 00accessibility.rpy")

			try:
				os.remove(f"{ROOT}/renpy/common/00keymap.rpyc")
				_log("Cleared cached 00keymap.rpy")

			except FileNotFoundError:
				NotImplemented #type:ignore

			except Exception:
				_warn("Failed to clear cached 00keymap.rpy")

			_log("Parasitic installer finished")
