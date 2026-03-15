import pandas as pd
import numpy as np

print("Starting GridMind data pipeline...")

# -----------------------------
# Load datasets
# -----------------------------

demand = pd.read_csv("../data/AEP_hourly.csv")
stability = pd.read_csv("../data/smart_grid_stability_augmented.csv")
solar = pd.read_csv("../data/Plant_1_Generation_Data.csv")
wind = pd.read_csv("../data/T1.csv")

# -----------------------------
# Demand normalization
# -----------------------------

demand_values = demand.iloc[:,1]

demand_norm = (demand_values - demand_values.min()) / (
    demand_values.max() - demand_values.min() + 1e-6
)

TN_PEAK_DEMAND = 15000

tn_demand = demand_norm * TN_PEAK_DEMAND


# -----------------------------
# Solar normalization
# -----------------------------

solar_power = solar["DC_POWER"].fillna(0)

solar_norm = (solar_power - solar_power.min()) / (
    solar_power.max() - solar_power.min() + 1e-6
)

TN_SOLAR_CAPACITY = 1400

tn_solar = solar_norm * TN_SOLAR_CAPACITY


# -----------------------------
# Wind normalization
# -----------------------------

wind_values = wind.iloc[:,1]

wind_norm = (wind_values - wind_values.min()) / (
    wind_values.max() - wind_values.min() + 1e-6
)

TN_WIND_CAPACITY = 400

tn_wind = wind_norm * TN_WIND_CAPACITY


# -----------------------------
# Align dataset size
# -----------------------------

rows = min(
    len(tn_demand),
    len(tn_solar),
    len(tn_wind),
    len(stability)
)

tn_demand = tn_demand[:rows]
tn_solar = tn_solar[:rows]
tn_wind = tn_wind[:rows]
stability = stability.iloc[:rows]


# -----------------------------
# Simulated grid signals
# -----------------------------

np.random.seed(42)

ev_load = np.random.normal(800, 200, rows)
frequency = np.random.normal(50, 0.05, rows)
voltage = np.random.normal(1.0, 0.03, rows)


# -----------------------------
# Build dataset
# -----------------------------

df = pd.DataFrame({
    "demand": tn_demand,
    "solar": tn_solar,
    "wind": tn_wind,
    "ev_load": ev_load,
    "frequency": frequency,
    "voltage": voltage
})

for col in stability.columns:
    if col != "stabf":
        df[col] = stability[col]

df["fault_label"] = stability["stabf"]

df.to_csv("../data/gridmind_real.csv", index=False)

print("Dataset created:", df.shape)