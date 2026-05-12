import os
import importlib
import logging

log = logging.getLogger("Yumi.Loader")

def load_modules(client, start_time):
    path = os.path.dirname(__file__)
    
    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("__"):
            name = file[:-3]
            try:
                mod = importlib.import_module(f"modules.{name}")
                if hasattr(mod, "register"):
                    mod.register(client, start_time)
                    log.info(f"OK: {name}")
            except Exception as e:
                log.error(f"FAIL {name}: {e}")
