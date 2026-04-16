import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Learn EE - Motor Lab", layout="wide")

# --- SESSION STATE (START/STOP) ---
if "motor_on" not in st.session_state:
    st.session_state.motor_on = False

# --- HEADER ---
st.title("⚡ 3-Phase Induction Motor Virtual Lab")
st.markdown("Control, simulate faults, and observe real-time motor behavior.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎛️ Control Panel")

    if st.button("▶️ START"):
        st.session_state.motor_on = True

    if st.button("⏹️ STOP"):
        st.session_state.motor_on = False

    st.markdown("---")

    v_input = st.slider("Supply Voltage (V)", 0, 480, 415)
    load = st.slider("Load (%)", 0, 150, 50)

    st.markdown("---")
    st.header("⚡ Fault Simulation")

    fault = st.selectbox(
        "Select Fault",
        ["Normal", "Single Phasing", "Voltage Unbalance"]
    )

# --- MACHINE PARAMETERS ---
Rc = 1000
Xm = 120

# --- LOGIC ---
if st.session_state.motor_on and v_input > 0:

    v_phase = v_input / np.sqrt(3)

    i_core = v_phase / Rc
    i_mag = v_phase / Xm
    i = np.sqrt(i_core**2 + i_mag**2)

    # Base power
    p = 3 * (i_core**2) * Rc

    # Apply load effect
    p = p * (1 + load/100)

    # --- FAULT CONDITIONS ---
    if fault == "Single Phasing":
        i = i * 1.8
        p = p * 0.5

    elif fault == "Voltage Unbalance":
        i = i * 1.5
        p = p * 0.8

    # Efficiency (approx)
    output_power = p * (load / 100)
    efficiency = (output_power / p) if p > 0 else 0

else:
    i = p = efficiency = 0

# --- STATUS ---
st.subheader("⚙️ System Status")

if not st.session_state.motor_on:
    st.error("🔴 Motor OFF")
elif fault != "Normal":
    st.warning(f"⚠️ Running under fault: {fault}")
else:
    st.success("🟢 Motor Running Normally")

# --- GAUGE FUNCTION ---
def gauge(val, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={'text': title},
        gauge={'axis': {'range': [0, max(1, val*1.5)]}}
    ))
    fig.update_layout(height=250)
    return fig

# --- DISPLAY ---
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(gauge(v_input, "Voltage (V)"), use_container_width=True)

with col2:
    st.plotly_chart(gauge(i, "Current (A)"), use_container_width=True)

with col3:
    st.plotly_chart(gauge(p, "Power (W)"), use_container_width=True)

# --- MOTOR ANIMATION ---
st.subheader("🔄 Motor Animation")

speed = (v_input / 480) * 360 if st.session_state.motor_on else 0

svg_motor = f"""
<svg width="200" height="200" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45" fill="#ddd"/>
    <g transform="rotate({speed} 50 50)">
        <line x1="50" y1="50" x2="50" y2="20" stroke="blue" stroke-width="4"/>
        <line x1="50" y1="50" x2="80" y2="50" stroke="blue" stroke-width="4"/>
        <line x1="50" y1="50" x2="50" y2="80" stroke="blue" stroke-width="4"/>
        <line x1="50" y1="50" x2="20" y2="50" stroke="blue" stroke-width="4"/>
    </g>
</svg>
"""

st.markdown(svg_motor, unsafe_allow_html=True)

# --- PERFORMANCE GRAPH ---
st.subheader("📉 Performance Curve")

voltages = np.linspace(0, 480, 50)
currents = []

for v in voltages:
    vp = v / np.sqrt(3)
    if vp > 0:
        ic = vp / Rc
        im = vp / Xm
        currents.append(np.sqrt(ic**2 + im**2))
    else:
        currents.append(0)

fig, ax = plt.subplots()
ax.plot(voltages, currents)
ax.set_xlabel("Voltage (V)")
ax.set_ylabel("Current (A)")
ax.set_title("Voltage vs Current")
ax.grid()

st.pyplot(fig)

# --- RESULTS ---
st.subheader("📊 Results")

c1, c2, c3 = st.columns(3)

c1.metric("Current", f"{i:.2f} A")
c2.metric("Power", f"{p:.2f} W")
c3.metric("Efficiency", f"{efficiency*100:.1f} %")

# --- TABLE ---
st.subheader("📋 Data Log")

st.table({
    "Voltage (V)": [v_input],
    "Current (A)": [round(i, 2)],
    "Power (W)": [round(p, 2)],
    "Efficiency (%)": [round(efficiency*100, 2)]
})

# --- FOOTER ---
st.info("⚡ Advanced Induction Motor Virtual Lab with Fault Simulation")
