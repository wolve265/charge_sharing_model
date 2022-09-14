import current_model.model as mod
import matplotlib.pyplot as plt

x = mod.Model(35, 75, 2200)
y = mod.Model(50, 75, 2200)

print(x.charge_distribution)
print(y.charge_distribution)

plt.scatter(x.charge_distribution, y.charge_distribution, s=1)
plt.hlines(0, -75, 150, colors="black")
plt.hlines(75, -75, 150, colors="black")
plt.vlines(0, -75, 150, colors="black")
plt.vlines(75, -75, 150, colors="black")
plt.show()