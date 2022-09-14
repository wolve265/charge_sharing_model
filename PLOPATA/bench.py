import current_model.model as mod
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

real_hit = 35
pixel_dim = 75
nr_of_el = 2200

iterations = np.linspace(0, 100, 101)
float_x0 = []
int_x0 = []
for i in iterations:
    scenario = mod.Model(real_hit=real_hit, pixel_dim=pixel_dim, nr_of_el=nr_of_el)
    float_x0.append(scenario.OneD_calc_hit())
    int_x0.append(scenario.OneD_calc_hit_int(100))

float_x0_mean = stat.mean(float_x0)
int_x0_mean = stat.mean(int_x0)
float_x0_stdev = stat.stdev(float_x0)
int_x0_stdev = stat.stdev(int_x0)

print(f"{float_x0_mean=}, {float_x0_stdev=}\n{int_x0_mean=}, {int_x0_stdev=}")

float_x0_err = []
int_x0_err = []
for f, i in zip(float_x0, int_x0):
    float_x0_err.append(abs(real_hit-f))
    int_x0_err.append(abs(real_hit - i))

float_x0_err_mean = stat.mean(float_x0_err)
int_x0_err_mean = stat.mean(int_x0_err)
# ----------------------------------------------------------------------------------------------------------------------

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.set_title(f"Calculated hit per iteration in float implementation, stdev = {float_x0_stdev:1.3f}")
ax1.set(xlabel="Iteration nr", ylabel="Hit position [μm]")
ax1.scatter(iterations, float_x0, c="blue", s=5, label="calc hits")
ax1.hlines(float_x0_mean, iterations[0], iterations[-1], colors="red", label="calc mean")
ax1.hlines(real_hit, iterations[0], iterations[-1], colors="green", label="real hit")
ax1.legend()

ax2.set_title(f"Calculated hit per iteration in float implementation, stdev = {int_x0_stdev:1.3f}")
ax2.set(xlabel="Iteration nr", ylabel="Hit position [μm]")
ax2.scatter(iterations, int_x0, c="blue", s=5, label="calc hits")
ax2.hlines(int_x0_mean, iterations[0], iterations[-1], colors="red", label="calc mean")
ax2.hlines(real_hit, iterations[0], iterations[-1], colors="green", label="real hit")
ax2.legend()

ax3.set_title("Error calculations in float implementation")
ax3.set(xlabel="Iteration nr", ylabel="Absolute error [μm]")
ax3.scatter(iterations, float_x0_err, c="blue", s=5, label="calc error")
ax3.hlines(float_x0_err_mean, iterations[0], iterations[-1], colors="red", label="error mean")
ax3.legend()

ax4.set_title("Error calculations in integer implementation")
ax4.set(xlabel="Iteration nr", ylabel="Absolute error [μm]")
ax4.scatter(iterations, int_x0_err, c="blue", s=5, label="calc error")
ax4.hlines(int_x0_err_mean, iterations[0], iterations[-1], colors="red", label="error mean")
ax4.legend()

fig.tight_layout()
plt.show()