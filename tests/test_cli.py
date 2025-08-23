import json
import subprocess
from pathlib import Path


def test_cli_outputs_json():
    repo_root = Path(__file__).resolve().parent.parent
    cmd = ["python", "-m", "grader.cli", "sum"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert "compile" in data
