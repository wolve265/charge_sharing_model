import math
from unittest import result
import numpy as np
from scipy.stats import norm
from scipy import special
import matplotlib as mpl
import matplotlib.pyplot as plt

def create_gauss_list(size, sig, electron_count) :
    # y = norm.rvs(0, sig, electron_count)
    y = norm.rvs(0, sig, size)
    y.sort()
    modulo_index = electron_count//size
    pure_gauss = []
    result = []
    pure_gauss = y
    # for i in range(electron_count) :
    #     if(i % modulo_index == 0):
    #         pure_gauss.append(y[i])

    for i in range(size) :
        counter = 0
        while(counter < modulo_index) :
            result.append(mean + pure_gauss[i])
            counter += 1
    return result

def calc_probabilities(y, pixel_dim):
    PI, PII, PIII = 0, 0, 0
    for i in y:
        if (-pixel_dim < i < 0):
            PI += 1
        elif (0 < i < pixel_dim):
            PII += 1
        elif (pixel_dim < i < 2*pixel_dim):
            PIII += 1
    return PI, PII, PIII


def OneD_calc_hit(mean, sig, electron_count, pixel_dim):
    # pixel_dim * 0.35

    #y = norm.rvs(mean, sig, electron_count)
    # y = norm.rvs(0, sig, electron_count)
    # y.sort()
    # size = 10
    # modulo_index = electron_count/size
    # pure_gauss = []
    # result = []
    # for i in range(electron_count) :
    #     if(i % modulo_index == 0):
    #         pure_gauss.append(y[i])

    # for i in range(size) :
    #     counter = 0
    #     while(counter < modulo_index) :
    #         result.append(mean + pure_gauss[i])
    #         counter += 1
    result = []
    size = 440 # 10, 20, 50, 100, 200, 440, 550, 1100, 2200
    result = create_gauss_list(size, sig, electron_count)


    PI, PII, PIII = calc_probabilities(result, pixel_dim)

    PSUM = PI + PII + PIII
    PI = PI / PSUM
    # PII = PII / PSUM
    PIII = PIII / PSUM

    if PI > PIII:
        x0 = -sig * math.sqrt(2) * special.erfinv(2*PI - 1)
    else:
        x0 = sig * math.sqrt(2) * special.erfinv(2*PIII - 1) + pixel_dim
    return x0, result

electron_count = 2200
pixel_dim = 75
mean = 70
sig = pixel_dim * 0.35

x0, y = OneD_calc_hit(mean, sig, electron_count, pixel_dim)
x = np.linspace(-pixel_dim, 2*pixel_dim, 3*pixel_dim + 1)
print(f"{x0=}")
print(f"{sig=}")

fig_size = 40

mpl.rcParams['font.family'] = 'DejaVu Sans'
# plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 2

fig = plt.figure()
ax = plt.axes()
# Edit the major and minor ticks of the x and y axes
ax.xaxis.set_tick_params(which='major', size=10, width=2, direction='in', top='on')
ax.xaxis.set_tick_params(which='minor', size=7,  width=2, direction='in', top='on')
ax.yaxis.set_tick_params(which='major', size=10, width=2, direction='in', right='on')
ax.yaxis.set_tick_params(which='minor', size=7,  width=2, direction='in', right='on')
# Edit the major and minor tick locations
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(50))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(25))
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(5))
# Set the axis limits
ax.set_xlim(-1.25*pixel_dim, 2.25*pixel_dim)
ax.set_ylim(0, fig_size)
# Add the x and y-axis labels
ax.set_xlabel(f'Position (μm)',                 labelpad=5)
ax.set_ylabel('Amount of electrons detected',   labelpad=5)

plt.title(f"1D charge distribution.\n Real hit at {mean:2.3f} μm. Calculated hit at {x0:2.3f}μm")
plt.hist(y, bins=len(x))
plt.vlines(-pixel_dim, 0, fig_size,     colors="black")
plt.vlines(0,    0, fig_size,           colors="black")
plt.vlines(pixel_dim,  0, fig_size,     colors="black")
plt.vlines(2*pixel_dim,  0, fig_size,   colors="black")
plt.vlines(mean, 0, fig_size/2,         colors="red",   label="real hit position")
plt.legend()
plt.show()

# plt.title(f"1D charge distribution.\n Real hit at {mean}um. Calculated hit at {x0:.3f}um")
# plt.hist(y, bins=len(x))
# plt.vlines(-100, 0, 30,  colors="black")
# plt.vlines(0,    0, 30,  colors="black")
# plt.vlines(100,  0, 30,  colors="black")
# plt.vlines(200,  0, 30,  colors="black")
# plt.vlines(mean, 0, 15,         colors="red",   label="hit position")
# plt.vlines(mean - 3*sig, 0, 15, colors="green", label="+-3sig")
# plt.vlines(mean + 3*sig, 0, 15, colors="green")
# plt.xlabel("x[um]")
# plt.ylabel("nr of electrons")
# plt.legend()
# plt.show()
