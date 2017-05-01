#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function, division, absolute_import

from collections import OrderedDict

import numpy as np
import pandas as pd

import decatur


def txt_light_curve(kic, q_start=None, q_end=None, interp_eclipse=True):
    """
    Save a Kepler light curve as a text file.
    
    Parameters
    ----------
    kic : int
        KIC ID of the star
    q_start : int, optional
        Only include quarters >= `q_start`
    q_end : int, optional
        Only included quarters <= `q_end`
    interp_eclipse : bool, optional
        Set to False to not interpolate over eclipses
    """
    eb = decatur.eclipsing_binary.EclipsingBinary.from_kic(kic)
    eb.normalize()
    if interp_eclipse:
        eb.interpolate_over_eclipse(window=1.5)

    # Include all quarters by default
    mask = np.repeat([True], len(eb.l_curve.quarters))

    # Mask out quarter range if specified
    if q_start is not None:
        mask &= eb.l_curve.quarters >= q_start
    else:
        q_start = eb.l_curve.quarters.min()

    if q_end is not None:
        mask &= eb.l_curve.quarters <= q_end
    else:
        q_end = eb.l_curve.quarters.max()

    columns = OrderedDict([('times', eb.l_curve.times[mask]),
                           ('fluxes', eb.l_curve.fluxes[mask])])

    df = pd.DataFrame(columns)

    df.to_csv('KIC{}_q{}-q{}.txt'.format(kic, q_start, q_end),
              header=False, index=False, sep=' ')
