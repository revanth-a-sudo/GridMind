from streaming.grid_simulator import GridSimulator

sim = GridSimulator()

for i in range(20):

    row = sim.simulate()

    print(row)