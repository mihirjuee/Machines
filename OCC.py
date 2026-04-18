import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Generator Build-up", layout="wide")
st.title("⚡ DC Shunt Generator: Voltage Build-up & Critical Speed")

# --- PARAMETERS ---
Rf = st.sidebar.slider("Field Resistance (Rf) (Ohms)", 50.0, 300.0, 150.0)
rated_speed = 1500  # Rated speed in RPM
actual_speed = st.sidebar.slider("Actual Speed (RPM)", 500, 2000, 1500)

# Critical speed calculation (simplified: Nc = N * (Rc / Rf))
# For this model, let's assume Rc = 200 Ohms
Rc = 200.0
critical_speed = rated_speed * (Rf / Rc)

# --- MODELING THE OCC ---
If = np.linspace(0, 3, 100)
# OCC varies linearly with speed (E = k * If * Speed)
speed_ratio = actual_speed / rated_speed
E_occ = (250 * If) / (1 + 0.05 * If) * speed_ratio + 2.0

V_field = If * Rf

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(If, E_occ, label=f"OCC at {actual_speed} RPM", linewidth=2)
ax.plot(If, V_field, label=f"Field Resistance Line ({Rf}Ω)", linestyle='--')

ax.set_xlabel("Field Current (If)")
ax.set_ylabel("Generated EMF (V)")
ax.set_title("Voltage Build-up: Effect of Speed")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# --- SPEED CHECK ---
st.divider()
if actual_speed < critical_speed:
    st.error(f"⚠️ Voltage will NOT build up! Actual speed ({actual_speed} RPM) is below Critical Speed ({int(critical_speed)} RPM).")
else:
    st.success(f"✅ Voltage will build up! Actual speed is above the critical speed of {int(critical_speed)} RPM.")

st.markdown("""
### 📘 Understanding Critical Speed
The **Critical Speed** is the minimum speed below which the generator cannot build up its rated voltage.
- If **$N < N_c$**: The resistance line is steeper than the OCC, so there is no point of intersection other than zero.
- If **$N > N_c$**: The resistance line intersects the OCC, allowing the voltage to grow until saturation.
""")
