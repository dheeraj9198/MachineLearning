import numpy
import matplotlib.pyplot as plt
numpy.random.seed(2)
from sklearn.metrics import r2_score


# Generate an array 'x' with 1000 random numbers from a normal distribution with mean 3 and standard deviation 1
x = numpy.random.normal(3, 1, 100)
# Generate an array 'yy' with 1000 random numbers from a normal distribution with mean 150 and standard deviation 40
yy = numpy.random.normal(150, 40, 100)
# Perform element-wise division of 'yy' by 'x'
y = yy / x

train_x = x[:80]
train_y = y[:80]

test_x = x[80:]
test_y = y[80:]

mymodel = numpy.poly1d(numpy.polyfit(train_x, train_y, 4))

# Generate an array 'myline' with 100 evenly spaced values from 0 to 6
myline = numpy.linspace(0, 6, 1000)

r2 = r2_score(train_y, mymodel(train_x))
print(r2)
r2 = r2_score(test_y, mymodel(test_x))
print(r2)

plt.scatter(train_x, train_y)
plt.plot(myline, mymodel(myline),color='red')
plt.show()


