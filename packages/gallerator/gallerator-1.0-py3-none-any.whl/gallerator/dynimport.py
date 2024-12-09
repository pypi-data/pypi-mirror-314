import importlib.util
import random
import string
import sys


# https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
def import_from_path(module_name, file_path):
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# I don't care about the module name, so create a random one.
def import_random_module_from_path(file_path):
    module = 'dynimport_' + ''.join(random.choices(string.ascii_uppercase, k=20))
    return import_from_path(module, file_path)

if __name__ == "__main__":
    file = sys.argv[1]
    mod = import_random_module_from_path(file)
    print(mod.render())

