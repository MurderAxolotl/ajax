label pyshell:
    python:
        _psExit = False

        while not _psExit:
            shellInput = renpy.input("PyShell")

            if shellInput.lower() == "exit":
                _psExit = True

            exec(compile(shellInput, "DynamicallyLoadedScript", "exec"))
