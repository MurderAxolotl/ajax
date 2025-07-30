A project to allow injecting code and other things into RenPy games fairly easily

## About Repository

This repository contains two projects:
- **Ajax** is the *static* patch installer
- **Parasitic** is the *dynamic* plugin runtime

Ajax patches are static, meaning they're directly written into the game and are non-interactive.

Parasitic plugins are dynamic and can be run at any time in-game. Parasitic has control over these.

## Install and use

First, make sure you install questionary with `pip install questionary`

Then, you can run these commands to clone and run the code:

```
git clone git@github.com:psychon-night/ajax12.git

cd ajax12

python main.py
```

It'll ask for your game's directory. Just paste something like `/home/user/Games/renpy-game` and it'll figure the rest out!

## Accessing Parasitic

All Parasitic features can be accessed by pressing Shift+A. Along the bottom of the screen, there are a few buttons:

- `Return` - Closes the accessibility menu
- `Parasitic` - Launches the Parasitic UI
- `Plugins` - Opens the plugin launcher, assuming `plugins/pluglaunch.rpy` is installed

If, for some reason, Shift+A is non-functional, you can also do the following:

1. Press Shift+O (that's o as in orange)
2. Type `call _parasitic_menu` and hit enter

## Plugins in Parasitic

Parasitic supports running custom .rpy scripts in-game. Place your .rpy file in the `plugins` folder in the game directory and Parasitic will pick up on it

### Cool, how do I launch 3rd-party plugins?

The number keys (1-9) in Parasitic UI launch 3rd-party plugins. 

Alternatively, there is an official plugin to launch 3rd party plugins using a mouse. You can access it by pressing Shift + A and clicking `Plugins`

## File Structure

Generally, here's the breakdown of the folder structure:

`main.py` - the actual mod manager itself\
`/payloads/` - where payloads are held\
`/payloads/game_name/` - contains patches for specific games\
`/payloads/game_name/resources/` - holds files for your patches. Images, videos, rpy files, etc\
`/payloads/game_name/strings/` - Despite the name, this is where your actual patches go

## Making static patches

1. Following the structure detailed above, create your game's folder
2. Create a Python file (for example, `cool_patch.py`)
3. Include the entrypoint `def _runPatch(root:str):`
   - Ajax calls this function to run your patch
	- `root` always contains the path to the game, which is always a valid folder

The patch manager calls `_runPatch`, so define it like this: `def _runPatch(root:str):` and write your patch inside.

For examples on writing patches, look at the patches that ship with the repo. `/payloads/ptk/name_fixer.py` is the simplest example

## Making dynamic plugins

These are really just rpy scripts, look at the RenPy docs for help on writing them.

Keep in mind, you need to make sure your `label` matches the file's name! For example, if your plugin is called `cool_plugin.rpa`, your `label` must be `label cool_plugin`, or Parasitic won't be able to run it

## Making dynamic (startup) plugins

These are also just rpy scripts... but use `init:` instead of `label:`

The file name is unimportant, Parasitic doesn't manage these at all.

***You should place startup plugins in the game's `startup` folder***

## FINAL WARNINGS

There are a few files you should be careful with:
- `00library.rpy`
- `options.rpy`
- `00accessibility.rpy`

These files are edited, either by global patches or Parasitic, and may not be exactly what you expect.

***Never*** blindly overwrite `00accessibility.rpy`! Not only does this make games less accessible, it also prevents the player from opening Parasitic!