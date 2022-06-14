# Imports for model testing
import model as md
import matplotlib.pyplot as plt

# Model testing
real_hit = 35
pixel_dim = 75
nr_of_el = 2200

mod = md.Model(real_hit=real_hit, pixel_dim=pixel_dim, nr_of_el=nr_of_el)
x0 = mod.OneD_calc_hit()

PI, PII, PIII = mod.calc_probabilities()

print(f"Error: {abs(mod.real_hit - x0)}um")

plt.title(f"1D charge distribution for hit at {real_hit}, with σ={mod.sigma}")
plt.hist(mod.charge_distribution, bins=mod.pixel_coordinates)
plt.vlines(   mod.real_hit, 0, 20, colors="red", label="Real Hit")
plt.vlines(             x0, 0, 20, colors="green", label="Calc Hit")
plt.vlines( -mod.pixel_dim, 0, 40, colors="black")
plt.vlines(              0, 0, 40, colors="black")
plt.vlines(  mod.pixel_dim, 0, 40, colors="black")
plt.vlines(2*mod.pixel_dim, 0, 40, colors="black")
plt.legend()
plt.show()