label _parasitic_menu:
 stop music
 python:
    import parasitic
    import parasitic_lib

    import sys
    import os

    import importlib
    importlib.reload(parasitic)
    importlib.reload(parasitic_lib)

    import parasitic
    from parasitic_lib import _log, _log_warn, _log_err

    from threading import Thread as thread

    if os.path.exists(sys.path[0] + "/_parasitic/no_music"):
      no_music = True
    else:
      no_music = False

    try:
        ec = parasitic._payload(sys.path[0], not no_music)
    except Exception as err:
        renpy.notify("     Parasitic has crashed     ")
        _log_err("GUI crashed! Caused by: " + str(err))
        ec = -666
   
    _preferences.fullscreen = True
    _preferences.fullscreen = False
    
    if ec != -666:
       renpy.notify("     Parasitic has relinquished control and blocked rollback     ")
    renpy.reset_physical_size()
    renpy.pause(0.1)
    renpy.set_physical_size(parasitic.RESOLUTION)
    renpy.pause(0.1)
    #renpy.restart_interaction()
    renpy.free_memory()
    renpy.block_rollback()

    renpy.pause(0.1)
    # Clean up namespace
    del parasitic
    del importlib
    del thread
    del os

    if ec == -2:
       del ec
       renpy.jump("start")

    elif ec == -1:
       del ec
       renpy.full_restart()

    elif ec == 1:
       del ec
       renpy.call("namefix")

    elif ec == 2:
       del ec
       renpy.call("pyshell")

    elif ec == 3:
       del ec
       renpy.call("pluglaunch")
    
    # Handle third-party plugins
    elif isinstance(ec, tuple):
      if ec[0] == 1000: 
         try: renpy.call(ec[1])
         except Exception as err: 
            renpy.notify("     Plugin has crashed     ")
            _log_err("Plugin crashed! Caused by: " + str(err))

    renpy.block_rollback()