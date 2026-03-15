import networkx as nx
import random


class SelfHealAgent:

    def __init__(self):

        self.grid = nx.DiGraph()

        # Tamil Nadu grid nodes
        self.grid.add_nodes_from([
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Salem",
            "Trichy"
        ])

        # transmission lines
        self.grid.add_edge("Salem", "Chennai", capacity=800)
        self.grid.add_edge("Trichy", "Chennai", capacity=600)
        self.grid.add_edge("Coimbatore", "Salem", capacity=500)
        self.grid.add_edge("Madurai", "Trichy", capacity=450)
        self.grid.add_edge("Salem", "Coimbatore", capacity=400)


    def stabilize(self, status):

        if status != "CRITICAL":
            return "No reroute required"

        # zones with potential surplus generation
        surplus_zones = [
            "Salem",
            "Coimbatore",
            "Madurai"
        ]

        # deficit zone (major load center)
        deficit_zone = "Chennai"

        # choose random surplus node
        source = random.choice(surplus_zones)

        try:
            path = nx.shortest_path(self.grid, source, deficit_zone)
            return f"Rerouting power via {path}"

        except nx.NetworkXNoPath:
            return "No available transmission path"