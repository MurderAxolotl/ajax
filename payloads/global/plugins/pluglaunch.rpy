label pluglaunch:
   $ renpy.block_rollback()
   python:
      import sys, os
      plugs = os.listdir(sys.path[0] + "/game/plugins")
      
      valid_plugins = []
      
      for plugItem in plugs:
         if not "rpyc" in plugItem and os.path.isfile(sys.path[0] + "/game/plugins/" + plugItem):
            valid_plugins.append(plugItem)
            
      valid_plugins.append("EXIT PLUGLAUNCH")

      del sys, os, plugs

   $ renpy.block_rollback()
   call screen apluglaunch_dynamic_screen
   $ renpy.block_rollback()
   $ res = _return
   $ renpy.block_rollback()

   python:
      if not _return == "EXIT PLUGLAUNCH":
         try: renpy.call(_return.split(".")[0])
         except: renpy.notify("     Plugin has crashed     ")
      renpy.block_rollback()

style apluglaunch_dynamic_screen_tx_button:
    color "#fff"
    hover_color "#ffff00"
    outlines [ (absolute(3), "#000", absolute(0), absolute(0)) ]
    
screen apluglaunch_dynamic_screen():

    vbox:
        align (0.5, 0.5)
        for item in valid_plugins:
            textbutton "[item]" action Return(item) text_style "apluglaunch_dynamic_screen_tx_button"
            
