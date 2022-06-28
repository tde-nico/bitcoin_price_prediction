# -*- coding: utf-8 -*-
"""Bitcoin_Price_Prediction

Automatically generated by Colaboratory.
"""

# Description: This program uses an artificial neural network called Long Short Term Memory (LSTM)
#              to predict the closing stock price of a corporation using the past 60 day stock price.

# Install dependencies
! pip install -U pandas_datareader

# Import the libraries
import math
import datetime as dt
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Get the stock quote
df = web.DataReader(
    'BTC-USD',
    data_source='yahoo',
    start='2020-01-01',
    end=dt.datetime.now()
)
# Show the data
df

df.shape

# Visualize the closing price history
plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('USD [$]', fontsize=18)
plt.show()

# Create a new dataframe with only the 'Close' column
data = df.filter(['Close'])
# Convert the dataframe into a numpy array
dataset = data.values
# Get the number of rows to train the model on
training_data_len = math.ceil(len(dataset) * 0.8)
print(training_data_len)

# Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

# Create the training dataset
# Create the scaled training data set
train_data = scaled_data[0:training_data_len, :]
# Split the data into x_train and y_train data sets
prediction_days = 60
x_train = []
y_train = []
for i in range(prediction_days, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])

# Convert the x_train and y_train to numpy arrays
x_train = np.array(x_train)
y_train = np.array(y_train)
# Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

# Build the LSTM model
neurons = 50

model = Sequential()
model.add(LSTM(neurons, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(neurons, return_sequences=False))
model.add(Dense(neurons / 2))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(x_train, y_train, batch_size=1, epochs=20)

# Create the testing data set
test_data = scaled_data[training_data_len - prediction_days:, :]
# Create the x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(prediction_days, len(test_data)):
  x_test.append(test_data[i-prediction_days:i, 0])

# Convert the data to a numpy array
x_test = np.array(x_test)
# Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Get the models predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Get the root mean squared error (RMSE)
rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
print(rmse)

# Plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
# predictions = predictions - rmse
valid['Predictions'] = predictions
# Visualize the data
plt.figure(figsize=(24,12))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('USD [$]', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()

# Show the valid and predicted prices
valid

# Get the quote
quote = web.DataReader(
    'BTC-USD',
    data_source='yahoo',
    start='2018-01-01',
    end=dt.datetime.now()
)
# Create a new dataframe
new_df = quote.filter(['Close'])
# Get the last 60 days closing price values
last_60_days = new_df[-60:].values
# Scale data to be between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
# Create test
x_test = []
# Append the last 60 days
x_test.append(last_60_days_scaled)
# Convert the x_test to a numpy array
x_test = np.array(x_test)
# Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
# Get the predicted scaled price
pred_price = model.predict(x_test)
# Undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)
