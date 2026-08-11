"""Evals for the site's grounded answer engine.

The Q&A box on the portfolio makes two promises: it answers real questions
correctly, and it declines rather than inventing. Both are testable, so they
are tested — the same standard the crediting engine is held to.

qa_harness.js stubs a minimal DOM and runs the *shipped* retrieval code
unmodified, so these evals exercise what visitors actually get, not a
reimplementation of it.

    python3 tests/test_site_qa.py

Requires node. Skips (does not fail) when node is unavailable.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import site_qa  # noqa: E402


def main():
    node = shutil.which("node")
    if not node:
        print("skip: node not found (retrieval evals need it)")
        return 0

    harness = (Path(__file__).parent / "qa_harness.js").read_text()
    payload = site_qa.data_js() + site_qa.QA_JS
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(harness.replace("__PAYLOAD__", payload))
        script = fh.name

    proc = subprocess.run([node, script], capture_output=True, text=True)
    Path(script).unlink(missing_ok=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
