#!/usr/bin/env python
# -*- coding: utf-8 -*-
# written by Christoph Federrath, 2023

import numpy as np
import argparse
import cfpack as cfp
from cfpack import stop, print


# === test for cfpack.fit ===
def test_fit(n=21):

    def func1(x, p):
        y = 0*x + p
        return y

    def func2(x, p0, p1):
        y = p0*x + p1
        return y

    # some x data
    xdat = cfp.get_1d_coords(cmin=-10., cmax=10., ndim=n, cell_centred=False)

    # constant func 1
    print("=== Fit (constant with y errors):", color="magenta")
    ydat = np.array([3.5]*n)
    yerr = np.array([1.0]*n)
    weights = 1/yerr
    fitres = cfp.fit(func1, xdat, ydat, weights=weights)
    fitres = cfp.fit(func1, xdat, ydat, weights=weights, scale_covar=False)
    fitres = cfp.fit(func1, xdat, ydat, yerr=yerr)

    # linear func 2
    print("=== Fit (linear func with y errors):", color="magenta")
    ydat = func2(xdat, 0.5, 1.5)
    yerr = ydat*0 + 0.5 + cfp.generate_random_gaussian_numbers(n=n, mu=0, sigma=0.05, seed=None)
    fitres_w = cfp.fit(func2, xdat, ydat, weights=1/yerr, scale_covar=False)
    fitres_e = cfp.fit(func2, xdat, ydat, yerr=yerr)
    cfp.plot(ydat, xdat, yerr=[yerr,yerr], linestyle=None, marker='o', label="data with y errors")
    cfp.plot(func2(xdat, *fitres_w.popt), xdat, label="fit with weights")
    cfp.plot(func2(xdat, *fitres_e.popt), xdat, label="fit with y errors")
    print("=== Fit (linear func with x errors):", color="magenta")
    ydat = func2(xdat, 0.5, 3.0)
    xerr = xdat*0 + 1.0 + cfp.generate_random_gaussian_numbers(n=n, mu=0, sigma=0.1, seed=None)
    cfp.plot(ydat, xdat, xerr=[xerr,xerr], linestyle=None, marker='o', label="data with x errors")
    fitres_e = cfp.fit(func2, xdat, ydat, xerr=xerr)
    cfp.plot(func2(xdat, *fitres_e.popt), xdat, label="fit with x errors")
    print("=== Fit (linear func with x and y errors):", color="magenta")
    ydat = func2(xdat, 0.5, 4.5)
    cfp.plot(ydat, xdat, xerr=[xerr,xerr], yerr=[yerr,yerr], linestyle=None, marker='o', label="data with x and y errors")
    fitres_e = cfp.fit(func2, xdat, ydat, xerr=xerr, yerr=yerr)
    cfp.plot(func2(xdat, *fitres_e.popt), xdat, label="fit with x and y errors")
    cfp.plot(show=True)

    stop()


# ===== the following applies in case we are running this in script mode =====
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test suite for cfpack.')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand', description='valid subcommands',
                                        help='additional help', required=True)
    # sub parser for 'fit' sub-command
    parser_adobe = subparsers.add_parser('fit')
    args = parser.parse_args()

    if args.subcommand == 'fit':
        test_fit()
