import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from main import sum_two


def test_negatives():
    assert sum_two(-4, 1) == -3
