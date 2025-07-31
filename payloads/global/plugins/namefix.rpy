label namefix:
    python hide:
        renpy.store.name = renpy.input("NameFix: Enter new name")
        renpy.store.NAME = name.upper()

        # Test for `mc` and overwrite it if it's a string
        try:
           if isinstance(renpy.store.mc, str):
              renpy.store.mc = name
              renpy.store.MC = NAME
        except:
           NotImplemented
        print("Name changed!")
        print("Press shift+o, or type exit, to close the console")
    $ renpy.block_rollback()
    $ renpy.notify(f"     Name changed to {name}    ")
