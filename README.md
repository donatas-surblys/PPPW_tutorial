# Partially permeable phantom-wall (PPPW) method: LAMMPS tutorial

This repository contains a terse tutorial on how to apply the partially
permeable phantom-wall (PPPW) method with LAMMPS to obtain the work of
solid-liquid adhesion. It reproduces one case of our paper: the Pt-Ar
solid-liquid system with a solid-fluid interaction parameter η = 0.2 and a
20 % permeable phantom wall (PW), sampled along the upward path (the PW is
moved away from the solid).

## Basic information about the method

The phantom-wall method is described in the following papers:

- Frédéric Leroy, Daniel J. V. A. dos Santos, and Florian Müller-Plathe,
  *Macromol. Rapid Commun.* **30**, 864–870 (2009).
  <https://doi.org/10.1002/marc.200800746>
- Frédéric Leroy and Florian Müller-Plathe, *J. Chem. Phys.* **133**, 044110 (2010).
  <https://doi.org/10.1063/1.3458796>

In the phantom-wall (PW) method, a purely repulsive virtual wall that
interacts only with the fluid is moved slowly away from the solid, reversibly
separating the liquid from the surface. The work of adhesion is obtained by
integrating the pressure exerted on the PW over its displacement and
subtracting the work done against the system pressure.

## Difference from the conventional phantom-wall

A conventional PW is impermeable: it interacts with all fluid molecules and
pushes every one of them away from the surface. The separated solid is
therefore left bare, without the vapor and the adsorbed or confined liquid
that exist in reality, and the result is the work of adhesion in a vacuum
environment. To obtain the physically meaningful work of adhesion under
saturated vapor (the one in the Young-Dupré equation), an auxiliary
solid-vapor calculation is needed. For structured interfaces, such as a
self-assembled monolayer (SAM) into which water penetrates, the conventional
PW also strips the liquid out of the interfacial structure, which must then
be re-equilibrated at a high computational cost.

The partially permeable PW interacts with only a prescribed fraction of the
fluid molecules. The rest (the "permeability", 20 % here) do not feel the PW,
pass through it freely and remain at the surface. During the separation they
form a vapor phase and an adsorption layer between the PW and the solid, so
the separated state resembles the physical solid-vapor state. The same
thermodynamic integration as in the conventional PW method is used. In the
LAMMPS input, the only change is the group the PW acts on; with a
permeability of 0 %, the conventional PW method is recovered.

## What the method can do

- Obtain a work of adhesion that includes the effect of the vapor and the
  adsorption layer from a single separation calculation. Unless the
  adsorption layer is exceptionally dense, this approximates the
  saturated-vapor value without the auxiliary solid-vapor calculation
  needed with the conventional PW.
- Separate the bulk liquid from structurally complex interfaces (e.g. a
  hydrated SAM) while preserving the interfacial liquid structure, avoiding
  the slow re-equilibration that follows its disruption.

Two limitations should be kept in mind. If the permeability is too high, a
liquid layer made only of permeating molecules can stay on the surface; the
permeability should be screened in advance (an entropy-of-mixing criterion
is given in the paper). The separation path must also be reversible, which
should be checked by comparing upward and downward PW sweeps, since
hysteresis can appear for strongly attractive or structured interfaces.
Details are given in the paper.

## Folder structure

The folder numbering indicates the order in which they should be looked at.
In each folder there is a `README.md` file with general information and a
`runme.bash` script that demonstrates how to execute the scripts.

| Folder | Contents |
|---|---|
| [`001_system_generation`](001_system_generation) | The LAMMPS inputs for the make and compute stages (`scripts/in.PW_SL_make`, `scripts/in.PW_SL_compute`), the relaxed initial system, and the PW sweep that generates one configuration per PW position. |
| [`002_production_runs`](002_production_runs) | 20 ns sampling at each PW position; `sample_data` holds log files of the runs used in the paper. |
| [`003_post_processing`](003_post_processing) | Calculation of the work of adhesion from the logs. |
