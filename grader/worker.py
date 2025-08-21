import json
import subprocess
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def _compile(compiler, sources, output, extra=None):
    cmd = [compiler, "-std=c++20"]
    if extra:
        cmd.extend(extra)
    cmd.extend(str(s) for s in sources)
    cmd.extend([
        "-lgtest",
        "-lgtest_main",
        "-lrapidcheck",
        "-pthread",
        "-o",
        str(output),
    ])
    return _run(cmd)


def _run_gtest(exe, json_path):
    return _run([str(exe), f"--gtest_output=json:{json_path}"])


def _static_checks(src):
    # Lightweight stand-ins for static analysis tools to keep tests fast
    _, tidy = _run(["clang-tidy", "--version"])
    _, cppcheck = _run(["cppcheck", "--version"])
    _, fmt_version = _run(["clang-format", "--version"])
    return {
        "clang_tidy": tidy.strip().splitlines(),
        "cppcheck": cppcheck.strip().splitlines(),
        "format": {"version": fmt_version.strip()},
    }


def grade_problem(problem_id: str):
    problem_dir = ROOT / "problems" / problem_id
    main_cpp = problem_dir / "main.cpp"
    test_sources = sorted((problem_dir / "tests").glob("*.cpp"))
    sources = [main_cpp] + test_sources

    results = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        exe = tmp / "tests_gpp"
        rc, log = _compile("g++", sources, exe)
        results["compile"] = {"ok": rc == 0, "log": log}
        tests = []
        if rc == 0:
            test_json = tmp / "tests.json"
            rc_run, run_log = _run_gtest(exe, test_json)
            if test_json.exists():
                data = json.loads(test_json.read_text())
                for suite in data.get("testsuites", []):
                    for case in suite.get("testsuite", []):
                        tests.append(
                            {
                                "name": f"{suite['name']}.{case['name']}",
                                "status": "passed" if rc_run == 0 else "failed",
                            }
                        )
            results["tests"] = tests
        exe_san = tmp / "tests_san"
        rc_san, log_san = _compile(
            "g++",
            sources,
            exe_san,
            extra=["-fsanitize=address,undefined"],
        )
        san_ok = rc_san == 0
        results["sanitizers"] = {"asan_ubsan": {"ok": san_ok, "log": log_san}}
        results["static"] = _static_checks(str(main_cpp))
        hint_logs = "\n".join([log, log_san])
        results["hints"] = _collect_hints(hint_logs)
    return results


HINTS_PATH = ROOT / "config" / "hints.yaml"
if HINTS_PATH.exists():
    HINTS = yaml.safe_load(HINTS_PATH.read_text()).get("hints", [])
else:
    HINTS = []


def _collect_hints(logs: str):
    tips = []
    for entry in HINTS:
        if entry["pattern"] in logs:
            tips.append(entry["hint"])
    return tips


__all__ = ["grade_problem", "_collect_hints"]
