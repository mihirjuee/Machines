import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Advanced VFD Motor Control Lab", layout="wide")

# --- SESSION STATE ---
if "motor_on" not in st.session_state:
    st.session_state.motor_on = False

# --- HEADER ---
st.title("⚡ Advanced VFD Controlled Induction Motor Lab")
st.markdown("Simulate **industrial motor control panel + V/f control + torque-speed characteristics**")

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.header("🎮 Control Panel")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ START"):
            st.session_state.motor_on = True
    with col2:
        if st.button("⏹ STOP"):
            st.session_state.motor_on = False

    if st.button("🔄 RESET"):
        st.session_state.motor_on = False

    st.markdown("---")

    st.header("⚡ VFD Control")

    freq = st.slider("Frequency (Hz)", 1, 60, 50)
    v_base = st.number_input("Base Voltage (V)", value=415)

    st.markdown("---")
    st.header("⚙️ Motor Parameters")

    poles = st.selectbox("Poles", [2, 4, 6, 8], index=1)
    R1 = st.number_input("Stator Resistance R1 (Ω)", value=0.5)
    R2 = st.number_input("Rotor Resistance R2 (Ω)", value=0.4)
    X1 = st.number_input("Stator Reactance X1 (Ω)", value=1.2)
    X2 = st.number_input("Rotor Reactance X2 (Ω)", value=1.0)

# --- V/f CONTROL ---
V = (freq / 50) * v_base if freq <= 50 else v_base

# --- SPEED CALCULATIONS ---
Ns = 120 * freq / poles  # synchronous speed

# --- TORQUE-SLIP MODEL ---
slip = np.linspace(0.001, 1, 200)

# Avoid division by zero
den = (R2/slip)**2 + (X1 + X2)**2
torque = (V**2 * (R2/slip)) / den

# Normalize torque
torque = torque / max(torque)

# --- OPERATING POINT ---
load_slip = 0.05 if st.session_state.motor_on else 1
speed = Ns * (1 - load_slip)
torque_op = np.interp(load_slip, slip, torque)

# --- STATUS ---
st.subheader("⚙️ System Status")

if not st.session_state.motor_on:
    st.error("🔴 Motor OFF")
else:
    st.success("🟢 Motor Running (VFD Controlled)")

# --- GAUGES ---
def gauge(val, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={'text': title},
        gauge={'axis': {'range': [0, max(1, val*1.5)]}}
    ))
    fig.update_layout(height=250)
    return fig

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(gauge(V, "Voltage (V)"), use_container_width=True)

with col2:
    st.plotly_chart(gauge(freq, "Frequency (Hz)"), use_container_width=True)

with col3:
    st.plotly_chart(gauge(speed, "Speed (RPM)"), use_container_width=True)

# --- MOTOR ANIMATION ---
st.subheader("🔄 Motor Rotation")

angle = (speed / max(1, Ns)) * 360 if st.session_state.motor_on else 0

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

# --- TORQUE-SPEED CURVE ---
st.subheader("📊 Torque-Speed Characteristic")

speed_curve = Ns * (1 - slip)

fig, ax = plt.subplots()
ax.plot(speed_curve, torque, label="Torque Curve")
ax.scatter(speed, torque_op, label="Operating Point")
ax.set_xlabel("Speed (RPM)")
ax.set_ylabel("Torque (p.u.)")
ax.set_title("Torque-Speed Curve")
ax.legend()
ax.grid()

st.pyplot(fig)

# --- RESULTS ---
st.subheader("📊 Results")

c1, c2, c3 = st.columns(3)

c1.metric("Synchronous Speed", f"{Ns:.0f} RPM")
c2.metric("Rotor Speed", f"{speed:.0f} RPM")
c3.metric("Torque (p.u.)", f"{torque_op:.2f}")

# --- INFO ---
st.info("""
⚡ **V/f Control Principle:**
- Voltage is proportional to frequency
- Maintains constant flux
- Ensures smooth speed control

📊 **Torque-Speed Curve:**
- High torque at low speed
- Peak torque (breakdown torque)
- Stable operating region near synchronous speed
""")
