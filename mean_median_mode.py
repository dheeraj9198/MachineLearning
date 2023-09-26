import numpy
from scipy import stats
import matplotlib.pyplot as plt


speed = numpy.random.uniform(70, 110, 2500)

print(numpy.mean(speed))
print(numpy.median(speed))
print(stats.mode(speed))
print(numpy.std(speed))
print(numpy.var(speed))
print(numpy.percentile(speed, 75))

plt.hist(speed, 110)
plt.show()

plt.hist(numpy.random.normal(5.0, 4.0, 100000), 100)
plt.show()

x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

plt.scatter(x, y)
plt.show()