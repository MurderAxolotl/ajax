label pluglaunch:
   $ renpy.block_rollback()
   python hide:
      import sys, os
      plugs = os.listdir(sys.path[0] + "/game/plugins")

      renpy.store.valid_plugins = []

      for plugItem in plugs:
         if not "rpyc" in plugItem and os.path.isfile(sys.path[0] + "/game/plugins/" + plugItem) and not "pluglaunch" in plugItem:
            plugin_item_stacksafe = str(plugItem.split(".")[0])
            renpy.store.valid_plugins.append(plugin_item_stacksafe)

      renpy.store.valid_plugins.append("EXIT PLUGLAUNCH")
   $ renpy.call("clean_namespace")


   $ renpy.block_rollback()
   call screen apluglaunch_dynamic_screen
   $ renpy.block_rollback()
   $ res = _return
   $ renpy.block_rollback()

   python hide:
      if not renpy.store.res == "EXIT PLUGLAUNCH":

         renpy.call(renpy.store.res)
         try: renpy.call(renpy.store.res)
         except Exception as err: renpy.notify("     Plugin has crashed     "); print("Plugin crashed: " + str(err))
      renpy.block_rollback()
   $ renpy.call("clean_namespace")

style apluglaunch_dynamic_screen_tx_button:
    color "#fff"
    hover_color "#ffff00"
    outlines [ (absolute(3), "#000", absolute(0), absolute(0)) ]

screen apluglaunch_dynamic_screen():

    vbox:
        align (0.5, 0.5)
        for item in valid_plugins:
            textbutton "[item]" action Return(item) text_style "apluglaunch_dynamic_screen_tx_button"
