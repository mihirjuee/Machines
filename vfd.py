import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="SCADA Motor Dashboard", layout="wide")

# --- SESSION STATE ---
if "motor_on" not in st.session_state:
    st.session_state.motor_on = False

# --- HEADER ---
st.title("🖥️ SCADA Dashboard - Induction Motor Control")

# --- SIDEBAR (CONTROL PANEL) ---
with st.sidebar:
    st.header("🎮 Control Panel")

    if st.button("▶ START"):
        st.session_state.motor_on = True

    if st.button("⏹ STOP"):
        st.session_state.motor_on = False

    st.markdown("---")

    freq = st.slider("Frequency (Hz)", 1, 60, 50)
    voltage = st.slider("Voltage (V)", 0, 415, 415)

    load = st.slider("Load (%)", 0, 100, 50)

# --- MOTOR STATUS ---
status_col1, status_col2, status_col3 = st.columns(3)

status_col1.metric("Motor Status", "RUNNING" if st.session_state.motor_on else "STOPPED")
status_col2.metric("Frequency", f"{freq} Hz")
status_col3.metric("Voltage", f"{voltage} V")

st.divider()

# --- REAL-TIME 3-PHASE WAVEFORM ---
st.subheader("⚡ Real-Time 3-Phase Voltage Waveform")

t = np.linspace(0, 0.04, 500)

Va = voltage * np.sin(2 * np.pi * freq * t)
Vb = voltage * np.sin(2 * np.pi * freq * t - 2*np.pi/3)
Vc = voltage * np.sin(2 * np.pi * freq * t + 2*np.pi/3)

fig_wave = go.Figure()
fig_wave.add_trace(go.Scatter(x=t, y=Va, name="Phase A"))
fig_wave.add_trace(go.Scatter(x=t, y=Vb, name="Phase B"))
fig_wave.add_trace(go.Scatter(x=t, y=Vc, name="Phase C"))

fig_wave.update_layout(
    title="3-Phase Voltage",
    xaxis_title="Time (s)",
    yaxis_title="Voltage (V)",
    height=400
)

st.plotly_chart(fig_wave, use_container_width=True)

# --- MOTOR MODEL ---
poles = 4
Ns = 120 * freq / poles

slip = 0.05 + (load / 200) if st.session_state.motor_on else 1
speed = Ns * (1 - slip)

# --- POWER CALCULATIONS ---
input_power = voltage * (load/100) * 10  # simplified
loss_stator = 0.05 * input_power
loss_rotor = 0.07 * input_power
core_loss = 0.03 * input_power

total_loss = loss_stator + loss_rotor + core_loss
output_power = input_power - total_loss

efficiency = (output_power / input_power * 100) if input_power > 0 else 0

# --- SCADA METRICS ---
st.subheader("📊 SCADA Live Parameters")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Speed (RPM)", f"{speed:.0f}")
col2.metric("Input Power (W)", f"{input_power:.0f}")
col3.metric("Output Power (W)", f"{output_power:.0f}")
col4.metric("Efficiency (%)", f"{efficiency:.1f}")

st.divider()

# --- LOSSES BREAKDOWN ---
st.subheader("📉 Losses Breakdown")

labels = ["Stator Loss", "Rotor Loss", "Core Loss"]
values = [loss_stator, loss_rotor, core_loss]

fig_loss = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
fig_loss.update_layout(title="Motor Loss Distribution")

st.plotly_chart(fig_loss, use_container_width=True)

# --- MOTOR ANIMATION ---
st.subheader("🔄 Motor Status")

angle = (speed / max(Ns,1)) * 360 if st.session_state.motor_on else 0

svg_motor = f"""
<svg width="200" height="200" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45" fill="#ddd"/>
    <g transform="rotate({angle} 50 50)">
        <line x1="50" y1="50" x2="50" y2="20" stroke="blue" stroke-width="4"/>
        <line x1="50" y1="50" x2="80" y2="50" stroke="blue" stroke-width="4"/>
        <line x1="50" y1="50" x2="50" y2="80" stroke="blue" stroke-width="4"/>
        <line x1="50" y1="50" x2="20" y2="50" stroke="blue" stroke-width="4"/>
    </g>
</svg>
"""

st.markdown(svg_motor, unsafe_allow_html=True)

# --- AUTO REFRESH (REAL-TIME FEEL) ---
time.sleep(0.5)
st.rerun()
