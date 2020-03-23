# -*- coding: utf-8 -*-
"""aiproj.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KluDqolGu3lufXscqBt8L0pgjnyj-3xS
"""

print("CASH FLOW")

pip install quandl

#dependencies
import quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
df2 = pd.read_csv(io.BytesIO(uploaded['train.csv']))
# Dataset is now stored in a Pandas Dataframe

df2 = df2[['CLIENT_OUT']]
print(df2.head(5))
#print(dfcash.head())

#Varialbe to predict 'n' days out
forecast_out = 30
#created new column ( a dependent var) - shifted n uniteds up
df2['Prediction'] = df2[['CLIENT_OUT']].shift(-forecast_out)
print(df2.tail(5))

#create independent data set
#convert df to numpy array
X = np.array(df2.drop(['Prediction'],1))
#remove last n rows
X = X[:-forecast_out]
print(X)

### Create the dependent data set (y)  #####
# Convert the dataframe to a numpy array (All of the values including the NaN's)
y = np.array(df2['Prediction'])
# Get all of the y values except the last 'n' rows
y = y[:-forecast_out]
print(y)

# Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and train the Support Vector Machine (Regressor)
svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
#svr_rbf.fit(x_train, y_train)

print(df2.head(8))

# Create and train the Linear Regression  Model
lr = LinearRegression()
# Train the model
lr.fit(x_train, y_train)

"""# New Section"""

# Testing Model: Score returns the coefficient of determination R^2 of the prediction. 
# The best possible score is 1.0
lr_confidence = lr.score(x_test, y_test)
print("lr confidence: ", lr_confidence)

# Set x_forecast equal to the last 30 rows of the original data set from Adj. Close column
x_forecast = np.array(df2.drop(['Prediction'],1))[-forecast_out:]
print(x_forecast)

# Print linear regression model predictions for the next 'n' days
lr_prediction = lr.predict(x_forecast)
print(lr_prediction)

# Print support vector regressor model predictions for the next 'n' days
svm_prediction = svr_rbf.predict(x_forecast)
print(svm_prediction)