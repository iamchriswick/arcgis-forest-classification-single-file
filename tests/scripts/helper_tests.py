#!/usr/bin/env python3
"""
Helper to run unittest (with or without coverage) without typing dotted paths.

Usage examples (tasks pass these automatically):
  python helper_tests.py --file <relativeFile> --root single_file_python_script --run
  python helper_tests.py --file <relativeFile> --symbol <selectedText> --root single_file_python_script --run
  python helper_tests.py --file <relativeFile> --root single_file_python_script --coverage
  python helper_tests.py single_file_python_script.tests.execution.test_x  # dotted path still supported
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

CONDA = r"C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\conda.exe"
ENV = "arcgispro-py3-3780"

WS_ROOT = (
    Path(__file__).resolve().parents[4]
)  # workspace root (adjusted from known script location)


def to_dotted(root_pkg: str, file_path: str, symbol: str | None) -> str:
    """
    Convert a file path (and optional symbol) into a unittest dotted path.

    root_pkg: top-level package (e.g., 'single_file_python_script')
    file_path: workspace-relative file path to a test module
    symbol: optional selected text (class or test function)
    """
    p = Path(file_path)
    if not p.suffix.lower() == ".py":
        raise ValueError(f"Not a Python file: {file_path}")

    # Build module dotted path starting from root_pkg
    try:
        rel = p.relative_to(WS_ROOT)
    except ValueError:
        # fall back: assume given path is already relative
        rel = Path(file_path)

    parts = list(rel.parts)
    # Trim everything up to root_pkg
    if root_pkg in parts:
        idx = parts.index(root_pkg)
        parts = parts[idx:]
    else:
        # If the path doesn't include root_pkg, assume it's already rooted
        pass

    # Drop .py and join with dots
    if parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    dotted = ".".join(parts)

    # If symbol provided, sanitize and append
    if symbol:
        # Grab likely class or test function token from selection
        m = re.search(r"([A-Za-z_][A-Za-z0-9_]*)", symbol)
        if m:
            dotted = f"{dotted}.{m.group(1)}"
    return dotted


def run_unittest(dotted: str) -> int:
    cmd = [CONDA, "run", "-n", ENV, "python", "-m", "unittest", dotted, "-v"]
    print("🧪", " ".join(cmd))
    return subprocess.call(cmd, cwd=WS_ROOT)


def run_coverage(dotted: str, source_root: str) -> int:
    # Coverage run
    run_cmd = [
        CONDA,
        "run",
        "-n",
        ENV,
        "python",
        "-m",
        "coverage",
        "run",
        "--branch",
        f"--source={source_root}",
        "-m",
        "unittest",
        dotted,
        "-v",
    ]
    print("📈", " ".join(run_cmd))
    rc = subprocess.call(run_cmd, cwd=WS_ROOT)
    # Coverage report (always show; exit code follows run)
    report_cmd = [
        CONDA,
        "run",
        "-n",
        ENV,
        "python",
        "-m",
        "coverage",
        "report",
        "--show-missing",
    ]
    subprocess.call(report_cmd, cwd=WS_ROOT)
    return rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "dotted", nargs="?", help="Optional direct dotted path (unittest syntax)"
    )
    ap.add_argument(
        "--file", help="Workspace-relative file path (e.g. ${relativeFile})"
    )
    ap.add_argument(
        "--symbol", help="Optional class/test symbol (e.g. ${selectedText})"
    )
    ap.add_argument(
        "--root", default="single_file_python_script", help="Top-level package root"
    )
    ap.add_argument("--run", action="store_true", help="Run unittest")
    ap.add_argument("--coverage", action="store_true", help="Run coverage + unittest")
    args = ap.parse_args()

    # Determine dotted path
    if args.dotted:
        dotted = args.dotted
    elif args.file:
        dotted = to_dotted(args.root, args.file, args.symbol)
    else:
        print(
            "Provide either a dotted path or --file <path> (with optional --symbol).",
            file=sys.stderr,
        )
        return 2

    print(f"Detected dotted path: {dotted}")

    if args.coverage:
        # Source root for coverage = '<root>/src' if it exists, else '<root>'
        src_candidate = WS_ROOT / args.root / "src"
        source_root = f"{args.root}/src" if src_candidate.exists() else args.root
        return run_coverage(dotted, source_root)

    # default run
    return run_unittest(dotted)


if __name__ == "__main__":
    sys.exit(main())
