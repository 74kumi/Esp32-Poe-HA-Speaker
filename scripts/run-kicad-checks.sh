#!/bin/sh
set -eu

usage() {
    echo "Usage: $0 OUTPUT_DIRECTORY" >&2
    exit 2
}

[ "$#" -eq 1 ] || usage

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
OUTPUT_DIR=$1
KICAD_CLI=${KICAD_CLI:-kicad-cli}
CANONICAL_DIR="$REPO_ROOT/hardware/PoE-Speaker/RevE/KiCad-RevE"
SCHEMATIC="$CANONICAL_DIR/PoE-Speaker-RevE.kicad_sch"
BOARD="$CANONICAL_DIR/PoE-Speaker-RevE.kicad_pcb"

[ -f "$SCHEMATIC" ] || {
    echo "Schematic not found: $SCHEMATIC" >&2
    exit 1
}
[ -f "$BOARD" ] || {
    echo "PCB not found: $BOARD" >&2
    exit 1
}

mkdir -p -- "$OUTPUT_DIR"

"$KICAD_CLI" sch erc \
    --exit-code-violations \
    -o "$OUTPUT_DIR/erc.rpt" \
    "$SCHEMATIC"

"$KICAD_CLI" pcb drc \
    --exit-code-violations \
    -o "$OUTPUT_DIR/drc.rpt" \
    "$BOARD"

printf '%s\n' 'Caution: clean ERC/DRC does not constitute fabrication approval.' >&2
