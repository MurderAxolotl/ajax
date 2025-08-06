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
