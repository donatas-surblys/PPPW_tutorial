# Sampling the systems

The systems generated in [`../001_system_generation`](../001_system_generation)
are sampled with the input script
[`../001_system_generation/scripts/in.PW_SL_compute`](../001_system_generation/scripts/in.PW_SL_compute).

`runme.bash` finds all `data.eta0.2_per20_<pos>` files written by the make
stage and, for each PW position `<pos>`, runs

```bash
lmp -log log.20ns_<pos> -v pos_pwall <pos> -in in.PW_SL_compute
```

in the `runs` directory, which reads `data.eta0.2_per20_<pos>`, fixes the PW
at `<pos>` and runs 20 ns. The thermo output is written to `log.20ns_<pos>`,
and the fluid density profiles to `fluid_20ns_<pos>.dat` and
`fluid_int_20ns_<pos>.dat`. The runs are executed one after another only to
show the procedure; in practice, every position should be submitted as a
separate job.

Because the runs take too long for an example, the log files of the runs
used in the paper are provided in `sample_data` (only the log files, due to
size constraints). In the paper, only 124 of the 171 positions written by
the make stage were sampled:

- 0.5 Å steps where the PW does not interact with the fluid yet (13.0–14.5 Å),
- 0.1 Å steps where the pressure on the PW changes sharply (14.6–22.9 Å),
- 0.2 Å steps on the tail (23.0–30.0 Å).

To sample the same positions, delete the other `data.eta0.2_per20_<pos>`
files before running `runme.bash`.

The input script used for the sample data was an earlier version of
`in.PW_SL_compute`; the simulation settings are identical.
