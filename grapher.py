import pickle
import matplotlib.pyplot as plt



file = open('momentum_basic_pickled', 'rb')
momentum_basic = pickle.load(file)
file.close()

file = open('static_60_40_pickled', 'rb')
static_60_40 = pickle.load(file)
file.close()

file = open('static_IVV_pickled', 'rb')
static_IVV = pickle.load(file)
file.close()


plt.figure()
plt.plot(momentum_basic.values())
plt.plot(static_IVV.values())
plt.plot(static_60_40.values())
plt.legend(("Momentum", "IVV", "60-40"))

plt.show()
