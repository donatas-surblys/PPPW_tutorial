#!/usr/bin/env bash
# usage: bash runme.bash [log directory (default: ../002_production_runs/sample_data)]

set -euo pipefail

LOGDIR="${1:-../002_production_runs/sample_data}"

python3 scripts/calc_work_of_adhesion.py "${LOGDIR}" | tee work_of_adhesion.txt
