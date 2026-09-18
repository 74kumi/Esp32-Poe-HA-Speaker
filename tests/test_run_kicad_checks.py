import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "run-kicad-checks.sh"
CANONICAL_DIR = REPO_ROOT / "hardware" / "PoE-Speaker" / "RevE" / "KiCad-RevE"


class RunKiCadChecksTests(unittest.TestCase):
    def make_fake_cli(self, directory: Path) -> Path:
        fake = directory / "fake-kicad-cli"
        fake.write_text(
            textwrap.dedent(
                f"""\
                #!{sys.executable}
                import json
                import os
                from pathlib import Path
                import sys

                args = sys.argv[1:]
                with open(os.environ["FAKE_KICAD_LOG"], "a", encoding="utf-8") as log:
                    log.write(json.dumps(args) + "\\n")

                if args[:2] == ["sch", "erc"]:
                    exit_code = int(os.environ.get("FAKE_ERC_EXIT", "0"))
                    if exit_code:
                        raise SystemExit(exit_code)

                output = Path(args[args.index("-o") + 1])
                output.write_text("fake report\\n", encoding="utf-8")
                """
            ),
            encoding="utf-8",
        )
        fake.chmod(0o755)
        return fake

    def run_wrapper(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_missing_output_directory_exits_two_and_prints_usage(self) -> None:
        result = self.run_wrapper()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage", result.stdout + result.stderr)

    def test_success_runs_erc_then_drc_and_writes_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            output = temp / "reports"
            log = temp / "calls.jsonl"
            fake = self.make_fake_cli(temp)
            env = os.environ | {"KICAD_CLI": str(fake), "FAKE_KICAD_LOG": str(log)}

            result = self.run_wrapper(str(output), env=env)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([call[:2] for call in calls], [["sch", "erc"], ["pcb", "drc"]])
            self.assertTrue(all("--exit-code-violations" in call for call in calls))
            self.assertEqual(calls[0][calls[0].index("-o") + 1], str(output / "erc.rpt"))
            self.assertEqual(calls[1][calls[1].index("-o") + 1], str(output / "drc.rpt"))
            self.assertEqual(Path(calls[0][-1]), CANONICAL_DIR / "PoE-Speaker-RevE.kicad_sch")
            self.assertEqual(Path(calls[1][-1]), CANONICAL_DIR / "PoE-Speaker-RevE.kicad_pcb")
            self.assertTrue((output / "erc.rpt").is_file())
            self.assertTrue((output / "drc.rpt").is_file())

    def test_erc_failure_is_propagated_and_prevents_drc(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            output = temp / "reports"
            log = temp / "calls.jsonl"
            fake = self.make_fake_cli(temp)
            env = os.environ | {
                "KICAD_CLI": str(fake),
                "FAKE_KICAD_LOG": str(log),
                "FAKE_ERC_EXIT": "7",
            }

            result = self.run_wrapper(str(output), env=env)

            self.assertEqual(result.returncode, 7)
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][:2], ["sch", "erc"])
            self.assertFalse((output / "drc.rpt").exists())


if __name__ == "__main__":
    unittest.main()
