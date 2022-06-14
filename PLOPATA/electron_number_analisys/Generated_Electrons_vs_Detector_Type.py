import math
from scipy.stats import norm
import matplotlib.pyplot as plt


E = [8000, 8000, 22000, 22000]  # 8keV
Eeh = [3.62, 4.2, 4.43, 4.6]    # Electron-hole pair generation energy [Si, GaAs, CdTe, CZT]
F = 0.1

photon_count = 1000000

N = []
sigN = []
y = []
for i in range(len(Eeh)):
    N.append(E[i]/Eeh[i])
    sigN.append(math.sqrt(F*N[-1]))
    y.append(norm.rvs(N[-1], sigN[-1], photon_count))

plt.title(f"Number of electrons generated in different materials after {photon_count} hits")
plt.boxplot(y[2:4], vert=0)
plt.yticks([1, 2], ["CdTe", "CZT"])
plt.xlabel("Number of electrons")
plt.show()

