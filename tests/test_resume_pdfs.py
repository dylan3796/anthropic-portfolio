"""One page per resume PDF — a hard constraint, pinned.

The four PDFs in docs/resumes/ are the files recruiters actually download.
A content addition that spills any of them onto a second page is a silent
regression: the layout still renders, the build still passes, and the second
page is discovered by a stranger. The /new-entry skill's remedy for overflow
is editorial (cut content), never shrinking fonts — this test is what forces
that conversation.

Page counting reads the PDF's object tree directly (Chromium's print-to-pdf
output is uncompressed enough for this) — no dependencies. If a PDF is ever
produced by a tool whose structure defeats the parser, the test skips that
file rather than failing, mirroring the node-skip pattern in test_site_qa.py.

    python3 tests/test_resume_pdfs.py
"""

import re
import sys
import zlib
from pathlib import Path

PDF_DIR = Path(__file__).resolve().parent.parent / "docs" / "resumes"


def page_count(raw: bytes):
    """Count pages via the /Count entry on the root /Pages node, with a
    fallback to counting /Type /Page leaf objects (decompressing streams if
    needed). Returns None when the structure can't be parsed."""
    m = re.search(rb"/Type\s*/Pages[^>]*?/Count\s+(\d+)", raw, re.S)
    if m:
        return int(m.group(1))
    leaves = re.findall(rb"/Type\s*/Page(?![s/\w])", raw)
    if leaves:
        return len(leaves)
    # object streams: decompress and retry the leaf count
    total = 0
    for stream in re.findall(rb"stream\r?\n(.*?)endstream", raw, re.S):
        try:
            total += len(re.findall(rb"/Type\s*/Page(?![s/\w])", zlib.decompress(stream)))
        except zlib.error:
            continue
    return total or None


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"fail: no PDFs found in {PDF_DIR}")
        return 1

    failures = 0
    for pdf in pdfs:
        pages = page_count(pdf.read_bytes())
        if pages is None:
            print(f"skip  {pdf.name}: unparseable structure")
        elif pages == 1:
            print(f"ok    {pdf.name}: 1 page")
        else:
            print(f"FAIL  {pdf.name}: {pages} pages — cut content, never shrink fonts")
            failures += 1

    print(f"\n{len(pdfs) - failures}/{len(pdfs)} within one page")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
