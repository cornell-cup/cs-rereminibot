import matplotlib.pyplot as plt
import numpy as np
x = np.loadtxt('LatencyMeasurements.txt', delimiter=',',unpack=True)

plt.plot(x)
plt.xlabel('X-axis')
plt.title('Data from text file')
plt.show()