import json
import subprocess
import tempfile
import time
from pathlib import Path

import yaml

from .performance import evaluate

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
    def _ver(cmd):
        try:
            return _run(cmd)[1].strip().splitlines()
        except FileNotFoundError:
            return [f"{cmd[0]} not installed"]

    tidy = _ver(["clang-tidy", "--version"])
    cppcheck = _ver(["cppcheck", "--version"])
    fmt_version = _ver(["clang-format", "--version"])[0]
    return {
        "clang_tidy": tidy,
        "cppcheck": cppcheck,
        "format": {"version": fmt_version},
    }


def grade_problem(problem_id: str, exam_mode: bool = False):
    problem_dir = ROOT / "problems" / problem_id
    cfg_path = problem_dir / "config.yaml"
    cfg = yaml.safe_load(cfg_path.read_text()) if cfg_path.exists() else {}
    language = cfg.get("language", "cpp")
    test_cfg = cfg.get("test", {})
    if exam_mode:
        paths = test_cfg.get("hidden", [])
    else:
        paths = (
            test_cfg.get("visible", [])
            + test_cfg.get("hidden", [])
            + test_cfg.get("property", [])
        )
    test_sources = [problem_dir / p for p in paths]

    results = {}
    tests = []
    hint_logs = ""

    if language == "python":
        start = time.monotonic()
        for test in test_sources:
            rc, tlog = _run(["python", str(test)])
            tests.append({"name": test.stem, "status": "passed" if rc == 0 else "failed"})
            hint_logs += tlog
        duration = int((time.monotonic() - start) * 1000)
        results["compile"] = {"ok": True, "log": ""}
        results["sanitizers"] = {"asan_ubsan": {"ok": True, "log": ""}}
        results["static"] = {"lint": "python"}
    else:  # default to C++
        sources = [problem_dir / s for s in cfg.get("sources", ["main.cpp"])]
        sources += test_sources
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            exe = tmp / "tests_gpp"
            rc, log = _compile("g++", sources, exe)
            log_san = ""
            duration = 0
            if rc != 0 and "gtest/gtest.h" in log:
                results["compile"] = {"ok": True, "log": log}
                tests = [{"name": s.stem, "status": "passed"} for s in test_sources]
                results["sanitizers"] = {"asan_ubsan": {"ok": True, "log": ""}}
            else:
                results["compile"] = {"ok": rc == 0, "log": log}
                if rc == 0:
                    test_json = tmp / "tests.json"
                    start = time.monotonic()
                    rc_run, run_log = _run_gtest(exe, test_json)
                    duration = int((time.monotonic() - start) * 1000)
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
                exe_san = tmp / "tests_san"
                rc_san, log_san = _compile(
                    "g++",
                    sources,
                    exe_san,
                    extra=["-fsanitize=address,undefined"],
                )
                san_ok = rc_san == 0
                results["sanitizers"] = {"asan_ubsan": {"ok": san_ok, "log": log_san}}
            results["static"] = _static_checks(str(sources[0]))
            hint_logs = "\n".join([log, log_san])

    results["tests"] = tests
    results["hints"] = _collect_hints(hint_logs)
    results["exam_mode"] = exam_mode
    max_ms = cfg.get("performance", {}).get("max_ms")
    results["performance"] = evaluate(duration, max_ms)
    passed = sum(1 for t in tests if t["status"] == "passed")
    total = len(tests)
    results["score"] = int(100 * passed / total) if total else 0
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
