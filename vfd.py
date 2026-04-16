import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Phasor Diagram", layout="wide")

st.title("⚡ Interactive Phasor Diagram (3-Phase Induction Motor)")

st.markdown("Adjust **Power Factor** and **Load** to visualize phasor changes.")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Controls")

pf = st.sidebar.slider("Power Factor", 0.1, 1.0, 0.8, 0.01)
pf_type = st.sidebar.selectbox("Power Factor Type", ["Lagging", "Leading"])

load = st.sidebar.slider("Load (%)", 0, 150, 100)

# --- CALCULATIONS ---
phi = np.arccos(pf)

if pf_type == "Leading":
    phi = -phi

# Voltage reference
V = 1  # per unit

# Current magnitude depends on load
I_mag = load / 100

# Phasors
V_phasor = V * np.exp(1j * 0)
I_phasor = I_mag * np.exp(-1j * phi)

# --- PLOT ---
fig, ax = plt.subplots(figsize=(6,6))

# Draw axes
ax.axhline(0)
ax.axvline(0)

# Voltage vector
ax.quiver(0, 0, np.real(V_phasor), np.imag(V_phasor),
          angles='xy', scale_units='xy', scale=1, label='Voltage (V)')

# Current vector
ax.quiver(0, 0, np.real(I_phasor), np.imag(I_phasor),
          angles='xy', scale_units='xy', scale=1, label='Current (I)')

# Formatting
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid()
ax.set_title("Phasor Diagram")
ax.legend()

st.pyplot(fig)

# --- DISPLAY VALUES ---
st.subheader("📊 Values")

col1, col2 = st.columns(2)

with col1:
    st.metric("Power Factor", f"{pf:.2f}")

with col2:
    st.metric("Phase Angle (°)", f"{np.degrees(phi):.1f}")

# --- INSIGHT ---
st.info("""
⚡ Voltage is taken as reference.
⚡ Current lags in inductive load (lagging PF).
⚡ Current leads in capacitive load (leading PF).
⚡ Increasing load increases current magnitude.
""")
