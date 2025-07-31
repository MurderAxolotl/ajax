label clean_namespace:
  python:
    #os = None
    #sys = None
    #parasitic = None
    #parasitic_lib = None
    #importlib = None
    renpy.store.os = None
    renpy.store.sys = None
    renpy.store.parasitic = None
    renpy.store.parasitic_lib = None
    renpy.store.importlib = None
    modulestoremove = ['os', 'sys', 'parasitic', 'parasitic_lib', 'importlib', '_log_warn', '_log', '_log_err']
    for index in range(len(renpy.game.log.log)):
     try:
       for item in renpy.game.log.log[index].stores['store']:
          if str(type(renpy.game.log.log[index].stores['store'][item])) == "<class 'module'>" or callable(renpy.game.log.log[index].stores['store'][item]):
           try:
             print("removing " + str(item))
             renpy.game.log.log[index].stores['store'][item] = None
           except Exception as err:
             NotImplemented
     except:
      NotImplemented
     try:
       for item in renpy.store:
          exec(compile(f"exec_output_1=str(type(renpy.store.{item}))", "ItemTest", "exec"))
          exec(compile(f"exec_output_2=callable(renpy.store.{item})", "ItemTest", "exec"))
          if exec_output_1 == "<class 'module'>" or exec_output_2:
           try:
             print("removing " + str(item))
             exec(compile(f"renpy.store.{item} = None", "ItemWrite", "exec"))
           except Exception as err:
             NotImplemented
     except:
      NotImplemented
