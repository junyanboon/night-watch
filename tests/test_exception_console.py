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

        # Contract invariants, not the text of any one published morning. An
        # assertion naming a specific day's copy goes red the next time the page
        # publishes real data, which is every day.
        self.assertFalse(re.search(r"\{\{.+?\}\}", source))
        self.assertEqual(source.count('<span class="k">'), 3)
        self.assertEqual(source.count('<span class="tk">'), 5)
        self.assertIn('class="truth"', source)
        # Either a verdict for the Ops Lead or an honest statement that none can
        # be given — never neither.
        self.assertTrue(
            'class="clear-card"' in source
            or 'class="system-card"' in source
            or 'class="row"' in source
        )
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

    def test_truth_band_and_queue_are_direct_reads(self):
        template = (ROOT / "template.html").read_text()
        design = (ROOT / "DESIGN.md").read_text()
        handoff = (ROOT / "HANDOFF.md").read_text()

        # The band and queue exist in the template.
        self.assertIn('class="truth"', template)
        self.assertIn("{{TRUTH_GAP_OR_EMPTY}}", template)
        self.assertIn("{{QUEUE_ROWS_OR_EMPTY}}", template)
        self.assertIn('id="queue"', template)

        # Five direct-read cells, and the score band still has exactly three.
        self.assertEqual(template.count('<span class="tk">'), 5)
        self.assertEqual(template.count('<span class="k">'), 3)

        # They are gauges, not a promotion of work to the Ops Lead.
        self.assertIn("gauge, never a task list", design)
        self.assertIn("pointers to work, not authority to act", design)

        # The publisher reads the data sources itself, not via the marker.
        for collection in (
            "collection://047caea0-3da0-4434-a924-319efa8237cb",
            "collection://b4bd4ed7-0ae8-44bb-aed0-adf78b7848b0",
            "collection://20df225d-382f-4bb8-9c15-c31571c9f4e0",
        ):
            self.assertIn(collection, handoff)

        # A failed handshake must not suppress them — that is when they matter most.
        self.assertIn("even when the handshake failed", handoff)

    def test_retired_runs_are_not_findings(self):
        handoff = (ROOT / "HANDOFF.md").read_text()

        self.assertIn("Retired runs are not findings", handoff)
        self.assertIn("Morning Shift", handoff)

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
