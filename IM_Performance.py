import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# --- PAGE CONFIG ---
st.set_page_config(page_title="IM Performance Analysis", layout="wide")

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

# Thevenin Constants
V_th = V_phase * (Xm / np.sqrt(R1**2 + (X1 + Xm)**2))
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
R_th, X_th = Z_th.real, Z_th.imag

def get_motor_metrics(s):
    # Torque Equation (Thevenin)
    denom_t = omega_s * ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * R2 / s) / denom_t
    
    # Current Equation
    Zr = (R2/s) + 1j*X2
    Zp = (1j*Xm * Zr) / (1j*Xm + Zr)
    I1 = V_phase / abs(R1 + 1j*X1 + Zp)
    
    return torque, I1

# Generate Curve Data
s_range = np.linspace(0.001, 1.0, 500)
T_curve, I_curve = get_motor_metrics(s_range)
T_op, I_op = get_motor_metrics(slip_op)

# --- THE PLOT ---
st.subheader("📈 Torque & Current vs. Slip")
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

# Plot Torque (Textbook Curve)
ax1.plot(s_range, T_curve, 'r-', lw=2, label="Torque")
ax1.set_xlabel("Slip (s)")
ax1.set_ylabel("Torque (Nm)", color='r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.grid(True, which='both', linestyle=':', alpha=0.5)

# Plot Current
ax2.plot(s_range, I_curve, 'b--', lw=1.5, label="Stator Current")
ax2.set_ylabel("Current (A)", color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Marker for Operating Point
ax1.scatter(slip_op, T_op, color='black', s=50, zorder=5)
ax1.annotate(f'Operating Point\n{T_op:.1f} Nm', (slip_op, T_op), 
             xytext=(slip_op+0.1, T_op+20), arrowprops=dict(arrowstyle='->'))

st.pyplot(fig)

# --- PERFORMANCE DASHBOARD ---
st.subheader("📊 Performance Results")
col1, col2, col3 = st.columns(3)
col1.metric("Sync Speed", f"{Ns:.0f} RPM")
col2.metric("Operating Torque", f"{T_op:.1f} Nm")
col3.metric("Stator Current", f"{I_op:.2f} A")

# Power Calculations for Metrics
Pag = T_op * omega_s
Pm = Pag * (1 - slip_op)
Pin = 3 * V_phase * I_op * np.cos(np.angle(V_phase/I_op)) # Simplified PF
eff = (Pm / Pin) * 100 if Pin > 0 else 0

col4, col5, col6 = st.columns(3)
col4.metric("Output Power", f"{Pm/1000:.2f} kW")
col5.metric("Efficiency", f"{eff:.1f} %")
col6.metric("Max Torque", f"{max(T_curve):.1f} Nm")
