from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MarkupProbe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.classes = []
        self.score_cells = 0
        self._inside_score_link = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = values.get("class", "").split()
        self.tags.append(tag)
        self.classes.extend(classes)
        if tag == "a" and "score" in self.classes[-len(classes) :]:
            self._inside_score_link = True


class ExceptionConsoleContract(unittest.TestCase):
    def test_template_is_read_only_and_uses_stable_handoff(self):
        source = (ROOT / "template.html").read_text()
        parser = MarkupProbe()
        parser.feed(source)

        self.assertIn("NW-HANDOFF-V1", source)
        self.assertIn("{{SYSTEM_EXCEPTION_OR_EMPTY}}", source)
        self.assertIn("{{AUTOMATIC_AUDIT}}", source)
        self.assertNotIn("<select", source)
        self.assertNotIn("<textarea", source)
        self.assertNotIn('type="checkbox"', source)
        self.assertNotIn("Copy selected handoff", source)
        self.assertEqual(source.count('<span class="k">'), 3)

    def test_published_page_is_exception_console_not_worksheet(self):
        source = (ROOT / "index.html").read_text()
        parser = MarkupProbe()
        parser.feed(source)

        self.assertFalse(re.search(r"\{\{.+?\}\}", source))
        self.assertIn("Concierge handoff incomplete", source)
        self.assertIn("Exception console activated", source)
        self.assertEqual(source.count('<span class="n">—</span>'), 3)
        self.assertNotIn("Waiting on you", source)
        self.assertNotIn("worksheet status", source)
        self.assertNotIn("<select", source)
        self.assertNotIn("<textarea", source)
        self.assertEqual(source.count('<span class="k">'), 3)

    def test_count_formula_and_residual_protocol_are_unambiguous(self):
        design = (ROOT / "DESIGN.md").read_text()
        handoff = (ROOT / "HANDOFF.md").read_text()

        self.assertIn("`Handled automatically` = marker `completed + parked`", design)
        self.assertIn("must equal marker `needs_ops`", design)
        self.assertIn("RESIDUAL class=", design)
        self.assertIn("JOB 34's classification is canonical", handoff)

    def test_july_26_fixture_contains_all_thirteen_findings(self):
        acceptance = (ROOT / "ACCEPTANCE.md").read_text()
        rows = [
            line
            for line in acceptance.splitlines()
            if line.startswith("| ") and not line.startswith("| Finding") and not line.startswith("|---")
        ]

        self.assertEqual(len(rows), 13)
        for expected in (
            "sensor bypass",
            "billing-reference message",
            "moved 509A booking",
            "901 booking",
            "cooling setpoint",
            "artist follow-up",
            "Coverage",
            "staff-name calendar block",
            "Alarm credential",
            "screenshot/drop",
            "509B booking",
            "Temporary access",
            "heat complaint",
        ):
            self.assertTrue(any(expected in row for row in rows), expected)


if __name__ == "__main__":
    unittest.main()
