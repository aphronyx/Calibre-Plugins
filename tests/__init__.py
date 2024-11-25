import importlib.util
import sys


def import_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)  # pyright: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # pyright: ignore
    return module
