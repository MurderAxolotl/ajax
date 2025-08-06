A project to allow injecting code and other things into RenPy games (somewhat) easily

## About Repository

This repository contains two projects:
- **Ajax** is the *static* patch installer
- **Parasitic** is the *dynamic* plugin runtime

Ajax patches are static, meaning they're directly written into the game and are non-interactive.

Parasitic plugins are dynamic and can be run at any time in-game. Parasitic has control over these.

Users: see [user warnings](https://github.com/psychon-night/ajax/blob/main/docs/warn_users.md)\
Developers: see [developer warnings](https://github.com/psychon-night/ajax/blob/main/docs/warn_devs.md)

## Install and use

Make sure you have the following Python modules installed:
- questionary (`pip install questionary`)
- rich (`pip install rich`)
- unrpa (`pip install unrpa`)

Then, make sure you have the following system packages installed:
- Python 3 (3.10 minimum, 3.12 recommended)
- git

Then, you can run these commands to clone and run the code:

```
git clone git@github.com:psychon-night/ajax.git
cd ajax12
python main.py
```

It'll ask for your game's directory. Just paste something like `/home/user/Games/renpy-game` and it'll figure the rest out!

### Command Line Arguments

Ajax supports a few command line arguments:
- `-g "game_folder"` / `--game "game_folder"` - Patch game_folder
- `-i` / `--ignore_checks` - Ignore sanity checks
- `-b` / `--backup` - Automatically force a backup
- `-n` / `--no_backup` - Do not ask abvout backups

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

There are two kinds of static patches: *patch scripts* and *JSON patch definitions*

JSON patch definitions are quick and easy to create. However, they can be fairly limited, as they only support a few actions.

Patch scripts require Python knowledge, but they are far more powerful - YOU write the code that modifies the game however you want!

For additional details:

Refer to [the JSON patch definitions page](https://github.com/psychon-night/ajax/tree/main/docs/json_patch_definitions.md)\
Refer to [the patch script page](https://github.com/psychon-night/ajax/tree/main/docs/patch_scripts.md)

## Making dynamic plugins

These are really just RenPy scripts, look at the RenPy docs for help on writing them.

Keep in mind, you need to make sure your `label` matches the file's name! For example, if your plugin is called `cool_plugin.rpa`, your `label` must be `label cool_plugin`, or Parasitic won't be able to run it

## Making startup tweaks

These are also just RenPy scripts... but use `init:` instead of `label:`

These do not have the same file name restrictions as plugins, as Parasitic doesn't directly run these

***You should place startup plugins in the game's `startup` folder***

## ATTRIBUTIONS

This repository ships code from other places, namely:

- Modified files from the RenPy Engine: https://github.com/renpy/renpy
- Compiled dynamic libraries from PygameSDL2: https://github.com/renpy/pygame_sdl2
- UnRPYC: https://github.com/CensoredUsername/unrpyc
