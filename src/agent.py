import pandas as pd
import pickle
import networkx as nx

from graph_topology import G

print("Initializing GridMind agents...")

# --------------------------
# Load trained models
# --------------------------

fault_detector = pickle.load(open("../models/fault_detector.pkl", "rb"))
forecaster = pickle.load(open("../models/load_forecaster.pkl", "rb"))

# --------------------------
# Prediction Agent
# --------------------------

class PredictionAgent:

    def predict(self, row):
        row = row.copy()

        # recreate training features
        row["solar_roc"] = 0
        row["ev_roc"] = 0
        row["freq_roc"] = 0
        row["voltage_roc"] = 0
        row["rolling_demand"] = row["demand"]

        # convert Series -> DataFrame
        df = pd.DataFrame([row])

        # keep only numeric features
        df = df.select_dtypes(include=["number"])

        features = df

        anomaly_score = fault_detector.decision_function(features)[0]

        predicted_stability = forecaster.predict(features)[0]

        risk_score = max(0, min(1, (1 - predicted_stability)))

        return {
            "anomaly_score": anomaly_score,
            "predicted_stability": predicted_stability,
            "risk_score": risk_score
        }


# --------------------------
# SelfHeal Agent
# --------------------------

class SelfHealAgent:

    def reroute(self, source, target):

        try:
            path = nx.shortest_path(G, source, target, weight="loss")

            loss = nx.path_weight(G, path, weight="loss")

            print("\nSELFHEAL ACTION")
            print("Reroute path:", " -> ".join(path))
            print("Transmission loss:", round(loss, 4))

            return path

        except nx.NetworkXNoPath:

            print("No reroute path available")

            return None


# --------------------------
# Prosumer Agent
# --------------------------

class ProsumerAgent:

    def send_price_signal(self, deficit):

        base_price = 4

        price = base_price + deficit / 100

        print("\nPROSUMER SIGNAL")
        print("Price updated to ₹", round(price,2))
        print("Expected demand reduction triggered")

        return price


# --------------------------
# GridMind Controller
# --------------------------

class GridMindController:

    def __init__(self):

        self.prediction = PredictionAgent()
        self.heal = SelfHealAgent()
        self.prosumer = ProsumerAgent()

    def run_step(self, row):

        pred = self.prediction.predict(row)

        print("\nPREDICTION AGENT")
        print("Risk score:", round(pred["risk_score"],3))
        print("Anomaly score:", round(pred["anomaly_score"],3))

        if pred["risk_score"] > 0.7:

            print("\n⚠ CRITICAL GRID RISK DETECTED")

            self.heal.reroute("Salem", "Chennai")

            self.prosumer.send_price_signal(200)


print("\nRunning GridMind test...")

df = pd.read_csv("../data/gridmind_real.csv")

# remove label columns
df = df.drop(columns=["fault_label"], errors="ignore")

# remove non-numeric columns
df = df.select_dtypes(include=["number"])

sample = df.iloc[0]

controller = GridMindController()

controller.run_step(sample)