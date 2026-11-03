import unittest
import pdf_compressor as pc


class BuildCommandTest(unittest.TestCase):
    def test_options(self):
        cmd = pc.build_command("gs", "a.pdf", "b.pdf", dpi=100, quality=30)
        self.assertIn("-dColorImageResolution=100", cmd)
        self.assertIn("-sOutputFile=b.pdf", cmd)
        self.assertEqual(cmd[-1], "a.pdf")
        self.assertEqual(cmd[-2], "-f")
        self.assertTrue(any("/QFactor" in c for c in cmd))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            pc.build_command("gs", "a", "b", quality=0)
        with self.assertRaises(ValueError):
            pc.build_command("gs", "a", "b", dpi=0)


if __name__ == "__main__":
    unittest.main()
