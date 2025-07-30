import os
import sys
import shutil

MIN_LIBS = [
	"display.cpython-39-x86_64-linux-gnu.so",
	"font.cpython-39-x86_64-linux-gnu.so",
	"mixer.cpython-39-x86_64-linux-gnu.so",
	"mixer_music.cpython-39-x86_64-linux-gnu.so"
]

def _installScript(PATH:str, ROOT:str):
	print("Testing for compatibility...")

	if os.path.exists(f"{ROOT}/lib/python3.9"):
		compatible = True

		print("Compatible! Proceeding with install")

	else:
		compatible = False
		print("Not compatible! Abort!")

	if compatible:
		try:
			os.mkdir(f"{ROOT}/_parasitic")

		except Exception as err:
			print(str(err))

		try:
			# shutil.copytree(f"{PATH}/parasitic/lib/pygame_sdl2", f"{ROOT}/lib/python3.9/pygame_sdl2")
			for libfile in MIN_LIBS:
				shutil.copy(f"{PATH}/parasitic/lib/pygame_sdl2/{libfile}", f"{ROOT}/lib/python3.9/pygame_sd2/")

				print(f"Copying lib/pygame_sdl2/{libfile}")

		except Exception as err:
			print(str(err))

		try:
			shutil.copy(f"{PATH}/parasitic/resources/lib/parasitic.py", f"{ROOT}/lib/python3.9/")

		except Exception as err:
			print(str(err))

		try:
			shutil.copy(f"{PATH}/parasitic/resources/lib/parasitic_lib.py", f"{ROOT}/lib/python3.9/")

		except Exception as err:
			print(str(err))

		for interface in os.listdir(f"{PATH}/parasitic/resources/interface"):
			try:
				shutil.copy(f"{PATH}/parasitic/resources/interface/{interface}", f"{ROOT}/game/")

			except Exception as err:
				print(str(err))

		try:
			shutil.copy(f"{PATH}/parasitic/resources/BitcountPropSingle.ttf", f"{ROOT}/_parasitic/")

		except Exception as err:
			print(str(err))

		try:
			shutil.copy(f"{PATH}/parasitic/resources/menu.ogg", f"{ROOT}/_parasitic/")

		except Exception as err:
			print(str(err))

		try:
			shutil.copy(f"{PATH}/parasitic/resources/00accessibility.rpy", f"{ROOT}/renpy/common/")

		except Exception as err:
			print(str(err))

		try:
			os.remove(f"{ROOT}/renpy/common/00accessibility.rpyc")

		except Exception as err:
			print(str(err))

		print("Parasitic installed! Launch the game and press Shift+A, then click 'Parasitic' to get started")
