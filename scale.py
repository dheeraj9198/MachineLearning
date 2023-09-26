import pandas
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
import os
import tempfile
import gzip
from datetime import datetime, timedelta, timezone

print(datetime.today().strftime('%Y-%m-%d-%H-%M'))
print((datetime.today()-timedelta(minutes=10)).strftime('%Y-%m-%d-%H-%M'))
print(datetime.today().isoformat().replace(":", "-").replace(".", "-"))

input_list = [{'a': 'b', 'c': [1, 2, 3, 4], 'd': {'x': 'y'}},{'a': 'b', 'c': [1, 2, 3, 4], 'd': {'x': 'y'}}]
print(str(input_list))

temp_file = tempfile.NamedTemporaryFile()
print(temp_file.name)



list_to_upload = []
for data in input_list:
    list_to_upload.append(str(data))
result = '\n'.join(list_to_upload)
print(result)
with gzip.open(temp_file.name, 'wb') as f_out:
    f_out.write(result.encode())
    f_out.close()
    print(temp_file.name)

print(gzip.open(temp_file.name).read())

exit(0)

scale = StandardScaler()

df = pandas.read_csv("data.csv")

X = df[['Weight', 'Volume']]
y = df['CO2']

scaledX = scale.fit_transform(X)

print(scaledX)

regr = linear_model.LinearRegression()
regr.fit(scaledX, y)

scaled = scale.transform([[2300, 1.3]])

predictedCO2 = regr.predict([scaled[0]])
print(predictedCO2)

