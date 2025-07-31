label _parasitic_handToPlugLaunch:
   python:
    try:renpy.save("99-9")
    except:NotImplemented
    if not persistent._loadedfromsnapshot:
      import os
      import sys

      PATH = sys.path[0]

      if os.path.exists(f"{PATH}/game/plugins/pluglaunch.rpy"):
         renpy.call("pluglaunch")

      else:
         renpy.notify("     PlugLaunch isn't installed. Launch plugins through Parasitic     ")

      modulestoremove = ['os', 'sys', 'parasitic', 'parasitic_lib', 'importlib', '_log_warn', '_log', '_log_err']
      for index in range(len(renpy.game.log.log)):
            for item in modulestoremove:
               try:
                  del renpy.game.log.log[index].stores['store'][item]
               except Exception as err:
                  NotImplemented
      renpy.block_rollback()
    else:
     persistent._loadedfromsnapshot = False
     renpy.call("clean_namespace")
     renpy.block_rollback()
   $ renpy.call("clean_namespace")
   $ renpy.call("clean_namespace")
   $ renpy.call("clean_namespace")
