label namefix:
    python:
        name = renpy.input("Ajax: Enter new name")
        NAME = name.upper()
        print("Ajax: Name changed!")
        print("Ajax: Press shift+o, or type exit, to close the console")
    "Ajax: Your name has been changed to [name]. This will only apply to future saves!"
    "Ajax: Of note, rolling back to before this change will revert your name"