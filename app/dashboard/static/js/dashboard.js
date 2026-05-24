const $ = (id) => document.getElementById(id);

function setText(id, value) {
  const node = $(id);
  if (node) node.textContent = value;
}

function renderAlerts(alerts, containerId) {
  const container = $(containerId);
  if (!container) return;
  if (!alerts || alerts.length === 0) {
    container.innerHTML = '<div class="empty">No active alerts</div>';
    return;
  }

  container.innerHTML = alerts.map((alert) => `
    <article class="alert ${alert.severity}">
      <div>
        <strong>${alert.title}</strong>
        <span>${alert.message}</span>
        <small>${new Date(alert.created_at).toLocaleString()} | ${alert.bed_id}</small>
      </div>
      ${alert.acknowledged ? '<em>Acknowledged</em>' : `<button data-alert="${alert.id}">Ack</button>`}
    </article>
  `).join('');

  container.querySelectorAll('button[data-alert]').forEach((button) => {
    button.addEventListener('click', async () => {
      await fetch(`/api/alerts/${button.dataset.alert}/acknowledge`, { method: 'POST' });
      loadAlerts();
    });
  });
}

function updateTelemetry(payload) {
  setText('spo2', `${payload.spo2 ?? '--'}%`);
  setText('heartRate', payload.heart_rate ?? '--');
  setText('fps', payload.fps ?? '--');
  setText('runtime', payload.pipeline?.execution_mode ?? 'cpu-demo');
  setText('patientVisible', payload.patient_visible ? 'Yes' : 'No');
  setText('fallState', payload.fall_detected ? 'Critical' : 'Normal');
  setText('source', payload.source ?? '--');
  setText('updatedAt', payload.updated_at ? new Date(payload.updated_at).toLocaleTimeString() : '--');
  renderAlerts(payload.active_alerts, 'alertsList');

  const banner = $('criticalBanner');
  if (banner) banner.classList.toggle('hidden', payload.severity !== 'critical');
}

async function loadStatus() {
  try {
    const response = await fetch('/api/monitoring/status');
    updateTelemetry(await response.json());
  } catch (error) {
    console.warn(error);
  }
}

async function loadAlerts() {
  try {
    const response = await fetch('/api/alerts');
    const data = await response.json();
    renderAlerts(data.alerts, 'alertsLog');
    renderAlerts(data.alerts.slice(0, 5), 'alertsList');
  } catch (error) {
    console.warn(error);
  }
}

function wireSourceButtons() {
  const demo = $('demoSource');
  const webcam = $('webcamSource');
  if (demo) demo.addEventListener('click', () => fetch('/api/monitoring/source/demo', { method: 'POST' }));
  if (webcam) webcam.addEventListener('click', () => fetch('/api/monitoring/source/webcam', { method: 'POST' }));
}

function connectSocket() {
  if (!('WebSocket' in window)) return;
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const socket = new WebSocket(`${protocol}://${window.location.host}/ws`);
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === 'telemetry') updateTelemetry(message.payload);
  };
}

wireSourceButtons();
connectSocket();
loadStatus();
loadAlerts();
setInterval(loadAlerts, 5000);
