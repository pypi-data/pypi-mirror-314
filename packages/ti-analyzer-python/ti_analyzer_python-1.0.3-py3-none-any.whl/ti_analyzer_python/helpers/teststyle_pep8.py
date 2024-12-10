import unittest
from pathlib import Path

import pycodestyle
import os

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = BASE_DIR / 'pycodestyle.ini'
IGNORE_MODULES = []


def get_source_files() -> list[str]:
    parent_dir = Path(os.path.dirname(BASE_DIR))
    for filename in parent_dir.glob('**/*.py'):
        s = str(filename)

        # Некоторые модули, или устарели, или являются внешними (ala.py), поэтому пропускаем их!
        if any(s.endswith(x) for x in IGNORE_MODULES):
            continue

        yield s


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_something():
        """Test that we conform to PEP-8."""
        style = pycodestyle.StyleGuide(config_file=CONFIG_FILE)
        result = style.check_files(get_source_files())

        if result.total_errors:
            result.print_statistics()

        assert result.total_errors == 0, 'Found code style errors (and warnings).'


if __name__ == '__main__':
    unittest.main()
