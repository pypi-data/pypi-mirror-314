import unittest

from flp2rpm.Package import Package
from testModule import on_macos


class TestPackage(unittest.TestCase):
    @unittest.skipIf(on_macos(), "on mac we can't test stuff related to modules")
    def test_init(self):
        package = Package(name='boost', version='v1.83.0-alice2-local1')
        self.assertIsNotNone(package)
        self.assertEqual(package.name, 'boost')
        self.assertRegex(package.path, r'.*flp-to-rpm/tests/alidist/boost.sh')
        self.assertEqual(package.requires.count('zlib'), 1)
        # TODO check the special case where the dependencies are overwritten by the defaults.
        self.assertEqual(package.tag, "v1.83.0-alice2")
        self.assertEqual(package.devel.count('lzma'), 1)
        self.assertEqual(package.module_version, 'v1.83.0-alice2-local1')
        self.assertGreater(len(package.module_dep_versions), 2)

    @unittest.skipIf(on_macos(), "on mac we can't test stuff related to modules")
    def test_get_deps(self):
        package = Package(name='QualityControl', version='v1.162.4')
        requires = []
        filtered = package.filter_dependencies(requires)
        self.assertEqual(len(filtered), 0)
        requires = ["O2", "boost"]
        filtered = package.filter_dependencies(requires)
        self.assertEqual(len(filtered), 2) # todo

    @unittest.skipIf(on_macos(), "on mac we can't test stuff related to modules")
    def test_deps_with_versions(self):
        package = Package(name='QualityControl', version='v1.162.4')
        dict_deps_versions = package.deps_with_versions()
        self.assertEqual(dict_deps_versions['boost'], 'from_system') # todo
        self.assertEqual(dict_deps_versions['O2'], 'from_system') # todo

if __name__ == '__main__':
    unittest.main()
