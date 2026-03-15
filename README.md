GridMind — Autonomous Smart Grid Stability System



GridMind is an AI-driven smart grid monitoring and stabilization system that predicts power grid instability and autonomously takes corrective actions to prevent blackouts.



The system combines machine learning, real-time grid simulation, and a multi-agent architecture to monitor grid conditions, evaluate risk, and dynamically stabilize the network.



📌 Problem



Electricity blackouts impose major economic and social costs in India.



Energy shortages cost ~1.9% of India’s GDP annually



Small and medium businesses lose over $10B every year



Households pay up to 25× the grid electricity price for reliable backup power



Grid inefficiencies cause outages despite sufficient installed capacity



Traditional grid control systems like SCADA are reactive — they detect problems only after instability begins.



GridMind aims to make grid management predictive and autonomous.



🚀 Solution



GridMind predicts instability before faults occur and automatically triggers stabilization actions.



The system performs three key functions:



Predict Grid Instability



Make Autonomous Decisions



Stabilize the Grid



It simulates a Tamil Nadu power grid and demonstrates how AI agents can coordinate to maintain stability.



🧠 System Architecture



GridMind uses a multi-agent architecture orchestrated using LangGraph.



Grid Simulator (Live Telemetry)

&nbsp;       ↓

Prediction Agent (ML Risk Model)

&nbsp;       ↓

Decision Agent (Grid State Evaluation)

&nbsp;       ↓

Self-Healing Agent (Power Rerouting)

&nbsp;       ↓

Prosumer Agent (Demand Response Signals)



Each agent has a specialized responsibility for grid stabilization.



🤖 Agents

Prediction Agent



Uses a trained XGBoost model to estimate grid instability risk.



Input features include:



solar generation



grid demand



EV load



grid frequency



voltage levels



Output:



Risk Score (0 → Stable, 1 → Critical)

Decision Agent



Interprets the predicted risk score and determines grid status.



Risk Score	Grid State

< 0.35	Stable

0.35 – 0.65	Warning

> 0.65	Critical

Self-Healing Agent



If instability occurs, this agent reroutes power across the grid network.



The Tamil Nadu grid is modeled as a graph using NetworkX.



Nodes:



Chennai

Coimbatore

Madurai

Salem

Trichy



Edges represent transmission lines.



The agent calculates the optimal rerouting path to stabilize the system.



Example:



Madurai → Trichy → Chennai

Prosumer Agent



When rerouting is insufficient, the system triggers demand response signals.



Examples:



Increase EV charging price



Incentivize home battery discharge



Adjust solar buyback pricing



This simulates real-world smart grid demand management.



📊 Data Sources



The project integrates multiple datasets to simulate realistic grid behavior.



Smart Grid Stability Dataset



Used to train the ML model.



Contains:



generator response parameters



load characteristics



elasticity coefficients



grid stability indicators



Energy Generation Datasets



Used to simulate renewable variability.



Solar generation dataset



Wind turbine SCADA dataset



AEP hourly electricity demand dataset



Data Processing



The datasets are normalized and scaled to approximate Tamil Nadu grid conditions:



Parameter	Value

Peak Demand	~15 GW

Solar Capacity	~1.4 GW

Wind Capacity	~400 MW

🔴 Live Grid Simulation



Since real SCADA grid data is restricted, GridMind includes a live grid telemetry simulator.



The simulator streams:



demand



solar generation



EV load



frequency



voltage



Agents process this real-time stream and take actions accordingly.



📈 Monitoring \& Evaluation



All agent decisions and system metrics are logged to Excel for analysis.



Stored metrics include:



timestep



demand



solar generation



risk score



grid status



rerouting actions



demand response signals



This ensures traceability and explainability.



🖥️ Frontend Dashboard



The project includes a control-center dashboard for real-time monitoring.



Dashboard components:



Grid health indicators



Power flow visualization



Tamil Nadu zone map



Transmission network topology



Agent decision log



⚙️ Tech Stack



Languages



Python



JavaScript



Libraries



XGBoost



Pandas



NetworkX



LangGraph



Chart.js



Tools



Cursor AI



Jupyter / Python scripts



📂 Project Structure

gridmind/

│

├── data/

│   ├── smart\_grid\_stability\_augmented.csv

│   ├── AEP\_hourly.csv

│   ├── solar\_generation.csv

│   └── wind\_scada.csv

│

├── models/

│   ├── load\_forecaster.pkl

│   └── training\_metrics.xlsx

│

├── src/

│   ├── data\_pipeline.py

│   ├── train\_models.py

│   ├── graph\_topology.py

│   ├── agent.py

│   └── demo\_replay.py

│

├── gridmind\_agents/

│   ├── prediction\_agent.py

│   ├── decision\_agent.py

│   ├── selfheal\_agent.py

│   └── prosumer\_agent.py

│

└── dashboard/

▶️ Running the Project

1 Install dependencies

pip install -r requirements.txt

2 Train the model

python src/train\_models.py

3 Run agent simulation

python gridmind\_agents/run\_agents.py

🌍 Impact



GridMind demonstrates how AI-driven autonomous systems can improve power grid resilience by:



predicting instability early



coordinating automated grid responses



reducing blackout risk



enabling smarter energy management



📜 License



This project is released for educational and research purposes

