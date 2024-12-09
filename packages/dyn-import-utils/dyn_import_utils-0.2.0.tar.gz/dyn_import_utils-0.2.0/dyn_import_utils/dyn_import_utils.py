import importlib.util
import sys
import os
import inspect

def _create_path(path):
    if os.path.isabs(path):
        return path
    caller_frame = inspect.stack()[2]
    caller_file_path = os.path.dirname(caller_frame.filename)
    res_path = os.path.join(caller_file_path, path)
    res_path = os.path.abspath(res_path)
    return res_path

def add_sys_path(path):
    sys_path = _create_path(path)
    if sys_path not in sys.path:
        sys.path.append(sys_path)

def import_module(path):
    file_path = _create_path(path)

    if file_path.endswith('.py'):
        if not os.path.exists(file_path):
            raise ImportError(f"Cannot find file: {file_path}")
    else:
        if not os.path.exists(file_path):
            file_path += '.py'
        if not os.path.exists(file_path):
            raise ImportError(f"Cannot find file: {file_path}")

    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # Check if module already exists in sys.modules
    if module_name in sys.modules:
        return sys.modules[module_name]

    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise ImportError(f"Failed to load module '{module_name}' from '{file_path}': {e}")
 
        # Register the loaded module into sys.modules
        sys.modules[module_name] = module
        return module
    else:
        raise ImportError(f"Cannot load '{file_path}'")

def import_package(path):
    dir_path = _create_path(path)

    # Check if it's a directory
    if not os.path.isdir(dir_path):
        raise ImportError(f"The path '{dir_path}' is not a directory.")

    # Check for __init__.py
    init_file_path = os.path.join(dir_path, "__init__.py")
    if not os.path.exists(init_file_path):
        raise ImportError(f"No '__init__.py' found in directory '{dir_path}'.")

    # Derive package name from the directory name
    package_name = os.path.basename(dir_path.rstrip('/\\'))

    # Check if package already exists in sys.modules
    if package_name in sys.modules:
        return sys.modules[package_name]
 
    # Create module spec for the package
    spec = importlib.util.spec_from_file_location(package_name, init_file_path)
    if spec and spec.loader:
        package = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(package)
        except Exception as e:
            raise ImportError(f"Failed to load package '{package_name}' from '{dir_path}': {e}")

        # Register the loaded package into sys.modules
        sys.modules[package_name] = package
        return package
    else:
        raise ImportError(f"Cannot load package '{package_name}' from '{dir_path}'")

