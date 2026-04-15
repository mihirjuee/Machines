import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fminbound

# --- PAGE CONFIG ---
st.set_page_config(page_title="Induction Motor Load Analysis", page_icon="⚡", layout="wide")

# --- HEADER WITH LOGO ---
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("logo.png", width=100) 
    except:
        st.header("⚡")

with col2:
    st.title("Induction Motor Performance: Load-Driven Analysis")

st.divider()

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
    s = np.clip(s, 0.0001, 1.0)
    denom_t = omega_s * ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * R2 / s) / denom_t
    
    Zr = (R2/s) + 1j*X2
    Zp = (1j*Xm * Zr) / (1j*Xm + Zr)
    I1 = V_phase / abs(R1 + 1j*X1 + Zp)
    return torque, I1

# Pre-calculate curve to find breakdown slip
s_range_calc = np.linspace(0.0001, 1.0, 500)
T_range_calc, _ = get_motor_metrics(s_range_calc)
max_torque_possible = float(np.max(T_range_calc))
s_at_max_t = s_range_calc[np.argmax(T_range_calc)]

st.sidebar.divider()
st.sidebar.header("⚖️ Applied Load")
# Cap load torque to breakdown torque - small margin to ensure stability
load_torque = st.sidebar.slider("Applied Load Torque (Nm)", 0.0, round(max_torque_possible - 0.1, 1), 50.0)

# --- FIND OPERATING SLIP (STABLE REGION ONLY) ---
def objective_func(s):
    t, _ = get_motor_metrics(s)
    return abs(t - (load_torque + 0.05)) # Adding tiny friction offset for no-load stability

# Search only between s=0.0001 and s_at_max_t (The Stable Motoring Region)
operating_slip = fminbound(objective_func, 0.0001, s_at_max_t)
operating_torque, operating_current = get_motor_metrics(operating_slip)
rotor_speed = Ns * (1 - operating_slip)

# --- PLOTTING ---
s_range = np.linspace(0.0001, 1.0, 500)
T_curve, I_curve = get_motor_metrics(s_range)

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.plot(s_range, T_curve, 'r-', lw=2, label="Motor Torque")
ax2.plot(s_range, I_curve, 'b--', lw=1.5, label="Stator Current")
ax1.axhline(load_torque, color='green', ls=':', label="Load Line")

# Operating Point
ax1.scatter(operating_slip, operating_torque, color='black', s=80, zorder=5)
ax1.annotate(f'Operating Point\ns={operating_slip:.4f}', (operating_slip, operating_torque), 
             xytext=(operating_slip+0.1, operating_torque+20), 
             arrowprops=dict(arrowstyle='->', color='black'))

ax1.set_xlim(1.0, 0) # Textbook view: Start at s=1 (left) to s=0 (right)
ax1.set_xlabel("Slip ($s$)")
ax1.set_ylabel("Torque (Nm)", color='r')
ax2.set_ylabel("Current (A)", color='b')
ax1.grid(True, linestyle=':', alpha=0.6)
st.pyplot(fig)

# --- DASHBOARD ---
st.subheader("📊 Performance Results")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Sync Speed", f"{Ns:.0f} RPM")
c2.metric("Resulting Slip", f"{operating_slip:.4f}")
c3.metric("Rotor Speed", f"{max(0, rotor_speed):.1f} RPM")
c4.metric("Current", f"{operating_current:.2f} A")

# Efficiency and PF logic
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
