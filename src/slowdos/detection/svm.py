import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
import joblib

# Import the dataset
df1 = pd.read_csv('data/dataset.csv')

df = df1.sample(frac = 1)
print(df.head(20))

# Splitting dataset into features and label
X = df.drop('Class', axis=1)
y = df['Class']

X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X_normal=scaler.fit_transform(X)

# Splitting the dataset into the training set and the test set
X_train, X_test, y_train, y_test = train_test_split(X_normal, y, test_size=0.4, random_state=42)


# Feature scaling (or standardization)
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)


# Fitting SVM with the training set
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train, y_train)

# Testing the model by classifying the test set
y_pred = classifier.predict(X_test)
# y_pred = classifier.predict(X_train)

X_xx = np.array([-0.53982399956658,1.9966985952636762,-0.5298222788524635,-0.5388923408653894,-0.38815997597924345])
X_xx = X_xx.reshape(1,-1)
print(classifier.predict(X_xx))
# # Creating confusion matrix for evaluation
cm = confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred)

# # Print out confusion matrix and report
# print(y_pred)
print(cm)
print(cr)

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# X_norm = (X - X.min())/(X.max() - X.min())
# pca = PCA(n_components=2) #2-dimensional PCA
# transformed = pd.DataFrame(pca.fit_transform(X_norm))
# print(transformed)

# print(X_train.shape)
# print(y_train.shape)
# ax = fig.add_subplot(projection='3d')
# plt.scatter(X_train[:,0], X_train[:,1], X_train[:,2], c=y_train)
# plt.show()
# pca = PCA(n_components=2)
# Xt = pca.fit_transform(X_normal)
# plot = plt.scatter(Xt[:,0], Xt[:,1], c=y)
# # plt.legend(handles=plot.legend_elements()[0], labels=list(winedata['target_names']))
# plt.show()

# plt.scatter(transformed[y==0][0], transformed[y==0][1], label='Class 1', c='red')
# plt.scatter(transformed[y==1][0], transformed[y==1][1], label='Class 2', c='blue')

# plt.legend()
# plt.show()

# Export model
filename = 'classifier.sav'
joblib.dump(classifier, filename)
print("Model exported!")
