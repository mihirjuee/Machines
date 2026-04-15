import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="IM Performance Pro", layout="wide")

# --- CALCULATIONS ---
V_phase = V / np.sqrt(3)  # RMS Phase Voltage
w_s = (2 * np.pi * Ns) / 60  # Sync angular velocity

# 1. Thevenin Equivalent (The "Textbook" Way)
V_th = V_phase * (Xm / np.sqrt(R1**2 + (X1 + Xm)**2))
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
R_th, X_th = Z_th.real, Z_th.imag

# 2. Define Torque and Current Functions
def get_motor_data(s_val):
    # Torque Equation: T = (3 * Vth^2 * R2/s) / [w_s * ((Rth + R2/s)^2 + (Xth + X2)^2)]
    denom_t = w_s * ((R_th + R2/s_val)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * R2 / s_val) / denom_t
    
    # Current Equation (Stator Current)
    Z_rotor = (R2 / s_val) + 1j * X2
    Z_parallel = (1j * Xm * Z_rotor) / (1j * Xm + Z_rotor)
    current = V_phase / abs(R1 + 1j * X1 + Z_parallel)
    
    return torque, current

# Generate Data
s_plot = np.linspace(0.001, 1, 500)
T_plot, I_plot = get_motor_data(s_plot)
T_op, I_op = get_motor_data(slip)

# --- THE PLOT ---
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx() # Secondary axis for Current

# Plot Torque
ax1.plot(s_plot, T_plot, 'r-', lw=2, label="Torque (Nm)")
ax1.set_ylabel("Torque (Nm)", color='r', fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='r')

# Plot Current
ax2.plot(s_plot, I_plot, 'b--', lw=1.5, label="Stator Current (A)")
ax2.set_ylabel("Current (A)", color='b', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='b')

# Operating Point
ax1.scatter(slip, T_op, color='black', zorder=5)
ax1.annotate(f'Operating Point\n{T_op:.1f} Nm', xy=(slip, T_op), xytext=(slip+0.1, T_op+10),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

# Formatting
ax1.set_title("Textbook Induction Motor Characteristics", fontsize=14)
ax1.set_xlabel("Slip (s)", fontsize=12)
ax1.grid(True, which='both', linestyle=':', alpha=0.5)
ax1.set_xlim(0, 1)

st.pyplot(fig)
