import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="VFD Simulator - Induction Motor", layout="wide")

# --- TITLE ---
st.title("⚡ Variable Frequency Drive (VFD) Simulation")
st.markdown("Control motor **speed using frequency** and observe torque behavior.")

# --- SIDEBAR ---
st.sidebar.header("🎛️ VFD Control")

f = st.sidebar.slider("Frequency (Hz)", 1, 60, 50)
poles = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
rated_speed = st.sidebar.number_input("Rated Speed (RPM)", value=1440)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Load Control")

load = st.sidebar.slider("Load Torque (%)", 0, 150, 50)

# --- CALCULATIONS ---

# Synchronous speed
Ns = 120 * f / poles

# Assume small slip for realism
slip = 0.04 + (load / 100) * 0.05

# Rotor speed
N = Ns * (1 - slip)

# Torque (simplified model)
torque = load * (f / 50)

# --- DISPLAY VALUES ---
st.subheader("📊 Motor Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Synchronous Speed (RPM)", f"{Ns:.0f}")

with col2:
    st.metric("Rotor Speed (RPM)", f"{N:.0f}")

with col3:
    st.metric("Torque (Relative)", f"{torque:.1f} %")

# --- GRAPH: SPEED VS FREQUENCY ---
freq_range = np.linspace(1, 60, 100)
Ns_range = 120 * freq_range / poles
speed_range = Ns_range * (1 - slip)

fig1, ax1 = plt.subplots()
ax1.plot(freq_range, speed_range)
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Speed (RPM)")
ax1.set_title("Speed vs Frequency")
ax1.grid()

st.pyplot(fig1)

# --- GRAPH: TORQUE VS SPEED ---
speed_vals = np.linspace(0.1, Ns, 100)
slip_vals = (Ns - speed_vals) / Ns

# Simplified torque-slip relation
T = (slip_vals) / (0.1 + slip_vals**2)

fig2, ax2 = plt.subplots()
ax2.plot(speed_vals, T)
ax2.set_xlabel("Speed (RPM)")
ax2.set_ylabel("Torque")
ax2.set_title("Torque vs Speed Characteristic")
ax2.grid()

st.pyplot(fig2)

# --- INFO SECTION ---
st.markdown("---")

st.markdown("""
### 🔍 Observations:

- Increasing **frequency** increases motor **speed**
- Torque remains nearly constant in V/f control
- At low frequency, torque reduces due to voltage drop
- Slip increases with load

### ⚙️ Applications of VFD:

- Energy saving
- Soft starting of motors
- Speed control in industries
""")

# --- FOOTER ---
st.info("⚡ This simulation demonstrates basic VFD control of a 3-phase induction motor.")
