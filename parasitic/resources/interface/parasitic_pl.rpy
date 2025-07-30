label _parasitic_handToPlugLaunch:
   python:
      import os
      import sys

      PATH = sys.path[0]

      if os.path.exists(f"{PATH}/game/plugins/pluglaunch.rpy"):
         del os, sys, PATH
         renpy.call("pluglaunch")
      else:
         renpy.notify("     PlugLaunch isn't installed. Launch plugins through Parasitic     ")
      del os
      del sys
      renpy.block_rollback()