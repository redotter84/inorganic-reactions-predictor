import pkgutil
import importlib as imp

def load_functs():
    for _, m, _ in pkgutil.iter_modules(__path__):
        module = "reacts.organic.classes." + m
        module = imp.import_module(module)
        rs = [x for x in dir(module) if x[0 : 2] == "r_"]
        for x in rs:
            yield getattr(module, x)
