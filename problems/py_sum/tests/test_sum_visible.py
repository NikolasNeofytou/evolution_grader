import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from main import sum_two


def test_small():
    assert sum_two(2, 3) == 5


def test_zero():
    assert sum_two(0, 0) == 0
