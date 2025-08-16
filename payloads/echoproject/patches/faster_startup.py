# Patch to remove the annoying startup animation in Echo Project games

def _runPatch(root:str):
	try:
		with open(f"{root}/game/script.rpy", "r+") as init_script:
			text = init_script.read()
			init_script.seek(0)

			init_script.write(text.replace("label splashscreen:", """label splashscreen:
    return"""))

	except FileNotFoundError:
		print("Failed to write to script file. Verify this is an Echo Project game")
