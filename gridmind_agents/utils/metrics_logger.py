import pandas as pd
import datetime


class MetricsLogger:

    def __init__(self):

        self.records = []

    def log(self, step, result):

        self.records.append({

            "timestamp": datetime.datetime.now(),
            "timestep": step,
            "solar": result["solar"],
            "demand": result["demand"],
            "risk": result["risk"],
            "status": result["status"],
            "grid_action": result["action"],
            "pricing_signal": result["pricing"]

        })

    def save(self):

        df = pd.DataFrame(self.records)

        df.to_excel("gridmind_runtime_metrics.xlsx", index=False)

        print("Runtime metrics saved to gridmind_runtime_metrics.xlsx")