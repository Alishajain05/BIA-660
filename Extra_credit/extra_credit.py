import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score
%matplotlib inline

def run():
    #X = np.array([[-3, -2], [-2, -2], [-3, -3], [1, 4], [6, 1], [1, 2], [4,5]])
    X = (np.random.uniform(0, 1, size=100)).reshape(100,1)
    y = (np.random.normal(0, 1, size=100)).reshape(100,1)
    y = 2 + 3*X + np.random.normal(0,0.25, size=100).reshape(100,1)
    #plt.plot(X, y, "k.")

    #nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(X)

    #plt.plot(X,Y)

    #ndices = nbrs.kneighbors(X)
    #return (X)

    def predict(data_point):
        knn3 = KNeighborsRegressor(n_neighbors=3, weights='uniform', algorithm='auto').fit(data_point, y)
        print(knn3.predict([2.7]))
        plt.figure(figsize=(12,9))
        line_x = np.array([[2], [5]])
        #knn_xx = kneighbors(X=data_point, n_neighbors=3, return_distance=True)
        #knn_x = np.linspace(0, 1, num=80).reshape(80,1)
        #print(knn_x)
        plt.plot(data_point,knn3.predict(data_point),"k.")
        plt.plot(line_x, "--")
        plt.legend()
    predict(X)

if __name__ == "__main__":
    run()
