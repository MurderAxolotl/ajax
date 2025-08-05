A project to allow injecting code and other things into RenPy games (somewhat) easily

## About Repository

This repository contains two projects:
- **Ajax** is the *static* patch installer
- **Parasitic** is the *dynamic* plugin runtime

Ajax patches are static, meaning they're directly written into the game and are non-interactive.

Parasitic plugins are dynamic and can be run at any time in-game. Parasitic has control over these.

## Install and use

Make sure you have the following Python modules installed:
- questionary (`pip install questionary`)

Then, make sure you have the following system packages installed:
- Python 3 (3.10 minimum, 3.12 recommended)
- git

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
- `Cleanup` - Tries to fix in-memory issues to fix saving. See the warnings for users

If you want to directly launch the Parasitic GUI, press F5

If, for some reason, Shift+A and F5 are non-functional, you can also do the following:

1. Press Shift+O (that's o as in orange)
2. Type `call _parasitic_menu` and hit enter

This will open the full Parasitic GUI, from which you can access all available features

## Plugins in Parasitic

Parasitic supports running custom .rpy scripts in-game. Place your .rpy file in the `plugins` folder in the game directory and Parasitic will pick up on it

#### Cool, how do I launch 3rd-party plugins?

The number keys (1-9) in the Parasitic GUI launch 3rd-party plugins.

Alternatively, there is an official plugin to launch 3rd party plugins using a mouse. You can access it by pressing Shift + A and clicking `Plugins`

## Supported Games

Any modern RenPy game should be supported. However, some older VNs are NOT supported. Generally:
-  Games using RenPy 8 are supported
-  Games using RenPy 7 and older are NOT supported

The Parasitic installer will check for compatibility before installation and warn you of any issues

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

## WARNINGS - USERS

#### Game Window

The Parasitic GUI has to forcefully take control of the game window, which can result in funky behaviour, including:
- Losing the maximize window control
- Resizing to 1024x576
- Being forced into windowed mode
- Losing the ability to resize the window
- Preferred window mode (fullscreen / windowed) being lost

#### Rollback

Due to the nature of RenPy, rollback (e.g. going backwards in the game) can accidentally re-run previous actions and break the game state. To prevent this, all official plugins and the Parasitic GUI will ***block rollback***

#### Saving

Always save before trying to launch Parasitic features! It can become impossible to save if a serious error occurs!

##### What do I do when saving breaks??

First, you should try the "Cleanup" button (available when you press Shift+A). This will try to clean up any issues left behind. Afterwards, try to save!

The Parasitic GUI always saves the game state to a separate file when you open it. Should saving still be broken, open the console and run `call _run_last_snapshot`

Please note that these snapshots are only created when opening the Parasitic GUI and official plugin launcher. No other entry points will create these snapshots!

## WARNINGS - DEVELOPERS

#### IMPORTANT PRACTICES

Because of how RenPy handles saving the game, imported modules ***completely break save files*** in the normal store. To avoid this problem, all Python blocks should be `python hide:` instead of `python:`

However, this also means you must use `renpy.store.variable` instead of `variable`. Example: `renpy.store.preferences.fullscreen` instead of `preferences.fullscreen`

Additionally, ***any non-picklable objects*** will cause serious breakages with saving. You should avoid them where possible!

Official plugin entrypoints will do their best to clean up after you, but Parasitic will only clear out:

- Functions
- Modules

Other non-picklable ojects ***are not handled***

#### Modified files
There are a few files you should be careful with:
- `00library.rpy`
- `options.rpy`
- `00accessibility.rpy`
- `00keymap.rpy`

These files are edited, either by global patches or Parasitic, and may not be exactly what you expect.

***Never*** blindly overwrite `00accessibility.rpy`! Not only does this make games less accessible, it also prevents the player from opening Parasitic!

#### Imports

Plugins SHOULD NOT `import parasitic` or `import parasitic_lib`! There are certain situations where these will not be available, and trying to import them will throw an exception.

If you absolutely must import them, wrap the code in a `try/except` block. A plugin should always fail gracefully instead of making RenPy eat the error

## ATTRIBUTIONS

This repository ships code from other places, namely:

- Modified files from the RenPy Engine: https://github.com/renpy/renpy
- Compiled dynamic libraries from PygameSDL2: https://github.com/renpy/pygame_sdl2
- UnRPYC: https://github.com/CensoredUsername/unrpyc
