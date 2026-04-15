import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Induction Motor Performance", layout="wide")

st.title("⚡ Induction Motor Performance Analysis")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Motor Parameters")

V = st.sidebar.slider("Supply Voltage (Line-to-Line V)", 100, 500, 400)
f = st.sidebar.slider("Frequency (Hz)", 10, 100, 50)
P = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)

R1 = st.sidebar.slider("Stator Resistance R1 (Ω)", 0.01, 5.0, 0.5)
X1 = st.sidebar.slider("Stator Reactance X1 (Ω)", 0.1, 5.0, 1.0)

R2 = st.sidebar.slider("Rotor Resistance R2 (Ω)", 0.01, 5.0, 0.8)
X2 = st.sidebar.slider("Rotor Reactance X2 (Ω)", 0.1, 5.0, 1.2)

Xm = st.sidebar.slider("Magnetizing Reactance Xm (Ω)", 5.0, 100.0, 30.0)

slip_op = st.sidebar.slider("Operating Slip (s)", 0.001, 1.0, 0.05)

# --- CALCULATIONS ---
V_phase = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

# Thevenin Equivalent for Torque Curve Accuracy
V_th = V_phase * (Xm / np.sqrt(R1**2 + (X1 + Xm)**2))
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
R_th = Z_th.real
X_th = Z_th.imag

def calculate_torque(s_val):
    # Standard Torque Equation
    num = 3 * V_th**2 * (R2 / s_val)
    den = omega_s * ((R_th + R2/s_val)**2 + (X_th + X2)**2)
    return num

# Generate Curve Data
s_range = np.linspace(0.001, 1, 500)
T_curve = calculate_torque(s_range)
T_max_val = np.max(T_curve)

# Operating Point
T_operating = calculate_torque(slip_op)

# --- PLOTTING ---
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the curve
ax.plot(s_range, T_curve, color='#1E88E5', lw=2.5, label="Torque-Slip Curve")

# Highlight Operating Point
ax.scatter(slip_op, T_operating, color='red', s=100, zorder=5, label=f"Operating Point (s={slip_op})")
ax.annotate(f"  {T_operating:.1f} Nm", (slip_op, T_operating), fontweight='bold')

# Visual regions
ax.axvspan(0, 0.1, color='green', alpha=0.1, label="Stable Region")
ax.axhline(calculate_torque(1.0), color='orange', ls='--', alpha=0.7, label="Starting Torque")

# Formatting
ax.set_xlabel("Slip (s)")
ax.set_ylabel("Torque (Nm)")
ax.set_title("Induction Motor Torque-Slip Characteristics", fontsize=14)
ax.invert_xaxis()  # Slip 0 (left) to Slip 1 (right) is standard convention
ax.grid(True, which='both', linestyle='--', alpha=0.5)
ax.legend()

st.pyplot(fig)

# --- DASHBOARD ---
# (Keep your existing dashboard metrics code here)
st.subheader("📊 Performance Results")
col1, col2, col3 = st.columns(3)
col1.metric("Synchronous Speed", f"{Ns:.0f} RPM")
col2.metric("Operating Torque", f"{T_operating:.2f} Nm")
col3.metric("Max Torque", f"{T_max_val:.2f} Nm")
