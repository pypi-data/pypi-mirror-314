import unittest
import os
import tempfile
import shutil
import sys
import dyn_import_utils

class TestDynImporter(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test modules/packages
        self.temp_dir = tempfile.mkdtemp()

        # Create a test module (standalone)
        self.module_code = "GLOBAL_VAR = 42\ndef hello(): return 'Hello, world!'"
        self.module_path = os.path.join(self.temp_dir, "test_module.py")
        with open(self.module_path, "w") as f:
            f.write(self.module_code)

        # Create a test package
        self.package_dir = os.path.join(self.temp_dir, "test_package")
        os.mkdir(self.package_dir)
        
        # __init__.py for the package
        init_code = "from .test_submodule import greet\nGLOBAL_VAR = 99\ndef hello(): return 'Hello from package!'\n"
        with open(os.path.join(self.package_dir, "__init__.py"), "w") as f:
            f.write(init_code)
        
        # Create a submodule in the package
        submodule_code = "def greet(): return 'Greetings from submodule!'"
        submodule_path = os.path.join(self.package_dir, "test_submodule.py")
        with open(submodule_path, "w") as f:
            f.write(submodule_code)

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)

    def test_import_module(self):
        module = dyn_import_utils.import_module(self.module_path)
        self.assertTrue(hasattr(module, "hello"))
        self.assertEqual(module.hello(), "Hello, world!")

    def test_import_package(self):
        package = dyn_import_utils.import_package(self.package_dir)
        self.assertTrue(hasattr(package, "hello"))
        self.assertEqual(package.hello(), "Hello from package!")

    def test_import_package_submodule(self):
        package = dyn_import_utils.import_package(self.package_dir)
        # Access submodule function via package import (since __init__.py imports it)
        self.assertTrue(hasattr(package, "greet"))
        self.assertEqual(package.greet(), "Greetings from submodule!")

    def test_add_sys_path(self):
        path = self.temp_dir
        dyn_import_utils.add_sys_path(path)
        self.assertIn(path, sys.path)

    def test_import_same_module_twice(self):
        # First import
        module_first = dyn_import_utils.import_module(self.module_path)
        # Second import (should be retrieved from sys.modules and be the same object)
        module_second = dyn_import_utils.import_module(self.module_path)
        self.assertIs(module_first, module_second)
        self.assertEqual(module_first.GLOBAL_VAR, 42)
        self.assertEqual(module_second.GLOBAL_VAR, 42)

    def test_import_same_package_twice(self):
        # First import
        package_first = dyn_import_utils.import_package(self.package_dir)
        # Second import (should come from sys.modules)
        package_second = dyn_import_utils.import_package(self.package_dir)
        self.assertIs(package_first, package_second)
        self.assertEqual(package_first.GLOBAL_VAR, 99)
        self.assertEqual(package_second.GLOBAL_VAR, 99)

    def test_import_non_existent_module(self):
        non_existent_path = os.path.join(self.temp_dir, "no_such_module.py")
        with self.assertRaises(ImportError):
            dyn_import_utils.import_module(non_existent_path)

    def test_import_non_existent_package(self):
        non_existent_dir = os.path.join(self.temp_dir, "no_such_package")
        with self.assertRaises(ImportError):
            dyn_import_utils.import_package(non_existent_dir)

if __name__ == "__main__":
    unittest.main()

