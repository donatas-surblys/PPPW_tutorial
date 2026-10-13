#!/usr/bin/env bash
# compute stage at every PW position written by the make stage (see README.md)
# usage: LMP="mpirun -np 56 lmp_mpi" bash runme.bash

set -euo pipefail

LMP="${LMP:-mpirun -np 8 lmp}"

ETA=0.2
PER=20
# data files written by the make stage (absolute path)
GEN="$(cd ../001_system_generation/generated && pwd)"

mkdir -p runs
cp ../001_system_generation/scripts/in.PW_SL_compute runs/
cd runs

# PW positions are taken from the data file names: data.eta0.2_per20_<pos>
for data in "${GEN}"/data.eta${ETA}_per${PER}_*
do
  z="${data##*_}"
  cp "${data}" .
  echo "PW position ${z} A -> runs/log.20ns_${z}"
  ${LMP} -log log.20ns_${z} -v eta ${ETA} -v per ${PER} \
    -v pos_pwall ${z} -in in.PW_SL_compute
done
