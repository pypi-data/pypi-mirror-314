import logging
import sys
import unittest

from flp2rpm.Module import Module

def on_macos():
    # this is necessary because at the moment we use (for an unknown reason) `script` when running a subprocess and that does not work on mac.
    return sys.platform.startswith('darwin')

class TestModule(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)

    @unittest.skipIf(on_macos(), "on mac we don't test modules")
    def test_versions(self):
        module_python = Module("Python-modules")
        versions = module_python.versions(True)
        self.assertGreater(len(versions), 0)
        versions2 = module_python.versions(False)
        self.assertGreater(len(versions2), len(versions))

    @unittest.skipIf(on_macos(), "on mac we don't test modules")
    def test_deps(self):
        boost = Module("boost")
        versions = boost.versions(True)
        deps = boost.deps(versions[0])
        self.assertIsNotNone(deps)
        deps_dict = boost.deps_as_dict(versions[0])
        self.assertEqual(len(deps), len(deps_dict))

# TODO test cache

if __name__ == '__main__':
    unittest.main()
