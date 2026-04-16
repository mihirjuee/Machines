import streamlit as st
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="No Load Test", layout="wide")

st.title("⚡ No-Load Test of 3-Phase Induction Motor")

st.markdown("Simulate the **No-Load Test** and calculate losses and current components.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("⚙️ Input Parameters")

V = st.sidebar.slider("Line Voltage (V)", 200, 500, 400)
I0 = st.sidebar.slider("No-load Current (A)", 1.0, 20.0, 5.0)
pf = st.sidebar.slider("Power Factor (cosφ₀)", 0.1, 1.0, 0.3)

# --- CALCULATIONS ---

# Input Power
P0 = np.sqrt(3) * V * I0 * pf

# Current components
phi = np.arccos(pf)
Iw = I0 * pf            # working component
Im = I0 * np.sin(phi)   # magnetizing component

# Assume stator copper loss (approx)
R1 = 1.0   # ohm (assumed)
stator_cu_loss = 3 * (I0**2) * R1

# Core + mechanical loss
core_mech_loss = P0 - stator_cu_loss

# --- DISPLAY RESULTS ---
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Input Power P₀", f"{P0:.2f} W")

with col2:
    st.metric("Working Current (Iw)", f"{Iw:.2f} A")

with col3:
    st.metric("Magnetizing Current (Im)", f"{Im:.2f} A")

st.subheader("⚡ Loss Analysis")

col4, col5 = st.columns(2)

with col4:
    st.metric("Stator Copper Loss", f"{stator_cu_loss:.2f} W")

with col5:
    st.metric("Core + Mechanical Loss", f"{core_mech_loss:.2f} W")

# --- INSIGHT ---
st.info("""
⚡ At no-load:
- Power factor is low
- Current is mostly magnetizing
- Input power represents core + mechanical losses
""")
