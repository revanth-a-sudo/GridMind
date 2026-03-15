from langgraph.graph import StateGraph
from typing import TypedDict

from streaming.grid_simulator import GridSimulator
from agents.prediction_agent import PredictionAgent
from agents.decision_agent import DecisionAgent
from agents.selfheal_agent import SelfHealAgent
from agents.prosumer_agent import ProsumerAgent


# ---------- Define Shared State ----------
class GridState(TypedDict):

    solar: float
    demand: float
    risk: float
    status: str
    action: str
    pricing: str


sim = GridSimulator()

prediction_agent = PredictionAgent()
decision_agent = DecisionAgent()
selfheal_agent = SelfHealAgent()
prosumer_agent = ProsumerAgent()


# ---------- Agent Nodes ----------

def prediction_node(state):

    grid = sim.simulate()

    risk = prediction_agent.predict_risk(grid)

    return {
        "solar": grid["solar"],
        "demand": grid["demand"],
        "risk": risk
    }


def decision_node(state):

    status = decision_agent.evaluate(state["risk"])

    return {"status": status}


def selfheal_node(state):

    action = selfheal_agent.stabilize(state["status"])

    return {"action": action}


def prosumer_node(state):

    pricing = prosumer_agent.respond(state["status"], state["risk"])

    return {"pricing": pricing}


# ---------- Build Graph ----------

builder = StateGraph(GridState)

builder.add_node("prediction", prediction_node)
builder.add_node("decision", decision_node)
builder.add_node("selfheal", selfheal_node)
builder.add_node("prosumer", prosumer_node)

builder.set_entry_point("prediction")

builder.add_edge("prediction", "decision")
builder.add_edge("decision", "selfheal")
builder.add_edge("selfheal", "prosumer")

graph = builder.compile()