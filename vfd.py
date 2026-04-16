import streamlit as st
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="No Load Test", layout="wide")

st.title("⚡ No-Load Test of 3-Phase Induction Motor")

st.markdown("Input measured values from the test and compute losses and current components.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("⚙️ Measured Values")

V = st.sidebar.slider("Line Voltage (V)", 200, 500, 400)
I0 = st.sidebar.slider("No-load Current (A)", 1.0, 20.0, 5.0)
P0 = st.sidebar.slider("Wattmeter Reading (W)", 100, 5000, 800)

# --- CALCULATIONS ---

# Power Factor calculation
pf = P0 / (np.sqrt(3) * V * I0)
pf = min(pf, 1.0)  # limit

phi = np.arccos(pf)

# Current components
Iw = I0 * pf
Im = I0 * np.sin(phi)

# Assume stator resistance
R1 = 1.0  # ohm (can make slider later)

stator_cu_loss = 3 * (I0**2) * R1

# Core + mechanical loss
core_mech_loss = P0 - stator_cu_loss

# --- DISPLAY RESULTS ---
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Power Factor", f"{pf:.3f}")

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

# --- WARNING ---
if core_mech_loss < 0:
    st.warning("⚠️ Invalid readings! Power is too low for given voltage/current.")

# --- INSIGHT ---
st.info("""
⚡ In real experiments:
- Power is measured using wattmeter
- Power factor is calculated
- Most current is magnetizing at no-load
""")
