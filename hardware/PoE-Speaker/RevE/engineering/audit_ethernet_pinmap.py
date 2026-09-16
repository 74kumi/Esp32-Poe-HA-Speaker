"""Check sourced MDI pin assignments against model, PCB and a fresh netlist.

Run with KiCad's Python; pass --kicad-cli if it is not on PATH.
This checks logical assignments, not routed continuity or electrical performance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "KiCad-RevE"
EXPECTED = {
    "U3": {"1": "ETH_TX_N", "2": "ETH_TX_P", "5": "ETH_RX_N", "6": "ETH_RX_P"},
    "J1": {"10": "ETH_TX_N", "11": "ETH_TX_P", "5": "ETH_RX_N", "4": "ETH_RX_P",
           "12": "ETH_TX_CT", "6": "ETH_RX_CT", "13": "POE_MODE_A_AC1",
           "14": "POE_MODE_A_AC2", "15": "POE_MODE_B_AC1", "16": "POE_MODE_B_AC2"},
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kicad-cli", default="kicad-cli")
    args = parser.parse_args()
    board_path = DESIGN / "PoE-Speaker-RevE.kicad_pcb"
    model_path = ROOT / "engineering/revision-e-design.json"
    board = pcbnew.LoadBoard(str(board_path))
    pcb = {(f.GetReference(), p.GetNumber()): p.GetNetname()
           for f in board.GetFootprints() for p in f.Pads()}
    model = json.loads(model_path.read_text(encoding="utf-8"))["components"]
    with tempfile.TemporaryDirectory(prefix="speaker-pinmap-") as tmp:
        netlist = Path(tmp) / "netlist.xml"
        subprocess.run([args.kicad_cli, "sch", "export", "netlist", "--format", "kicadxml",
                        "-o", str(netlist), str(DESIGN / "PoE-Speaker-RevE.kicad_sch")],
                       check=True, capture_output=True, text=True)
        schematic = {(node.attrib["ref"], node.attrib["pin"]): net.attrib["name"]
                     for net in ET.parse(netlist).findall("./nets/net") for node in net.findall("node")}
    rows = []
    for ref, pins in EXPECTED.items():
        model_pins = {p["number"]: p["net"] for p in model[ref]["pins"]}
        for pin, expected in pins.items():
            actual = {"pcb": pcb.get((ref, pin)), "schematic": schematic.get((ref, pin)),
                      "model": model_pins.get(pin)}
            rows.append({"reference": ref, "pin": pin, "expected": expected,
                         **actual, "pass": all(net == expected for net in actual.values())})
    sources = [board_path, model_path, *sorted(DESIGN.glob("*.kicad_sch"))]
    report = {
        "method": "Expected pin nets from manufacturer pinouts; fresh schematic netlist compared with PCB and design model. No physical validation.",
        "references": ["https://docs.wiznet.io/img/products/w5500/W5500_ds_v110e.pdf#page=8",
                       "https://www.belfuse.com/media/drawings/products/magjack%20ICMs/dr-mag-2250506.pdf#page=2"],
        "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        "pass": all(row["pass"] for row in rows), "pins": rows,
    }
    (DESIGN / "reports/ethernet-pinmap-review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Ethernet pin map: {sum(row['pass'] for row in rows)}/{len(rows)} passed")
    raise SystemExit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
