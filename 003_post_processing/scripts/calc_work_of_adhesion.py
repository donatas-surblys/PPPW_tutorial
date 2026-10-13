#!/usr/bin/env python3
"""
Work of adhesion from the PPPW production logs (see README.md).

    python3 calc_work_of_adhesion.py <dir with log.20ns_<pos> files>
"""
import argparse
import os
import re
import sys

import numpy as np

# numpy >= 2.0 renamed trapz -> trapezoid
trapezoid = getattr(np, 'trapezoid', None) or np.trapz


def read_thermo(filename, columns):
    """Return the requested thermo columns of a LAMMPS log as a 2D array."""
    header = None
    rows = []
    in_block = False
    with open(filename) as fh:
        for line in fh:
            if line.startswith('   Step'):          # thermo header
                in_block = True
                if header is None:
                    header = line.split()
                    idx = [header.index(c) for c in columns]
                continue
            if not in_block:
                continue
            if line.startswith('Loop time'):          # end of thermo output
                in_block = False
                continue
            fields = line.split()
            if len(fields) == len(header) and not fields[0].startswith('WARN'):
                rows.append([float(fields[i]) for i in idx])
    if header is None:
        sys.exit(f'No thermo output found in {filename}')
    return np.array(rows)


def block_means(values, skip, n_block):
    """Means of n_block blocks after skipping `skip` rows, plus the overall mean.

    Returns an array of length n_block + 1; the last entry is the overall mean.
    """
    data = values[skip:]
    size = len(data) // n_block
    blocks = [data[j*size:(j+1)*size].mean() for j in range(n_block)]
    return np.array(blocks + [data.mean()])


def block_error(values, n_block):
    """Standard error of the mean from the block means (values[-1] = overall mean)."""
    var = (np.sum(values[:n_block]**2) / n_block - values[-1]**2) / (n_block - 1)
    return np.sqrt(abs(var))


def main():
    parser = argparse.ArgumentParser(
        description='Work of adhesion from PPPW production logs (log.20ns_<pos>).')
    parser.add_argument('logdir', help='directory containing the log.20ns_<pos> files')
    parser.add_argument('--pset', type=float, default=1.0,
                        help='set pressure of the piston [MPa] (default: 1.0)')
    parser.add_argument('--skip', type=int, default=10000,
                        help='thermo rows discarded as equilibration '
                             '(default: 10000 rows = 10 ns)')
    parser.add_argument('--nblock', type=int, default=4,
                        help='number of blocks for the error estimate (default: 4)')
    args = parser.parse_args()

    # PW positions from the file names: log.20ns_<pos>
    pattern = re.compile(r'log\.20ns_(\d+(?:\.\d+)?)$')
    files = {float(m.group(1)): os.path.join(args.logdir, f)
             for f in os.listdir(args.logdir) if (m := pattern.match(f))}
    if not files:
        sys.exit(f'No log.20ns_<pos> files found in {args.logdir}')
    z = np.array(sorted(files))                     # PW positions [A]
    nb = args.nblock

    # rows 0..nb-1: block means, row nb: overall mean
    press = np.zeros((nb + 1, len(z)))              # pressure on the PW [MPa]
    piston = np.zeros((2, nb + 1))                  # piston position [nm]
    for i, zi in enumerate(z):
        data = read_thermo(files[zi], ['v_press_pwall', 'v_z_virtual'])
        # v_press_pwall is the force on the wall (negative): flip sign, Pa -> MPa
        press[:, i] = -block_means(data[:, 0], args.skip, nb) * 1e-6
        if i == 0:
            piston[0] = block_means(data[:, 1], args.skip, nb) / 10    # A -> nm
        if i == len(z) - 1:
            piston[1] = block_means(data[:, 1], args.skip, nb) / 10

    # work done by the piston against the set pressure: MPa*nm = 1e-3 J/m^2
    w_piston = args.pset * (piston[1] - piston[0]) * 1e-3
    # integral of the PW pressure: MPa*A = 1e-4 J/m^2
    w_pw = np.array([trapezoid(press[j], z) for j in range(nb + 1)]) * 1e-4
    # work of adhesion (trapezoidal rule) for every block and the overall mean
    w_adh = w_pw - w_piston

    print(f'PW positions        : {len(z)} ({z[0]:.1f} - {z[-1]:.1f} A)')
    print(f'Averaging           : first {args.skip} thermo rows skipped, '
          f'{nb} blocks')
    print(f'Piston displacement : {piston[1, -1] - piston[0, -1]:.4f} nm '
          f'({piston[0, -1]:.4f} -> {piston[1, -1]:.4f} nm)')
    print()
    print(f'int P_PW dz         = {w_pw[-1]:.4e} +- {block_error(w_pw, nb):.1e} J/m^2')
    print(f'P_set * dz_piston   = {w_piston[-1]:.4e} +- {block_error(w_piston, nb):.1e} J/m^2')
    print()
    print(f'Work of adhesion W  = {w_adh[-1]:.4e} +- {block_error(w_adh, nb):.1e} J/m^2'
          f'  (trapezoidal rule, +- standard error)')
    print(f'                    = {w_adh[-1]*1e3:.3f} +- '
          f'{block_error(w_adh, nb)*1e3:.3f} mJ/m^2')


if __name__ == '__main__':
    main()
