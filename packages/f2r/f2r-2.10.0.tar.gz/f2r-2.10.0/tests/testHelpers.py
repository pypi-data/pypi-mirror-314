import unittest

from flp2rpm.helpers import parse_recipe_header, cache_recipe_header, load_yaml_from_file, run_subprocess


class TestHelpers(unittest.TestCase):
    def test_parse_recipe_header(self):
        self.assertEqual(len(cache_recipe_header), 0)
        header = parse_recipe_header("test_recipe.yml")
        self.assertNotEqual(header, None)
        self.assertEqual(header["package"], "Readout")
        self.assertEqual(len(header["requires"]), 15)
        self.assertEqual(len(cache_recipe_header), 1)

        # Rerun it -> it should use the cached value
        with self.assertLogs('', level='DEBUG') as cm:
            header2 = parse_recipe_header("test_recipe.yml")
            self.assertEqual(cm.output, ['DEBUG:root:Using cached recipe header: test_recipe.yml'])
            self.assertEqual(header2["package"], "Readout")
        self.assertEqual(len(cache_recipe_header), 1) # still only 1 item in the cache

    def test_load_yaml_from_file(self):
        result = load_yaml_from_file("test_runtime.yml")
        self.assertEqual(len(result["Python"]), 3)
        self.assertEqual(result["zlib"][0], "zlib")
        self.assertTrue("python3-pip" in result["Python"])

    def test_run_subprocess(self):
        output = run_subprocess("ls")
        self.assertTrue("testHelpers.py" in output)
        output = run_subprocess(["cd", "xxx"], failOnError=False)
        self.assertFalse(output)

if __name__ == '__main__':
    unittest.main()
