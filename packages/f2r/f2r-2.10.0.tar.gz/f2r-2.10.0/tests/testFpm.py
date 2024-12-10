import unittest

from flp2rpm.Fpm import Fpm


class TestFpm(unittest.TestCase):
    def test_init(self):
        fpm = Fpm()
        self.assertEqual(fpm.architecture, 'x86_64')
        self.assertRegex(fpm.buildDir, '.*sw/slc8_x86-64')
        self.assertEqual(fpm.packagePrefix, 'o2-')
        self.assertGreater(len(fpm.runtimeDepsDict), 5)
        self.assertGreater(len(fpm.skipDeps), 1)
        self.assertEqual(fpm.targetDir, 'o2_rpms')
        self.assertEqual(fpm.release_suffix, 'slc8')

    def test_convert_deps_to_devel(self):
        fpm = Fpm()
        dependencies = {"o2":"v1.2", "boost":"from_system"}
        devs = fpm.convert_deps_to_devel(dependencies)
        self.assertEqual(devs, {"o2-devel":"v1.2"})

if __name__ == '__main__':
    unittest.main()
