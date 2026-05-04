import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import matplotlib.pyplot as plt

# Load Auto MPG dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
cols = ["mpg","cylinders","displacement","horsepower","weight",
        "acceleration","model_year","origin","car_name"]

df = pd.read_csv(url, names=cols, sep=r'\s+', na_values='?')
df.dropna(inplace=True)
df.drop("car_name", axis=1, inplace=True)

X = df.drop("mpg", axis=1)
y = df["mpg"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Store feature names for later use
feature_names = X.columns.tolist()

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)

y_pred = rf.predict(X_test_scaled)
print(f"R² Score : {r2_score(y_test, y_pred):.4f}")
print(f"RMSE     : {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

# Feature importance chart
feat_imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values()
feat_imp.plot(kind='barh', title='Feature Importance')
plt.tight_layout()
plt.savefig("static/feature_importance.png")
plt.close()

# Save model + scaler + feature names together
with open("model/model.pkl", "wb") as f:
    pickle.dump({"model": rf, "scaler": scaler, "feature_names": feature_names}, f)

print("Model saved to model/model.pkl")