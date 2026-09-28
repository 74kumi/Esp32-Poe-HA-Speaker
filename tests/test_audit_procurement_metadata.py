import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_procurement_metadata.py"
CURRENT_REPORT = (
    ROOT
    / "hardware"
    / "PoE-Speaker"
    / "RevE"
    / "KiCad-RevE"
    / "reports"
    / "procurement-audit.json"
)
CURRENT_REPORT_SHA256 = "3dfe9d548ee20e9049ff3472cc6474819a961201d37c41526692fc432c798af5"


class AuditProcurementMetadataTests(unittest.TestCase):
    def run_audit(self, report, *args):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "procurement.json"
            report_path.write_text(json.dumps(report), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), *args, str(report_path)],
                text=True,
                capture_output=True,
                cwd=ROOT,
            )
            return result, report_path.read_bytes()

    def test_complete_purchase_metadata_passes_strict_mode(self):
        report = {
            "components": [
                {
                    "reference": "R1",
                    "manufacturer": "Example Corp",
                    "mpn": "EX-100",
                    "status": "Candidate; qualification remains",
                    "properties": {"Datasheet": "https://example.invalid/ex-100.pdf"},
                },
                {
                    "reference": "TP1",
                    "manufacturer": "",
                    "mpn": "",
                    "status": "No purchase required",
                    "properties": {},
                },
            ]
        }

        result, source_bytes = self.run_audit(report, "--strict")

        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["status"], "complete")
        self.assertEqual(summary["purchase_required_components"], 1)
        self.assertEqual(summary["no_purchase_required_components"], 1)
        self.assertEqual(summary["source_sha256"], hashlib.sha256(source_bytes).hexdigest())
        self.assertEqual(summary["gaps"], {})

    def test_strict_mode_fails_and_lists_missing_fields(self):
        report = {
            "components": [
                {
                    "reference": "C1",
                    "manufacturer": "",
                    "mpn": "",
                    "status": "Candidate; checks remain",
                    "properties": {"Datasheet URL": {"url": "", "text": ""}},
                },
                {
                    "reference": "TP1",
                    "manufacturer": "",
                    "mpn": "",
                    "status": "No purchase required",
                    "properties": {},
                },
            ]
        }

        result, _ = self.run_audit(report, "--strict")

        self.assertEqual(result.returncode, 1)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["status"], "incomplete")
        self.assertEqual(summary["gaps"]["missing_manufacturer"], ["C1"])
        self.assertEqual(summary["gaps"]["missing_mpn"], ["C1"])
        self.assertEqual(summary["gaps"]["missing_datasheet"], ["C1"])

    def test_malformed_report_exits_two(self):
        result, _ = self.run_audit({"components": {}}, "--strict")

        self.assertEqual(result.returncode, 2)
        self.assertIn("components must be a list", result.stderr)

    def test_current_report_is_fingerprinted_and_reports_known_gaps(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(CURRENT_REPORT)],
            text=True,
            capture_output=True,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["status"], "incomplete")
        self.assertEqual(summary["total_components"], 209)
        self.assertEqual(summary["purchase_required_components"], 179)
        self.assertEqual(summary["no_purchase_required_components"], 30)
        self.assertEqual(len(summary["gaps"]["missing_manufacturer"]), 18)
        self.assertEqual(len(summary["gaps"].get("missing_mpn", [])), 0)
        self.assertEqual(len(summary["gaps"]["missing_datasheet"]), 19)
        self.assertEqual(summary["source_sha256"], CURRENT_REPORT_SHA256)


if __name__ == "__main__":
    unittest.main()
