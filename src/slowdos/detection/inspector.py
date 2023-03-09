import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
import joblib, warn

filename = 'classifier.sav'
classifier = joblib.load(filename)
# dt_realtime = pd.read_csv('realtime.csv',delimiter=",")
dt_realtime = np.genfromtxt('realtime.csv', delimiter=",")
X = np.array(dt_realtime)
X = X.reshape(1,-1)


# print(X)
result = classifier.predict(X)
# print(result)

with open('.result', 'w') as f:
    f.write(str(result[0]))
