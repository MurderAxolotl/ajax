label _parasitic_menu:
 stop music
 python:
  try:renpy.save("99-9")
  except:NotImplemented
  if not persistent._loadedfromsnapshot:

    renpy.suspend_rollback(True)
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

    renpy.store.preferences.fullscreen = not renpy.store.preferences.fullscreen
    renpy.store.preferences.fullscreen = not renpy.store.preferences.fullscreen

    if ec != -666 and ec != 2000:
       renpy.notify("     Parasitic has relinquished control and blocked rollback     ")
    elif ec == 2000:
       renpy.notify("     Parasitic GUI updated!     ")
    renpy.reset_physical_size()
    renpy.pause(0.1)
    renpy.set_physical_size(parasitic.RESOLUTION)
    renpy.pause(0.1)
    #renpy.restart_interaction()
    renpy.free_memory()

    renpy.pause(0.1)

    os = None
    sys = None
    parasitic = None
    parasitic_lib = None
    importlib = None

    modulestoremove = ['os', 'sys', 'parasitic', 'parasitic_lib', 'importlib']
    for index in range(len(renpy.game.log.log)):
       for item in modulestoremove:
          try:
             renpy.game.log.log[index].stores['store'].pop(item)
          except Exception as err:
             NotImplemented

    if ec == -2:
       renpy.jump("start")

    elif ec == -1:
       renpy.full_restart()

    elif ec == 1:
       renpy.call("namefix")

    elif ec == 3:
       renpy.call("pluglaunch")

    # Handle third-party plugins
    elif isinstance(ec, tuple):
      if ec[0] == 1000:
         try: renpy.call(ec[1])
         except Exception as err:
            renpy.notify("     Plugin has crashed     ")
            _log_err("Plugin crashed! Caused by: " + str(err))

    os = None
    sys = None
    parasitic = None
    parasitic_lib = None
    importlib = None
    renpy.store.os = None
    renpy.store.sys = None
    renpy.store.parasitic = None
    renpy.store.parasitic_lib = None
    renpy.store.importlib = None
    modulestoremove = ['os', 'sys', 'parasitic', 'parasitic_lib', 'importlib', '_log_warn', '_log', '_log_err']
    for index in range(len(renpy.game.log.log)):
       for item in modulestoremove:
          try:
             renpy.game.log.log[index].stores['store'][item] = None
          except Exception as err:
             NotImplemented

    renpy.block_rollback()
    renpy.suspend_rollback(False)
  else:
    persistent._loadedfromsnapshot = False
    renpy.call("clean_namespace")
    renpy.block_rollback()
 $ renpy.suspend_rollback(False)
 $ renpy.call("clean_namespace")
 $ renpy.call("clean_namespace")
 $ renpy.call("clean_namespace")
