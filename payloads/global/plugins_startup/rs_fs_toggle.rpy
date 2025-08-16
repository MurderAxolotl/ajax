init 999 python hide:
   from parasitic_lib import _log
   config.pad_bindings['pad_rightstick_press'] = ["toggle_fullscreen"]
   _log("Mapped right stick to Fullscreen Toggle")

   del _log
