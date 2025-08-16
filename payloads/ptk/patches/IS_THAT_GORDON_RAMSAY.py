# Converts all of Rofi's sprites (and a few others, by accident) into Gordon Ramsay
# Also overwrites Rofi's name and colour

import os
import sys
import shutil

PATH = sys.path[0]

print("Oh yeah, it's Ramsey time :3")

def _runPatch(root:str):
	os.system(f"cd {root}/game && unrpa images.rpa")

	for file in os.listdir(f"{root}/game/images"):
		if "r " in file:
			print(f"{file} has been Ramsay'd")
			os.remove(f"{root}/game/images/{file}")

			shutil.copy(f"{PATH}/payloads/ptk/resources/definitely_rofi.png", f"{root}/game/images/{file}")

	with open(f"{root}/game/day1_3.rpy", "r+") as rwfile:
		script = rwfile.read()

		rwfile.seek(0)

		# rwfile.write(script.replace('define r = Character("Rofi", who_color ="f55436")', 'define r = Character("Gordon Ramsay", who_color ="f5c836")'))
		rwfile.write(script.replace('define r = Character("Rofi", who_color ="f55436")', 'define r = Character("Spooderman", who_color ="DF1F2D")'))
		rwfile.truncate()
