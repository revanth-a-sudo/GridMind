import pandas as pd
import time

from agent import GridMindController

print("Starting GridMind demo replay...")

df = pd.read_csv("../data/gridmind_real.csv")
df = df.drop(columns=["fault_label"], errors="ignore")

controller = GridMindController()

print("\n==============================")
print(" GRIDMIND DEMO SIMULATION ")
print("==============================")

start_index = 15000
previous_row = None

for step in range(20):

    row = df.iloc[start_index + step].copy()

    # ---------------------------------
    # Forced blackout scenario
    # ---------------------------------
    if 10 <= step <= 14:

        print("⚠ Simulating renewable collapse + EV surge")

        row["solar"] *= 0.15       # solar crash
        row["ev_load"] *= 2.0      # EV spike
        row["frequency"] -= 0.4    # frequency drop
        row["voltage"] -= 0.08

    # ---------------------------------
    # Feature engineering
    # ---------------------------------
    if previous_row is not None:

        row["solar_roc"] = row["solar"] - previous_row["solar"]
        row["ev_roc"] = row["ev_load"] - previous_row["ev_load"]
        row["freq_roc"] = row["frequency"] - previous_row["frequency"]
        row["voltage_roc"] = row["voltage"] - previous_row["voltage"]

    else:

        row["solar_roc"] = 0
        row["ev_roc"] = 0
        row["freq_roc"] = 0
        row["voltage_roc"] = 0

    row["rolling_demand"] = row["demand"]

    print("\n-----------------------------")
    print("Time Step:", step)

    print(
        "Solar:", round(row["solar"],2),
        "| EV:", round(row["ev_load"],2),
        "| Frequency:", round(row["frequency"],3)
    )

    controller.run_step(row)

    previous_row = row

    time.sleep(0.2)

print("\nDemo simulation complete.")