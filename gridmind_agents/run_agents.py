from langgraph_workflow import graph
from utils.metrics_logger import MetricsLogger


logger = MetricsLogger()

state = {}

for step in range(20):

    result = graph.invoke(state)

    print("\n-----------------------------")

    print("Solar:", round(result["solar"],2))
    print("Demand:", round(result["demand"],2))
    print("Risk:", round(result["risk"],3))
    print("Status:", result["status"])
    print("Grid Action:", result["action"])
    print("Prosumer Signal:", result["pricing"])

    logger.log(step, result)


logger.save()