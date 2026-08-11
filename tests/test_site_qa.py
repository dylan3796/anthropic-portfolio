"""Evals for the site's answer engine, its chat client, and the chat Worker.

Three promises are testable, so all three are tested — the same standard the
crediting engine is held to:

  1. retrieval  — answers correctly, and declines rather than inventing
  2. chat client — uses the live model, and degrades to retrieval when it can't
  3. worker      — refuses foreign origins, caps input, rate-limits, contains
                   upstream failures without leaking them

Each harness drives the *shipped* code (stubbed DOM, stubbed fetch, stubbed KV)
rather than a reimplementation of it.

    python3 tests/test_site_qa.py

Requires node. Skips (does not fail) when node is unavailable.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import site_qa  # noqa: E402


def _run(node, script, cwd=None):
    proc = subprocess.run([node, script], capture_output=True, text=True, cwd=cwd)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def _render(harness_name, endpoint, suffix=".js"):
    """Inline the shipped client into a harness and write it next to the tests.

    It lands in tests/ so the harness's relative imports still resolve.
    """
    harness = (HERE / harness_name).read_text()
    payload = site_qa.data_js() + site_qa.QA_JS
    fh = tempfile.NamedTemporaryFile("w", suffix=suffix, dir=HERE, delete=False)
    with fh:
        fh.write(harness.replace("__PAYLOAD__", payload))
    return fh.name


def main():
    node = shutil.which("node")
    if not node:
        print("skip: node not found (these evals need it)")
        return 0

    failures = 0

    # 1 + 2. retrieval, then the chat client with a live endpoint configured
    for label, harness, endpoint in (
        ("retrieval", "qa_harness.js", ""),
        ("chat client", "chat_harness.js", "https://ask-dylan.example.workers.dev"),
    ):
        original = site_qa.CHAT_ENDPOINT
        site_qa.CHAT_ENDPOINT = endpoint
        script = _render(harness, endpoint)
        site_qa.CHAT_ENDPOINT = original
        print(f"\n== {label} ==")
        failures |= _run(node, script)
        Path(script).unlink(missing_ok=True)

    # 3. the Worker's guards, against a stubbed provider
    print("\n== worker guards ==")
    failures |= _run(node, str(HERE / "worker_harness.mjs"), cwd=str(ROOT))

    return failures


if __name__ == "__main__":
    raise SystemExit(main())
