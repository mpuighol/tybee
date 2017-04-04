from __future__ import absolute_import, division, print_function
import pandas as pd
import matplotlib.pyplot as plt
import decatur


df = pd.read_csv('tybee/data/kebc_pu.csv', comment='#')
eb = decatur.eclipsing_binary.EclipsingBinary.from_kic(2569494)
eb.normalize()
eb.interpolate_over_eclipse(window=1.5)
plt.plot(eb.l_curve.times, eb.l_curve.fluxes)
plt.figure(2)
eb.run_periodogram()
plt.plot(eb.periods, eb.powers)
plt.axvline(eb.params.p_orb)
plt.show()