from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "co2": np.random.rand(100),
    "humidity": np.random.rand(100),
    "rainfall": np.random.rand(100),
    "temperature": np.random.rand(100) * 40
})

X = df[["co2", "humidity", "rainfall"]]
y = df["temperature"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, predictions))
