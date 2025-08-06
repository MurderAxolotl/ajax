## File Structure

Generally, here's the breakdown of the folder structure:

`main.py` - the actual mod manager itself\
`/payloads/` - where payloads are held\
`/payloads/game_name/` - contains patches for specific games\
`/payloads/game_name/resources/` - holds files for your patches. Images, videos, rpy files, etc\
`/payloads/game_name/strings/` - Despite the name, this is where your actual patches go

## Patch Scripts

These are Python files called by Ajax. These provide far more flexibility, as *you* write all of the code yourself

1. Following the structure detailed above, create your game's folder
2. Create a Python file (for example, `cool_patch.py`)
3. Include the entrypoint `def _runPatch(root:str):`
   - Ajax calls this function to run your patch
	- `root` always contains the path to the game, which is always a valid folder

The patch manager calls `_runPatch`, so define it like this: `def _runPatch(root:str):` and write your patch inside.

Here's a simple example patch:

```python
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
```

## Quick Aside

As a quick aside, let's focus just on disabling the splash screen. Using a patch script:

```python
import os
import sys

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
```

And you would need to write this for each text replacement. In comparison, here's the JSON definition file to do the same thing:
```json
{
	"patchName": "Remove Splash Screen",
	"patchAuth": "MurderAxolotl",
	"patchDesc": "Remove the splash screen from supported games",
	"needsGlbs": true,

	"rules": [
		{
			"file": "script.rpy",
			"ruleName": "Insert RETURN on SplashScreen",
			"ruleType": "INSERT_AFTER",
			"search": "label splashscreen:",
			"insert": "    return"
		}
	]
}
```

The advantage is that this is quickly reusable, easier to read, and easier to modify.
