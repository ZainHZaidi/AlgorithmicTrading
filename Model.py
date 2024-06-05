import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingRegressor

# Load dataset
data = pd.read_csv("sum.csv")
y = data["yield"].tolist()
data = data.drop("yield",axis=1)

X = data.values


# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
rf_classifier = GradientBoostingRegressor(loss="huber", n_estimators=10000).fit(X_train, y_train)

# Train the model


# Make predictions
y_pred = rf_classifier.predict(X_test)

# Evaluate the model
accuracy = rf_classifier.score(X_test, y_test)
print(accuracy)

print(y_test)
error_sum = 0
for i in range(len(y_pred)):
    e = y_pred[i]
    a = y_test[i]
    error_sum += ((abs(a-e))/a)

print(error_sum/len(y_pred)*100)