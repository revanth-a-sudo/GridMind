from streaming.grid_simulator import GridSimulator
from agents.prediction_agent import PredictionAgent
from agents.decision_agent import DecisionAgent
from agents.selfheal_agent import SelfHealAgent
from agents.prosumer_agent import ProsumerAgent

import pandas as pd

sim = GridSimulator()

predictor = PredictionAgent()
decision = DecisionAgent()
selfheal = SelfHealAgent()
prosumer = ProsumerAgent()

records = []

for step in range(20):

    state = sim.simulate()

    risk = predictor.predict_risk(state)

    status = decision.evaluate(risk)

    action = selfheal.stabilize(status)

    pricing = prosumer.respond(status, risk)

    print(
        "Solar:", round(state["solar"],2),
        "| Demand:", round(state["demand"],2),
        "| Risk:", round(risk,3),
        "| Status:", status
    )

    print("Grid Action:", action)

    print("Prosumer Response:", pricing)

    print("----------------------------------")

    # store results
    records.append({
        "timestep": step,
        "solar": state["solar"],
        "demand": state["demand"],
        "risk": risk,
        "status": status,
        "grid_action": action,
        "pricing_signal": pricing
    })


# convert to dataframe
df = pd.DataFrame(records)

# save to excel
df.to_excel("gridmind_agent_results.xlsx", index=False)

print("\nExcel file saved as gridmind_agent_results.xlsx")