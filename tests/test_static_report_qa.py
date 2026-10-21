"""Regression tests for static WDBC publication boundaries (no external dependencies)."""

from __future__ import annotations

import unittest

from scripts.verify_static_report import (
    COVER_IMAGES,
    INDEX_PATH,
    NOTEBOOK_PATH,
    PAGES_REPORT_PATH,
    REPORT_PATH,
    StaticAudit,
    git_blob_sha,
    EXPECTED_NOTEBOOK_BLOB,
    EXPECTED_REPORT_BLOB,
)


class TestStaticAudit(unittest.TestCase):
    def parse(self, html: str) -> StaticAudit:
        parser = StaticAudit()
        parser.feed(html)
        parser.close()
        return parser

    def test_reject_script_elements(self) -> None:
        with self.assertRaisesRegex(ValueError, "active HTML"):
            self.parse("<html lang='es'><script>alert(1)</script></html>")

    def test_reject_inline_event_handlers(self) -> None:
        with self.assertRaisesRegex(ValueError, "event handler"):
            self.parse("<main onload='anything()'></main>")

    def test_reject_script_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "JavaScript"):
            self.parse("<a href='javascript:alert(1)'>Unsafe</a>")

    def test_reject_external_images(self) -> None:
        with self.assertRaisesRegex(ValueError, "approved local or embedded"):
            self.parse("<img src='https://example.org/chart.png' alt='Chart'>")

    def test_reject_arbitrary_local_images(self) -> None:
        with self.assertRaisesRegex(ValueError, "approved local or embedded"):
            self.parse("<img src='assets/other.png' alt='Chart'>")

    def test_reject_missing_alt(self) -> None:
        with self.assertRaisesRegex(ValueError, "alt text"):
            self.parse("<img src='assets/wdbc_brier_benchmark.png'>")

    def test_frozen_notebook_git_blob(self) -> None:
        self.assertEqual(git_blob_sha(NOTEBOOK_PATH.read_bytes()), EXPECTED_NOTEBOOK_BLOB)

    def test_frozen_report_git_blob(self) -> None:
        self.assertEqual(git_blob_sha(REPORT_PATH.read_bytes()), EXPECTED_REPORT_BLOB)
        self.assertEqual(REPORT_PATH.read_bytes(), PAGES_REPORT_PATH.read_bytes())

    def test_checkout_line_endings_not_converted(self) -> None:
        for path in (NOTEBOOK_PATH, REPORT_PATH, PAGES_REPORT_PATH):
            with self.subTest(path=path.name):
                self.assertNotIn(b"\r\n", path.read_bytes())

    def test_landing_links_and_images(self) -> None:
        parser = self.parse(INDEX_PATH.read_text(encoding="utf-8"))
        self.assertEqual(parser.h1_count, 1)
        self.assertEqual(parser.local_pngs, list(COVER_IMAGES))
        self.assertIn("wdbc-report.html", parser.links)


if __name__ == "__main__":
    unittest.main()
