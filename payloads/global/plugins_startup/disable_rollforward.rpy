init 999 python:
   from parasitic_lib import _log
   config.keymap['toggle_skip'].remove('K_TAB')
   _log("Rollforward toggle disabled")

   del _log