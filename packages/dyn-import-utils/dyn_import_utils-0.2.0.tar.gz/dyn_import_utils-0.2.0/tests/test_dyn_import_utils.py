import unittest
import os
import sys
import re
import dyn_import_utils

class TestDynImportUtils(unittest.TestCase):

    def setUp(self):
        # Ensure the tests directory is in sys.path so we can import from there
        test_dir = os.path.dirname(__file__)
        dyn_import_utils.add_sys_path(test_dir)
        self.module_path = os.path.join(test_dir, "test_module.py")
        self.package_dir = os.path.join(test_dir, "test_package")

    def test_01_import_module(self):
        module = dyn_import_utils.import_module(self.module_path)
        self.assertTrue(hasattr(module, "hello"))
        self.assertEqual(module.hello(), "Hello, world!")

    def test_02_import_package(self):
        package = dyn_import_utils.import_package(self.package_dir)
        self.assertTrue(hasattr(package, "hello"))
        self.assertEqual(package.hello(), "Hello from package!")

    def test_03_import_package_submodule(self):
        package = dyn_import_utils.import_package(self.package_dir)
        self.assertTrue(hasattr(package, "greet"))
        self.assertEqual(package.greet(), "Greetings from submodule!")

    def test_04_import_same_module_twice(self):
        module_first = dyn_import_utils.import_module(self.module_path)
        module_second = dyn_import_utils.import_module(self.module_path)
        self.assertIs(module_first, module_second)

    def test_05_import_same_package_twice(self):
        package_first = dyn_import_utils.import_package(self.package_dir)
        package_second = dyn_import_utils.import_package(self.package_dir)
        self.assertIs(package_first, package_second)

    def test_06_add_sys_path(self):
        # Ensure '/dyn_import_utils' is not already in sys.path
        match = any(re.search(r"/dyn_import_utils$", path) for path in sys.path)
        self.assertFalse(match, f"Unexpectedly found dyn_import_utils in sys.path before adding it.")
    
        # Add the path
        relative_path = '../dyn_import_utils'
        absolute_path = os.path.abspath(relative_path)
        dyn_import_utils.add_sys_path(relative_path)
    
        # Check the last entry in sys.path matches the added path
        self.assertEqual(sys.path[-1], absolute_path, f"Expected {absolute_path} to be the last entry in sys.path.")

if __name__ == "__main__":
    unittest.main(verbosity=2)

