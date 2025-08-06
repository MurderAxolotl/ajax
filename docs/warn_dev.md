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
