import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# --- PAGE CONFIG ---
st.set_page_config(page_title="Induction Motor Load Analysis", layout="wide")

st.title("⚡ Induction Motor Performance: Load-Driven Analysis")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Motor Parameters")
V = st.sidebar.slider("Supply Voltage (L-L V)", 100, 500, 400)
f = st.sidebar.slider("Frequency (Hz)", 10, 100, 50)
P = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)

R1 = st.sidebar.slider("Stator Resistance R1 (Ω)", 0.01, 5.0, 0.5)
X1 = st.sidebar.slider("Stator Reactance X1 (Ω)", 0.1, 5.0, 1.0)
R2 = st.sidebar.slider("Rotor Resistance R2 (Ω)", 0.01, 5.0, 0.8)
X2 = st.sidebar.slider("Rotor Reactance X2 (Ω)", 0.1, 5.0, 1.2)
Xm = st.sidebar.slider("Magnetizing Reactance Xm (Ω)", 5.0, 100.0, 30.0)

# --- CALCULATIONS SETUP ---
V_phase = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

# Thevenin Constants
V_th = V_phase * (Xm / np.sqrt(R1**2 + (X1 + Xm)**2))
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
R_th, X_th = Z_th.real, Z_th.imag

def get_motor_metrics(s):
    # Avoid division by zero
    s = np.clip(s, 0.0001, 1.0)
    denom_t = omega_s * ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * R2 / s) / denom_t
    
    Zr = (R2/s) + 1j*X2
    Zp = (1j*Xm * Zr) / (1j*Xm + Zr)
    I1 = V_phase / abs(R1 + 1j*X1 + Zp)
    return torque, I1

# Calculate Max Torque to set the slider limit
s_range_temp = np.linspace(0.001, 1, 500)
T_range_temp, _ = get_motor_metrics(s_range_temp)
max_torque_possible = float(np.max(T_range_temp))

st.sidebar.divider()
st.sidebar.header("⚖️ Applied Load")
load_torque = st.sidebar.slider("Applied Load Torque (Nm)", 0.0, round(max_torque_possible, 1), 50.0)

# --- FIND OPERATING SLIP ---
# We solve: get_motor_metrics(s)[0] - load_torque = 0
def solve_slip(s):
    t, _ = get_motor_metrics(s)
    return t - load_torque

# Search in the stable region (0 to slip at max torque)
operating_slip = fsolve(solve_slip, x0=0.02)[0]
operating_torque, operating_current = get_motor_metrics(operating_slip)

# --- PLOTTING ---
s_range = np.linspace(0.001, 1.0, 500)
T_curve, I_curve = get_motor_metrics(s_range)

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

# Plot Torque & Current
ax1.plot(s_range, T_curve, 'r-', lw=2, label="Motor Torque Output")
ax2.plot(s_range, I_curve, 'b--', lw=1.5, label="Stator Current")

# Plot Load Line
ax1.axhline(load_torque, color='green', ls=':', label="Load Torque Line")

# Operating Point Marker
ax1.scatter(operating_slip, operating_torque, color='black', s=80, zorder=5)
ax1.annotate(f'Operating Point\ns={operating_slip:.4f}', (operating_slip, operating_torque), 
             xytext=(operating_slip+0.1, operating_torque+20), 
             arrowprops=dict(arrowstyle='->', color='black'))

# Formatting (Textbook Style: 1 to 0)
ax1.set_xlim(1.0, 0)
ax1.set_xlabel("Slip ($s$)", fontsize=12)
ax1.set_ylabel("Torque (Nm)", color='r', fontsize=12)
ax1.tick_params(axis='y', labelcolor='r')
ax2.set_ylabel("Current (A)", color='b', fontsize=12)
ax2.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.set_title("Load-Dependent Performance Characteristics", fontsize=14)

st.pyplot(fig)

# --- DASHBOARD ---
st.subheader("📊 Performance Results")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Sync Speed", f"{Ns:.0f} RPM")
c2.metric("Resulting Slip", f"{operating_slip:.4f}")
c3.metric("Rotor Speed", f"{Ns*(1-operating_slip):.1f} RPM")
c4.metric("Current", f"{operating_current:.2f} A")

# Power & Efficiency
# Pin = 3 * V_ph * I_stator * cos(phi)
Zr_op = (R2/operating_slip) + 1j*X2
Zp_op = (1j*Xm * Zr_op) / (1j*Xm + Zr_op)
Z_total = R1 + 1j*X1 + Zp_op
pf = np.cos(np.angle(Z_total))
Pin = 3 * V_phase * operating_current * pf
Pout = operating_torque * (omega_s * (1 - operating_slip))
eff = (Pout / Pin) * 100 if Pin > 0 else 0

c5, c6, c7, c8 = st.columns(4)
c5.metric("Input Power", f"{Pin/1000:.2f} kW")
c6.metric("Output Power", f"{Pout/1000:.2f} kW")
c7.metric("Efficiency", f"{eff:.1f} %")
c8.metric("Power Factor", f"{pf:.2f}")
