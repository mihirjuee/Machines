import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Voltage Build-up Simulation", layout="wide")
st.title("⚡ DC Shunt Generator: Voltage Build-up")

# --- PARAMETERS ---
st.sidebar.header("Generator Settings")
Rf = st.sidebar.slider("Field Resistance (Ohms)", 50.0, 200.0, 100.0)
residual_v = st.sidebar.slider("Residual Voltage (V)", 1.0, 10.0, 5.0)
speed_factor = st.sidebar.slider("Speed Ratio (Actual/Rated)", 0.5, 1.2, 1.0)

# --- MODELING THE OCC (Saturation Curve) ---
# We use a simple saturation model: E = (k * If) / (1 + b * If)
k = 250.0
b = 0.05

If = np.linspace(0, 3, 100)
E_occ = (k * If) / (1 + b * If) * speed_factor + residual_v

# --- SIMULATION ---
# Calculate the resistance line
V_field = If * Rf

# Find intersection point (Voltage Build-up point)
diff = E_occ - V_field
idx = np.where(diff < 0)[0][0] if np.any(diff < 0) else -1

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(If, E_occ, label="OCC (Saturation Curve)", linewidth=2)
ax.plot(If, V_field, label=f"Field Resistance Line (Rf={Rf}Ω)", linestyle='--')

if idx != -1:
    ax.plot(If[idx], E_occ[idx], 'ro', label=f"Final Voltage: {E_occ[idx]:.1f}V")

ax.set_xlabel("Field Current (If)")
ax.set_ylabel("Generated EMF (V)")
ax.set_title("Voltage Build-up Process in DC Shunt Generator")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# --- THEORY ---
st.divider()
st.subheader("📘 Key Conditions for Build-up")
st.markdown(""""
1.  **Residual Magnetism:** The generator must have some initial magnetism.
2.  **Field Connection:** The field winding must be connected such that the field current **aids** the residual flux.
3.  **Critical Resistance:** The field resistance ($R_f$) must be **less than** the critical resistance ($R_c$). If $R_f > R_c$, the resistance line will not intersect the OCC, and voltage will not build up.
4.  **Speed of Generator:** The speed of the prime mover must be greater than the critical speed, which is the minimum speed below which the generator cannot build up voltage.
            )

