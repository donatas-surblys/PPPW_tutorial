#!/usr/bin/env bash
# make stage (see README.md)
# usage: LMP="mpirun -np 56 lmp_mpi" bash runme.bash

set -euo pipefail

LMP="${LMP:-mpirun -np 8 lmp}"

ETA=0.2   # solid-liquid interaction scaling factor
PER=20    # permeability of the phantom wall [%]

mkdir -p generated
cp scripts/in.PW_SL_make data/data.relaxed_eta${ETA} generated/
cd generated

# phantom-wall sweep -> data.eta0.2_per20_13.0 ... data.eta0.2_per20_30.0
${LMP} -log log.eta${ETA}_per${PER} -v eta ${ETA} -v per ${PER} \
  -v pos_pwall 13.0 -v dpos 0.1 -v npos 171 -in in.PW_SL_make
