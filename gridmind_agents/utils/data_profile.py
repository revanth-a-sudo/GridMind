import pandas as pd
import json

df = pd.read_csv("../../data/gridmind_real.csv")

profile = {
    "solar_mean": df["solar"].mean(),
    "solar_std": df["solar"].std(),

    "demand_mean": df["demand"].mean(),
    "demand_std": df["demand"].std(),

    "ev_mean": df["ev_load"].mean(),
    "ev_std": df["ev_load"].std(),

    "freq_mean": df["frequency"].mean(),
    "freq_std": df["frequency"].std(),

    "voltage_mean": df["voltage"].mean(),
    "voltage_std": df["voltage"].std()
}

with open("../streaming/grid_profile.json","w") as f:
    json.dump(profile,f,indent=2)

print("Grid statistical profile created.")