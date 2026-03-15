import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# load processed dataset
df = pd.read_csv("../data/stability_processed.csv")
X = df.drop(columns=["stab"])
y = df["stab"]

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBRegressor(
    n_estimators=50,
    learning_rate=0.05,
    max_depth=6
)

training_log = []

for epoch in range(1, 51):

    model.set_params(n_estimators=epoch)
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    val_pred = model.predict(X_val)

    train_loss = mean_squared_error(y_train, train_pred)
    val_loss = mean_squared_error(y_val, val_pred)

    training_log.append({
        "epoch": epoch,
        "train_loss": train_loss,
        "val_loss": val_loss
    })

    print(f"Epoch {epoch} | Train Loss {train_loss:.4f} | Val Loss {val_loss:.4f}")

# save model
import pickle
pickle.dump(model, open("../models/load_forecaster.pkl", "wb"))

# save training metrics
log_df = pd.DataFrame(training_log)

log_df.to_excel("../models/training_metrics.xlsx", index=False)

print("\nTraining metrics saved to models/training_metrics.xlsx")