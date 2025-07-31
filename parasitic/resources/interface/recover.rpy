init python:
  persistent._loadedfromsnapshot = False

label _load_last_snapshot:
   python:
      persistent._loadedfromsnapshot = True
      renpy.load("99-9")
