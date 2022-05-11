import math
import numpy as np
from scipy.stats import norm
from scipy import special
import matplotlib as mpl
import matplotlib.pyplot as plt


E = 8000                        # 8keV
Eeh = [3.62, 4.2, 4.43, 4.6]    # Electron-hole pair generation energy [Si, GaAs, CdTe, CZT]
F = 0.1
N = E/Eeh[0]
sigN = math.sqrt(F*N)

photon_count = 1000

y = norm.rvs(N, sigN, photon_count)
bin_min = (N - 4*sigN).__floor__()
bin_max = (N + 4*sigN).__floor__()
bins = np.linspace(bin_min, bin_max, bin_max-bin_min+1)

plt.title(f"E = 8keV, {Eeh[0]=:.2f}, {sigN=:.2f}, {photon_count} photons")
plt.hist(y, bins=bins)
plt.xlabel("Generated number of electrons")
plt.show()

