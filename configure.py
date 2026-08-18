#!/usr/bin/env python3
"""Turn the site's optional features on, one command each.

Three switches live in two files. Rather than hunting for them, use this:

    python3 configure.py status                      # what's on, what's off
    python3 configure.py chat https://x.workers.dev  # live chat + JD fit check
    python3 configure.py analytics dylanram          # GoatCounter site code
    python3 configure.py domain dylanram.com         # custom domain

Each writes the value, rebuilds the site, and tells you what changed. Pass
"off" as the value to switch something back off.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# switch -> (file, constant, what it turns on, what to do after)
SWITCHES = {
    "chat": (
        "site_qa.py", "CHAT_ENDPOINT",
        "live chat + JD fit check",
        "commit and push — the site goes live with it",
    ),
    "analytics": (
        "build_site.py", "ANALYTICS_ID",
        "visitor counts (GoatCounter — no cookies, no banner)",
        "commit and push, then watch goatcounter.com for clicks",
    ),
    "domain": (
        "build_site.py", "DOMAIN",
        "custom domain (writes docs/CNAME)",
        "commit and push, then finish the DNS steps in DOMAIN-SETUP.md",
    ),
}


def read(name):
    path, const, _, _ = SWITCHES[name]
    text = (ROOT / path).read_text()
    m = re.search(rf'^{const} = "(.*)"$', text, re.M)
    return m.group(1) if m else None


def write(name, value):
    path, const, _, _ = SWITCHES[name]
    f = ROOT / path
    text = f.read_text()
    new, n = re.subn(rf'^{const} = ".*"$', f'{const} = "{value}"', text, count=1, flags=re.M)
    if not n:
        sys.exit(f"couldn't find {const} in {path} — set it by hand")
    f.write_text(new)


def status():
    print()
    for name, (_, _, does, _) in SWITCHES.items():
        value = read(name)
        state = f"\033[32mon\033[0m  {value}" if value else "\033[90moff\033[0m"
        print(f"  {name:<10} {state}")
        if not value:
            print(f"  {'':<10} \033[90m{does}\033[0m")
    print(f"\n  turn one on:  python3 configure.py <switch> <value>\n")


def main(argv):
    if len(argv) < 2 or argv[1] == "status":
        return status()
    name = argv[1]
    if name not in SWITCHES:
        sys.exit(f"unknown switch {name!r} — try: {', '.join(SWITCHES)}, or status")
    if len(argv) < 3:
        sys.exit(f"usage: python3 configure.py {name} <value|off>")

    value = "" if argv[2] == "off" else argv[2].strip().rstrip("/")
    # a pasted domain often arrives with a scheme; the constant wants bare host
    if name == "domain":
        value = re.sub(r"^https?://", "", value)
    write(name, value)

    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)

    _, _, does, next_step = SWITCHES[name]
    if value:
        print(f"\n  \033[32m✓\033[0m {does} — on ({value})")
        print(f"    next: {next_step}\n")
    else:
        print(f"\n  {does} — off\n")


if __name__ == "__main__":
    main(sys.argv)
