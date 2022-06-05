from matplotlib.cbook import index_of
import numpy as np
import matplotlib.pyplot as plt
import math

#generate gauss
a = 1 #szerokosc jednego pixela
mi = 0.4  # 0 < mi < 1 dla a = 1
#mi2d = [0.4, 0.4]  # 0 < mi < 1 dla a = 1
sigma = 0.35 # sigma zeby wartosci byly od -1 do 2
#sigma2d = [[0.4, 0.4], [0.4, 0.4]] # sigma zeby wartosci byly od -1 do 2
size = 2200
#size2d = (1, 100)
s_mean_0 = np.random.normal(0, sigma, size)
s_mean_0.sort()
gauss_size = 20
modulo_index = size/gauss_size
result = []
for i in range(size) :
    if(i % modulo_index == 0):
        result.append(s_mean_0[i])

print(result, len(result))
s = np.random.normal(mi, sigma, size)
#s2d = np.random.multivariate_normal(mi2d, sigma2d, size2d)

#left pixel probability
error_func1_numerator = -mi
error_func1_denominator = sigma * (math.sqrt(2))
error_func1 = error_func1_numerator/error_func1_denominator
PxI = 0.5 + 0.5 * math.erf(error_func1)

#right pixel probability
error_func2_numerator = mi - a
error_func2_denominator = (sigma * (math.sqrt(2)))
error_func2 = error_func2_numerator / error_func2_denominator
PxIII = 0.5 + 0.5 * math.erf(error_func2)

#center pixel probability
PxII = 1 - (PxI + PxIII)

print(f'Left pixel -> {PxI:.3}\nCenter pixel -> {PxII:.3}\nRight pixel -> {PxIII:.3}')

#x0 position
if(PxI > PxII) :
    x0 = -sigma * math.sqrt(2) * (1/math.erf(2 * PxI - 1))
else :
    x0 = sigma * math.sqrt(2) * (1/math.erf(2 * PxIII - 1)) + a

print(f'x0 position -> {x0:.3}')

# mean = [0.4, 0.8]
# cov = [[0, 0.4], [-0.2, 0.3]]
# x, y = np.random.multivariate_normal(mean, cov, 5000).T
# plt.plot(x, y, 'x')
# plt.axis('equal')
# plt.show()
#plot gauss
count, bins, ignored = plt.hist(s, len(s), density=True)

print("rozmiar binow: ", len(bins))
print(bins)
plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) *
            np.exp(- (bins - mi) ** 2 / (2 * sigma ** 2)),
            linewidth=2, color='r')
y = np.linspace(0,1.5,1000)
plt.plot(len(y) * [x0], y, linewidth=4, color='y')
plt.show()