import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from research_scaffold.cli import main
from research_scaffold.core import create, plan, slugify


class PlanTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Soil Microbes & Drought (2026)"), "soil_microbes_drought_2026")
        self.assertEqual(slugify("2026 study"), "p_2026_study")

    def test_basic_plan(self):
        dirs, files = plan("Soil Microbes", "Ada Lovelace", orcid="0000-0002-1825-0097", date="2026-01-01")
        self.assertIn("src/soil_microbes", dirs)
        self.assertIn("data/raw/.gitkeep", files)
        self.assertIn('family-names: "Lovelace"', files["CITATION.cff"])
        self.assertIn('orcid: "https://orcid.org/0000-0002-1825-0097"', files["CITATION.cff"])
        self.assertIn("python -m soil_microbes", files["README.md"])
        self.assertIn("data/raw/*", files[".gitignore"])

    def test_templates(self):
        dirs, files = plan("X", "A B", template="ml")
        self.assertIn("models", dirs)
        self.assertIn("configs/default.json", files)
        self.assertIn("manuscript/main.md", plan("X", "A B", template="paper")[1])
        with self.assertRaises(ValueError):
            plan("X", "A B", template="huge")
        with self.assertRaises(ValueError):
            plan("X", "A B", license="WTFPL")

    def test_create_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            dirs, files = plan("Proj", "A B")
            create(d, dirs, files)
            with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
                fh.write("mine")
            created, skipped = create(d, dirs, files)
            self.assertIn("README.md", skipped)
            with open(os.path.join(d, "README.md"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "mine")

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "proj")
            with redirect_stdout(io.StringIO()) as buf:
                main(["My Study", "-a", "Ada Lovelace", "-d", target, "-t", "paper"])
            self.assertIn("file(s) created", buf.getvalue())
            self.assertTrue(os.path.isfile(os.path.join(target, "src", "my_study", "__main__.py")))
            self.assertTrue(os.path.isdir(os.path.join(target, "manuscript", "sections")))


if __name__ == "__main__":
    unittest.main()
