/**
 * GridMind Dashboard – real-time control center UI
 * Updates every 1s with mock API data; drives charts, map, topology, and agent log.
 */

(function () {
  "use strict";

  // ----- Configuration -----
  const UPDATE_INTERVAL_MS = 1000;
  const HISTORY_LENGTH = 30;

  // Topology edges (from backend SelfHealAgent): from → to
  const TOPOLOGY_EDGES = [
    ["Salem", "Chennai"],
    ["Trichy", "Chennai"],
    ["Coimbatore", "Salem"],
    ["Madurai", "Trichy"],
    ["Salem", "Coimbatore"],
  ];

  // Node positions for topology canvas (roughly map-like)
  const NODE_POS = {
    Chennai: { x: 0.85, y: 0.25 },
    Coimbatore: { x: 0.2, y: 0.5 },
    Madurai: { x: 0.5, y: 0.9 },
    Salem: { x: 0.35, y: 0.25 },
    Trichy: { x: 0.7, y: 0.6 },
  };

  // ----- State -----
  let powerChart = null;
  let dataHistory = [];
  let currentData = null;
  /** Action log entries for Excel export: { timeStr, agentName, message } */
  const logEntries = [];

  // ----- DOM refs -----
  const el = {
    timestamp: document.getElementById("timestamp"),
    indicatorFrequency: document.getElementById("indicator-frequency"),
    indicatorVoltage: document.getElementById("indicator-voltage"),
    indicatorRisk: document.getElementById("indicator-risk"),
    indicatorStatus: document.getElementById("indicator-status"),
    chartPowerFlow: document.getElementById("chartPowerFlow"),
    canvasTopology: document.getElementById("canvasTopology"),
    logList: document.getElementById("logList"),
    btnDownloadReport: document.getElementById("btnDownloadReport"),
  };

  /**
   * Generate mock API payload.
   * Returns structure: { solar, demand, ev_load, frequency, voltage, risk, status, reroute?, pricing_signal }.
   */
  function getMockData() {
    const statuses = ["STABLE", "WARNING", "CRITICAL"];
    const r = Math.random();
    let status = "STABLE";
    if (r > 0.7) status = "CRITICAL";
    else if (r > 0.4) status = "WARNING";

    const risk = status === "CRITICAL" ? 0.65 + Math.random() * 0.3
      : status === "WARNING" ? 0.35 + Math.random() * 0.3
      : Math.random() * 0.35;

    const solar = Math.round(200 + Math.random() * 800);
    const demand = Math.round(4000 + Math.random() * 6000);
    const ev_load = Math.round(400 + Math.random() * 800);
    const deficit = Math.max(0, demand + ev_load - solar);

    const frequency = 50 + (Math.random() - 0.5) * 0.15;
    const voltage = 0.95 + Math.random() * 0.1;

    let reroute = null;
    let pricing_signal = "No pricing signal required";
    if (status === "CRITICAL") {
      const paths = [
        ["Salem", "Chennai"],
        ["Trichy", "Chennai"],
        ["Coimbatore", "Salem", "Chennai"],
        ["Madurai", "Trichy", "Chennai"],
      ];
      reroute = paths[Math.floor(Math.random() * paths.length)];
      pricing_signal = "EV charging price increased";
    }

    return {
      solar,
      demand,
      ev_load,
      frequency: Math.round(frequency * 100) / 100,
      voltage: Math.round(voltage * 100) / 100,
      risk: Math.round(risk * 100) / 100,
      status,
      reroute,
      pricing_signal,
      deficit,
    };
  }

  /**
   * Update header timestamp and all health indicator cards.
   */
  function updateHealthIndicators(data) {
    const now = new Date();
    el.timestamp.textContent = now.toTimeString().slice(0, 8);

    el.indicatorFrequency.textContent = data.frequency;
    el.indicatorVoltage.textContent = data.voltage;
    el.indicatorRisk.textContent = data.risk;

    el.indicatorRisk.className = "health-value health-value-risk " +
      (data.risk < 0.35 ? "low" : data.risk < 0.65 ? "medium" : "high");

    el.indicatorStatus.textContent = data.status;
    el.indicatorStatus.className = "health-value health-value-status " + data.status.toLowerCase();
  }

  /**
   * Initialize Chart.js line chart for power flow (solar, demand, ev_load, deficit).
   */
  function initPowerChart() {
    const ctx = el.chartPowerFlow.getContext("2d");
    const bg = "#1e293b";
    const gridColor = "rgba(148, 163, 184, 0.15)";

    powerChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          { label: "Solar", data: [], borderColor: "#22c55e", backgroundColor: "rgba(34, 197, 94, 0.1)", fill: true, tension: 0.3 },
          { label: "Demand", data: [], borderColor: "#3b82f6", backgroundColor: "rgba(59, 130, 246, 0.1)", fill: true, tension: 0.3 },
          { label: "EV Load", data: [], borderColor: "#eab308", backgroundColor: "rgba(234, 179, 8, 0.1)", fill: true, tension: 0.3 },
          { label: "Predicted Deficit", data: [], borderColor: "#ef4444", backgroundColor: "rgba(239, 68, 68, 0.1)", fill: true, tension: 0.3 },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: "#94a3b8", font: { size: 11 } } },
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: "#94a3b8", maxTicksLimit: 8 },
          },
          y: {
            grid: { color: gridColor },
            ticks: { color: "#94a3b8" },
            beginAtZero: true,
          },
        },
      },
    });
  }

  /**
   * Push new reading into history and update chart.
   */
  function updatePowerChart(data) {
    if (!powerChart) return;
    const i = dataHistory.length;
    dataHistory.push({ t: i, ...data });
    if (dataHistory.length > HISTORY_LENGTH) dataHistory.shift();

    const labels = dataHistory.map((_, j) => j.toString());
    powerChart.data.labels = labels;
    powerChart.data.datasets[0].data = dataHistory.map((d) => d.solar);
    powerChart.data.datasets[1].data = dataHistory.map((d) => d.demand);
    powerChart.data.datasets[2].data = dataHistory.map((d) => d.ev_load);
    powerChart.data.datasets[3].data = dataHistory.map((d) => d.deficit);
    powerChart.update("none");
  }

  /**
   * Draw topology graph on canvas; highlight reroute path if present.
   */
  function drawTopology(data) {
    const canvas = el.canvasTopology;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;
    const padding = 28;

    ctx.clearRect(0, 0, w, h);

    const x = (px) => padding + px * (w - 2 * padding);
    const y = (py) => padding + py * (h - 2 * padding);

    const rerouteSet = new Set((data.reroute || []).flat());
    const isRerouteEdge = (from, to) => {
      if (!data.reroute || data.reroute.length < 2) return false;
      for (let i = 0; i < data.reroute.length - 1; i++) {
        if (data.reroute[i] === from && data.reroute[i + 1] === to) return true;
      }
      return false;
    };

    // Draw edges
    TOPOLOGY_EDGES.forEach(([from, to]) => {
      const fromPos = NODE_POS[from];
      const toPos = NODE_POS[to];
      if (!fromPos || !toPos) return;
      const active = isRerouteEdge(from, to);
      ctx.strokeStyle = active ? "#3b82f6" : "rgba(148, 163, 184, 0.4)";
      ctx.lineWidth = active ? 3 : 1;
      ctx.beginPath();
      ctx.moveTo(x(fromPos.x), y(fromPos.y));
      ctx.lineTo(x(toPos.x), y(toPos.y));
      ctx.stroke();
    });

    // Draw nodes
    const statusColor = data.status === "CRITICAL" ? "#ef4444" : data.status === "WARNING" ? "#eab308" : "#22c55e";
    Object.keys(NODE_POS).forEach((name) => {
      const pos = NODE_POS[name];
      const px = x(pos.x);
      const py = y(pos.y);
      const inReroute = rerouteSet.has(name);
      ctx.fillStyle = inReroute ? "#3b82f6" : statusColor;
      ctx.strokeStyle = inReroute ? "#3b82f6" : "rgba(148, 163, 184, 0.6)";
      ctx.lineWidth = inReroute ? 2 : 1;
      ctx.beginPath();
      ctx.arc(px, py, 20, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = "#0f172a";
      ctx.font = "bold 10px system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(name, px, py);
    });
  }

  /**
   * Append one entry to the agent decision log and store for export.
   */
  function appendLog(timeStr, agentName, message) {
    logEntries.push({ timeStr, agentName, message });

    const placeholder = el.logList.querySelector(".log-placeholder");
    if (placeholder) placeholder.remove();

    const li = document.createElement("li");
    li.className = "log-item";
    li.innerHTML = `<span class="log-time">[${timeStr}]</span><span class="log-agent">${agentName}</span> → <span class="log-message">${escapeHtml(message)}</span>`;
    el.logList.appendChild(li);
    el.logList.scrollTop = el.logList.scrollHeight;

    // Keep only last 80 entries in DOM
    while (el.logList.children.length > 80) el.logList.removeChild(el.logList.firstChild);
  }

  /**
   * Build CSV from action log and trigger download (Excel-friendly).
   */
  function downloadActionLogReport() {
    const headers = "Timestamp,Agent,Action / Message";
    const rows = logEntries.map((e) => {
      const time = e.timeStr;
      const agent = e.agentName;
      const msg = String(e.message).replace(/"/g, '""');
      return `"${time}","${agent}","${msg}"`;
    });
    const csv = [headers, ...rows].join("\r\n");
    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "GridMind_action_log_" + new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "-").replace("--", "_") + ".csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  /**
   * Emit agent log entries for the current data tick.
   */
  function updateAgentLog(data) {
    const timeStr = new Date().toTimeString().slice(0, 8);
    appendLog(timeStr, "Prediction Agent", `Risk Score: ${data.risk}`);
    appendLog(timeStr, "Decision Agent", `Status: ${data.status}`);
    if (data.status === "CRITICAL" && data.reroute && data.reroute.length >= 2) {
      appendLog(timeStr, "SelfHeal Agent", `Rerouting ${data.reroute.join(" → ")}`);
    } else {
      appendLog(timeStr, "SelfHeal Agent", "No reroute required");
    }
    appendLog(timeStr, "Prosumer Agent", data.pricing_signal);
  }

  /**
   * One tick: fetch mock data, update all panels.
   */
  function tick() {
    currentData = getMockData();
    updateHealthIndicators(currentData);
    updatePowerChart(currentData);
    drawTopology(currentData);
    updateAgentLog(currentData);
  }

  // ----- Init & loop -----
  function init() {
    initPowerChart();
    if (el.btnDownloadReport) {
      el.btnDownloadReport.addEventListener("click", downloadActionLogReport);
    }
    tick();
    setInterval(tick, UPDATE_INTERVAL_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
