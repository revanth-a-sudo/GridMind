import numpy as np
import pickle
import random
import os




class PredictionAgent:

    def __init__(self):

        # Get project root directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        model_path = os.path.join(base_dir, "models", "load_forecaster.pkl")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)


    def build_features(self):

        # Smart Grid Stability parameters
        tau = np.random.uniform(0.5, 2.0, 4)

        p = np.random.uniform(-1, 1, 4)

        g = np.random.uniform(0.1, 1.0, 4)

        features = [
            tau[0], tau[1], tau[2], tau[3],
            p[0], p[1], p[2], p[3],
            g[0], g[1], g[2], g[3]
        ]

        return np.array([features])


    def predict_risk(self, state):

        features = self.build_features()

        predicted_stability = self.model.predict(features)[0]

        ml_risk = 1 / (1 + np.exp(predicted_stability))

        # physics-based risk
        demand = state["demand"]
        solar = state["solar"]
        ev = state["ev_load"]
        freq = state["frequency"]

        supply = solar + 5000
        load = demand + ev

        imbalance = abs(load - supply) / max(supply, 1)

        freq_penalty = abs(50 - freq)

        physics_risk = min(1, imbalance + freq_penalty)

        risk = 0.5 * ml_risk + 0.5 * physics_risk

        return float(risk)