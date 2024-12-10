import pandas as pd
import numpy as np
import pickle
import requests
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def model(file, n_iter=100, rank = 8, init_stdev=0.01, test_size=0.2):
    # Load the dataset from CSV
    df = pd.read_csv(file)
    df = df.dropna()
    cols = df.columns.tolist()
    df[cols[0]] = df[cols[0]].astype(str)
    df[cols[1]] = df[cols[1]].astype(str)
    df[cols[3]] = df[cols[3]].astype(int)


    # Ensure the column order matches the expectation
    if len(cols) < 4:
        raise ValueError("The dataset must have at least four columns: userId, itemId, rating, timestamp.")

    # Preprocess the data using DictVectorizer
    v = DictVectorizer(sparse=True)
    X = v.fit_transform(df[[cols[0], cols[1]]].to_dict(orient='records'))
    y = df[cols[2]].astype(int)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Train a local fastFM model
    local_model = sgd.FMRegression(
        n_iter=n_iter, 
        init_stdev=init_stdev, 
        l2_reg_w=0.1, 
        l2_reg_V=0.1, 
        rank=rank, 
        step_size=0.001
    )
    local_model.fit(X_train, y_train)

    return local_model, X_test, y_test

def evaluate(local_model, X_test, y_test):
    # Predict using the trained model
    pred = local_model.predict(X_test)
    # Ensure both predictions and true values are not NaN
    valid_indices = ~np.isnan(y_test) & ~np.isnan(pred)
    y_test = y_test[valid_indices]
    pred = pred[valid_indices]
    # Calculate the mean squared error
    accuracy = mean_squared_error(y_test, pred)
    return pred, accuracy
    
