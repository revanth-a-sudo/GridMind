import networkx as nx

print("Building Tamil Nadu grid topology...")

# Create directed graph
G = nx.DiGraph()

# -------------------------
# Add nodes (grid zones)
# -------------------------

zones = {
    "Chennai": {"capacity": 3200, "priority": 1},
    "Coimbatore": {"capacity": 2100, "priority": 2},
    "Madurai": {"capacity": 1800, "priority": 3},
    "Salem": {"capacity": 1400, "priority": 4},
    "Trichy": {"capacity": 1600, "priority": 5},
}

for zone, data in zones.items():
    G.add_node(zone, **data)

# -------------------------
# Add transmission lines
# -------------------------

edges = [
    ("Salem", "Chennai", 800, 0.02),
    ("Trichy", "Chennai", 600, 0.03),
    ("Coimbatore", "Salem", 500, 0.02),
    ("Madurai", "Trichy", 450, 0.02),
    ("Salem", "Coimbatore", 400, 0.01),
]

for src, dst, capacity, loss in edges:
    G.add_edge(src, dst, capacity=capacity, loss=loss)

print("Nodes:", G.nodes(data=True))
print("Edges:", G.edges(data=True))

# -------------------------
# Find best reroute path
# -------------------------

def find_reroute_path(source, target):

    try:
        path = nx.shortest_path(G, source, target, weight="loss")
        loss = nx.path_weight(G, path, weight="loss")

        print("\nOptimal reroute path:")
        print(" -> ".join(path))
        print("Total transmission loss:", loss)

        return path

    except nx.NetworkXNoPath:
        print("No path available")
        return None


# Test rerouting

find_reroute_path("Salem", "Chennai")