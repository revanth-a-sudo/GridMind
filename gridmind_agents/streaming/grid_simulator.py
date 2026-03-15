import numpy as np
import json
import time
import os


class GridSimulator:

    def __init__(self):

        profile_path = os.path.join(os.path.dirname(__file__), "grid_profile.json")

        with open(profile_path) as f:
            self.profile = json.load(f)

        self.t = 0

    def simulate(self):

        solar = max(
            0,
            np.random.normal(
                self.profile["solar_mean"],
                self.profile["solar_std"]
            )
        )

        demand = np.random.normal(
            self.profile["demand_mean"],
            self.profile["demand_std"]
        )

        ev_load = np.random.normal(
            self.profile["ev_mean"],
            self.profile["ev_std"]
        )

        frequency = np.random.normal(
            self.profile["freq_mean"],
            self.profile["freq_std"]
        )

        voltage = np.random.normal(
            self.profile["voltage_mean"],
            self.profile["voltage_std"]
        )

        # disturbance event every ~30 timesteps
        if self.t % 30 == 0 and self.t != 0:
            solar *= 0.3
            frequency -= 0.2

        self.t += 1

        time.sleep(0.5)

        return {
            "solar": float(solar),
            "demand": float(demand),
            "ev_load": float(ev_load),
            "frequency": float(frequency),
            "voltage": float(voltage)
        }