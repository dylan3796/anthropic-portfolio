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


def prompt_contract():
    """Hermetic guard: the sections the stand-in's behavior depends on must
    survive every future edit to SYSTEM_PROMPT. Live behavior is tested in
    tests/prompt_evals.py (needs a provider key); this pins the text."""
    prompt = site_qa.system_prompt()
    required = [
        "The one rule that matters",
        "Mapping a requirement to listed experience",
        "Transfers",                              # the maximalist verdict exists
        "Never claim the unlisted thing itself",  # the honesty line that funds it
        "argue the transfer",                     # instruction, not just a label
        "never lead with the",                    # the no-deficit-first rule
        "Dossier — everything you know about Dylan",
    ]
    missing = [r for r in required if r not in prompt]
    for r in required:
        mark = "ok  " if r not in missing else "FAIL"
        print(f"{mark}  prompt contains: {r!r}")
    jd_required = ["FIT CHECK", "TRANSFERS", "RAMP", "NOT LISTED", "never soften"]
    jd_missing = [r for r in jd_required if r not in site_qa.JD_INSTRUCTION]
    for r in jd_required:
        mark = "ok  " if r not in jd_missing else "FAIL"
        print(f"{mark}  jd instruction contains: {r!r}")
    return 1 if (missing or jd_missing) else 0


def main():
    node = shutil.which("node")

    print("== prompt contract ==")
    failures = prompt_contract()

    if not node:
        print("skip: node not found (the remaining evals need it)")
        return failures

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
