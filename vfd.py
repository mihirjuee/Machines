import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="VFD Simulation", layout="wide")

st.title("⚡ Induction Motor VFD Simulation (Speed Control)")

st.markdown("Control motor using **speed input** and observe **torque behavior**.")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Motor Parameters")

f_rated = st.sidebar.slider("Rated Frequency (Hz)", 40, 60, 50)
V_rated = st.sidebar.slider("Rated Voltage (V)", 200, 500, 400)
poles = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)

# Frequency range
f = np.linspace(5, f_rated, 100)

# Synchronous speed
Ns = (120 * f) / poles  # RPM

# --- USER SPEED INPUT ---
N_input = st.sidebar.slider("Set Motor Speed (RPM)", 100, int(max(Ns)), 1400)

# --- CALCULATE SLIP ---
# Using rated frequency synchronous speed for reference
Ns_rated = (120 * f_rated) / poles
slip = (Ns_rated - N_input) / Ns_rated

# Limit slip
slip = max(0.001, min(slip, 1))

# --- V/f CONTROL ---
V = V_rated * (f / f_rated)

# --- TORQUE MODEL ---
T = (V**2 / (f**2 + 1e-6)) * slip
T = T / np.max(T)

# --- ACTUAL SPEED CURVE ---
N_actual = Ns * (1 - slip)

# --- PLOTS ---
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(f, N_actual, label="Motor Speed")
    ax1.axhline(N_input, linestyle="--", label="Selected Speed")
    ax1.set_title("Speed vs Frequency")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Speed (RPM)")
    ax1.grid()
    ax1.legend()
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(f, T)
    ax2.set_title("Torque vs Frequency")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Torque (pu)")
    ax2.grid()
    st.pyplot(fig2)

# --- METRICS ---
st.subheader("📊 Key Results")

col3, col4 = st.columns(2)

with col3:
    st.metric("Calculated Slip", f"{slip:.3f}")

with col4:
    st.metric("Rated Synchronous Speed", f"{Ns_rated:.0f} RPM")

# --- INSIGHT ---
st.info("""
⚡ Speed control is achieved by adjusting frequency using VFD.
Slip is automatically adjusted based on load and selected speed.
""")
