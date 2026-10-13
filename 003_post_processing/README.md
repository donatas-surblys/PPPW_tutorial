# Post-processing

In this folder, we finally obtain the work of solid-liquid adhesion from the
production runs with `scripts/calc_work_of_adhesion.py`, which reads the
`log.20ns_<pos>` files directly (python3 and numpy are needed):

```bash
bash runme.bash                               # sample data
bash runme.bash ../002_production_runs/runs   # your own runs
```

The result is printed and saved to `work_of_adhesion.txt`.

For each PW position, the first 10 ns are discarded as equilibration and
`v_press_pwall` is averaged over the last 10 ns, with its sign flipped to give
the pressure exerted on the PW, P<sub>PW</sub>. The work of adhesion is

```
W = int P_PW dz - P_set * dz_piston
```

where the integral is evaluated with the trapezoidal rule over all PW
positions, P<sub>set</sub> = 1 MPa, and dz<sub>piston</sub> is the change of
the mean piston position (`v_z_virtual`) between the first and the last PW
position. The standard error of the mean is obtained by repeating the
calculation for four 2.5 ns blocks.
