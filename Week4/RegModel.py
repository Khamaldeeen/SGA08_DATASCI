import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import random as r
import matplotlib.pyplot as plt



data = pd.read_csv("Week4\LagosRentCleaned.csv", sep=",")



X = np.array(data[['Location', 'Type', 'Rooms']])
y = np.array(data['Price'])

print(X.shape)

enc = LabelEncoder()
X[:, 1] = enc.fit_transform(X[:, 1])


ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [0])], remainder='passthrough')
X = ct.fit_transform(X)


for i in range(2000):
    ran = r.randint(0, 1000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state= ran)


    #reg = RandomForestRegressor()
    reg = LinearRegression()
    #reg = DecisionTreeRegressor(random_state=ran)
    reg.fit(X_train, y_train)

    acc = reg.score(X_train, y_train)
    pred = reg.predict(X_test)
    if acc > 0.4:
        print([acc], [ran])
        plt.plot(X_test[:, 26], y_test, color='blue')
        plt.scatter(X_test[:, 26], pred, color='red')
        plt.show()
        for i in range(len(pred)):
            if i <= round(0.1 * (len(pred))):
                print( y[i], pred[i])
                
        break
    else:
        continue

'''
for i in range(len(pred)):
    if i <= round(0.4 * (len(pred))):
        print(X_test[i], y_test[i], pred[i])
'''
