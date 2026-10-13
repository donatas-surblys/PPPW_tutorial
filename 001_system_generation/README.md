# System generation

This folder demonstrates how to generate the simulation systems. As in the
conventional phantom-wall method, a well equilibrated system is needed for
every PW position to reliably sample the pressure on the PW.

`data/data.relaxed_eta0.2` is the starting system, already equilibrated at
85 K and 1 MPa without the PW. It contains the Pt substrate (type 1, atoms
connected by harmonic bonds, bottom layer fixed), the Ar fluid (type 2, 2000
atoms) and a virtual particle (type 3) that carries the upper wall working as
a piston to control the pressure. See the paper for the potential parameters.

The LAMMPS input scripts are in the `scripts` directory:

| Script | Stage |
|---|---|
| `in.PW_SL_make` | make stage (this folder) |
| `in.PW_SL_compute` | compute stage (production runs, [`../002_production_runs`](../002_production_runs)) |

Both share the same system settings and differ only in the stage-specific
part at the end of the file.

`runme.bash` runs the make stage with `in.PW_SL_make` in the `generated`
directory. The LAMMPS command is assumed to be `mpirun -np 8 lmp`; set the
`LMP` environment variable to change it, e.g.

```bash
LMP="mpirun -np 56 lmp_mpi" bash runme.bash
```

**LAMMPS requirements:** the MOLECULE, EXTRA-PAIR and TALLY packages, and the
PYTHON package for drawing random seeds. Without the PYTHON package, replace
the `python ... random_integer` lines in both input scripts with

```
variable random_integer equal round(random(1,900000000,12345))
```

## The make stage

The PW is inserted at z = 13.0 Å, where it does not interact with the fluid
yet, and moved upwards in 0.1 Å steps up to z = 30.0 Å (171 positions),
holding each position for 1 ns. The configuration at every position is
written to `data.eta0.2_per20_<pos>`, which is the starting point of the
production runs in [`../002_production_runs`](../002_production_runs).

## Some details about the partially permeable phantom-wall

The PW is created with `fix wall/lj93` (`fix pwall`), with its cut-off at the
potential minimum so that it is purely repulsive. It interacts only with the
group `fluid_int`, which consists of the first (100 − per) % of the fluid atom
IDs. The other per % of the Ar atoms do not feel the PW and can pass through
it. With `per = 0`, the conventional (impermeable) PW method is recovered.

The force on the PW is output as a pressure in Pa, `v_press_pwall` (negative,
the sign of the force acting on the wall), and the piston position as
`v_z_virtual`. These two quantities are all that is needed for the work of
adhesion; the other thermo outputs are extra information.
