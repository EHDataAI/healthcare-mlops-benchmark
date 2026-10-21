"""Fail-closed, stdlib-only QA for the public WDBC static report site.

No scientific inputs are downloaded, regenerated, or executed by this check.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "WDBC_ERLV2_Research_Report_v0_1_1.ipynb"
REPORT_PATH = ROOT / "preview/WDBC_ERLV2_Research_Report_v0_1_1.html"
INDEX_PATH = ROOT / "docs/index.html"
PAGES_REPORT_PATH = ROOT / "docs/wdbc-report.html"
README_PATH = ROOT / "README.md"
GITATTRIBUTES_PATH = ROOT / ".gitattributes"
COVER_IMAGES = {
    "assets/wdbc_brier_benchmark.png": 0,
    "assets/wdbc_brier_calibration.png": 1,
}

# Frozen public Git blob hashes on main before static-site publication.
EXPECTED_NOTEBOOK_BLOB = "f595fd5a2d7a1ca084969479182fd1ddf921a130"
EXPECTED_REPORT_BLOB = "a7df0675aed110aee9eb8c6f7688acce15a7bbae"

BAD_TAGS = {"script", "iframe", "frame", "object", "embed", "form", "input"}
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    re.compile(r"[A-Za-z]:[/\\]Users[/\\]", re.IGNORECASE),
    re.compile(r"/home/[^/\s]+/"),
)


def git_blob_sha(data: bytes) -> str:
    """Compute the canonical Git blob SHA-1 without shelling out to Git."""
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 (Git blob format)


class StaticAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.png_images = 0
        self.embedded_pngs: list[bytes] = []
        self.local_pngs: list[str] = []
        self.h1_count = 0
        self.headings: list[str] = []
        self.has_html_lang = False
        self.has_title = False
        self.links: list[str] = []
        self.has_viewport = False
        self.has_csp = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1":
            self.h1_count += 1
        if tag in BAD_TAGS:
            raise ValueError(f"Disallowed active HTML element: {tag}")
        d = dict(attrs)
        if any(k.lower().startswith("on") for k in d):
            raise ValueError(f"Inline browser event handler detected on {tag}")
        for k, value in attrs:
            if value and value.lower().strip().startswith("javascript:"):
                raise ValueError(f"JavaScript URL or attribute in {tag}.{k}")
        if tag == "html" and d.get("lang") == "es":
            self.has_html_lang = True
        if tag == "title":
            self.has_title = True
        if tag == "meta":
            self.has_viewport |= d.get("name") == "viewport"
            self.has_csp |= d.get("http-equiv", "").lower() == "content-security-policy"
        if tag == "a":
            href = d.get("href", "")
            if not href:
                raise ValueError("Empty link")
            self.links.append(href)
        if tag == "link" and d.get("rel") in {"stylesheet", "preload", "modulepreload"}:
            raise ValueError("External stylesheet or preload not permitted")
        if tag == "img":
            if not d.get("alt", "").strip():
                raise ValueError("PNG figure missing descriptive alt text")
            payload = d.get("src", "")
            prefix = "data:image/png;base64,"
            if payload in COVER_IMAGES:
                self.local_pngs.append(payload)
            elif payload.startswith(prefix):
                try:
                    image = base64.b64decode(payload[len(prefix) :], validate=True)
                except (ValueError, base64.binascii.Error) as exc:
                    raise ValueError("Invalid embedded PNG base64") from exc
                if not image.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise ValueError("Invalid embedded PNG signature")
                self.embedded_pngs.append(image)
                self.png_images += 1
            else:
                raise ValueError("Image source is not an approved local or embedded PNG")


def ensure_safe_text(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    if "@import" in content.lower():
        raise ValueError(f"Unexpected CSS import in {path.name}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            raise ValueError(f"Sensitive-path or token pattern in {path.name}")
    return content


def run() -> None:
    notebook_bytes = NOTEBOOK_PATH.read_bytes()
    report_bytes = REPORT_PATH.read_bytes()
    pages_report_bytes = PAGES_REPORT_PATH.read_bytes()
    if git_blob_sha(notebook_bytes) != EXPECTED_NOTEBOOK_BLOB:
        raise ValueError("The scientific notebook differs from its approved frozen Git blob")
    if git_blob_sha(report_bytes) != EXPECTED_REPORT_BLOB:
        raise ValueError("The HTML report differs from its approved frozen Git blob")
    if pages_report_bytes != report_bytes:
        raise ValueError("Pages copy differs byte-for-byte from the frozen HTML")

    notebook = json.loads(notebook_bytes.decode("utf-8"))
    cells = notebook["cells"]
    code_cells = [c for c in cells if c["cell_type"] == "code"]
    if len(cells) != 21 or len(code_cells) != 11:
        raise ValueError("Unexpected notebook cell structure")
    if any(c.get("execution_count") is not None or c.get("outputs") for c in code_cells):
        raise ValueError("Research notebook must remain source-only")
    if notebook.get("metadata", {}).get("erl", {}).get("execution_mode") != "read_only":
        raise ValueError("Notebook read-only contract missing")

    report = ensure_safe_text(REPORT_PATH)
    home = ensure_safe_text(INDEX_PATH)
    readme = README_PATH.read_text(encoding="utf-8")
    for name, text in (("report", report), ("index", home)):
        if re.search(r"<\s*/?\s*script\b|\bjavascript:\s*|\burl\(\s*['\"]?https?://", text, re.I):
            raise ValueError(f"Active or externally fetched content in {name}")

    report_parser = StaticAudit()
    report_parser.feed(report)
    report_parser.close()
    if report_parser.png_images != 5 or not report_parser.has_html_lang:
        raise ValueError("Report must contain the original five accessible PNG figures")
    if report_parser.local_pngs:
        raise ValueError("Frozen report unexpectedly references separate image files")
    if any(not anchor.startswith("#") for anchor in report_parser.links):
        raise ValueError("Unexpected external navigation inside frozen report")

    index_parser = StaticAudit()
    index_parser.feed(home)
    index_parser.close()
    if not (index_parser.has_html_lang and index_parser.has_viewport and index_parser.has_csp):
        raise ValueError("Landing page missing language, viewport or security policy")
    if index_parser.h1_count != 1:
        raise ValueError("Landing page must contain exactly one primary heading")
    if index_parser.png_images or index_parser.local_pngs != list(COVER_IMAGES):
        raise ValueError("Landing page references unexpected or duplicated scientific figures")
    for relative, report_index in COVER_IMAGES.items():
        png_bytes = (ROOT / "docs" / relative).read_bytes()
        if png_bytes != report_parser.embedded_pngs[report_index]:
            raise ValueError(f"Cover figure differs from frozen report evidence: {relative}")
    rules = GITATTRIBUTES_PATH.read_text(encoding="utf-8")
    for required in ("*.ipynb text eol=lf", "*.html text eol=lf",
                     "*.py text eol=lf", "*.yml text eol=lf"):
        if required not in rules:
            raise ValueError(f"Missing LF checkout protection: {required}")
    required = "wdbc-report.html"
    if required not in index_parser.links or "docs/wdbc-report.html" not in readme:
        raise ValueError("Static report not linked from both index and README")
    if "No es una herramienta" not in home or "source-only" not in home:
        raise ValueError("Landing page lacks clinical/reproducibility cautions")

    print("PASS: Frozen notebook (source-only; 21 cells, 11 code cells)")
    print("PASS: Frozen static HTML, with byte-identical /docs report (5 verified PNG figures)")
    print("PASS: No active scripts, external HTML resources or common secret patterns")
    print("PASS: Two scientific cover PNGs byte-identical to frozen HTML")
    print("PASS: LF-safe checkout rules for Windows and Linux")
    print("PASS: Static landing page links, language, accessibility and safeguards")
    print("WDBC_STATIC_REPORT_QA=PASS")


if __name__ == "__main__":
    run()
