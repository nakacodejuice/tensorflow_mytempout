import numpy as np
import pandas as pd


# Import data
data = pd.read_csv('/home/rootkit/out.csv')

# Drop date variable
data = data.drop(['date'], 1)
data = data.drop(['date1'], 1)
data = data.drop(['date2'], 1)

# Dimensions of dataset
n = data.shape[0]
p = data.shape[1]

# Make data a np.array
data = data.values

# Training and test data
train_start = 0
train_end = int(np.floor(0.8*n))
test_start = train_end + 1
test_end = n
data_train = data[np.arange(train_start, train_end), :]
data_test = data[np.arange(test_start, test_end), :]