import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fminbound

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Induction Motor Analysis", 
    page_icon="⚡", 
    layout="wide"
)

# --- HEADER WITH LOGO ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=100) 
    except:
        st.header("⚡")

with col_title:
    st.title("Induction Motor Performance: Load-Driven Analysis")

st.divider()

# --- SIDEBAR: MOTOR PARAMETERS ---
st.sidebar.header("🕹️ Motor Parameters")
V = st.sidebar.slider("Supply Voltage (Line-to-Line V)", 100, 500, 400)
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
    # Bound slip to avoid division by zero or negative speed
    s_safe = np.clip(s, 0.0001, 1.0)
    denom_t = omega_s * ((R_th + R2/s_safe)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * R2 / s_safe) / denom_t
    
    Zr = (R2/s_safe) + 1j*X2
    Zp = (1j*Xm * Zr) / (1j*Xm + Zr)
    Z_total = R1 + 1j*X1 + Zp
    I1 = V_phase / abs(Z_total)
    pf = np.cos(np.angle(Z_total))
    return torque, I1, pf

# Pre-calculate full curve for limits
s_range_calc = np.linspace(0.0001, 1.0, 500)
T_range_calc, _, _ = get_motor_metrics(s_range_calc)
max_torque_possible = float(np.max(T_range_calc))
s_at_max_t = s_range_calc[np.argmax(T_range_calc)]

# --- SIDEBAR: LOAD CONTROL ---
st.sidebar.divider()
st.sidebar.header("⚖️ Applied Load")
# We allow the slider to go slightly above max torque to demonstrate the stall
load_torque = st.sidebar.slider("Applied Load Torque (Nm)", 0.0, round(max_torque_possible * 1.1, 1), 50.0)

# --- STALL LOGIC & OPERATING POINT ---
if load_torque > max_torque_possible:
    st.error("🚨 **MOTOR STALL**: The applied load is greater than the breakdown torque!")
    operating_slip = 1.0  # Rotor stops
    is_stalled = True
else:
    # Solve for stable slip (between 0 and breakdown point)
    def objective(s_try):
        t_motor, _, _ = get_motor_metrics(s_try)
        return abs(t_motor - load_torque)
    
    operating_slip = fminbound(objective, 0.0001, s_at_max_t)
    is_stalled = False

# Get final performance data
operating_torque, operating_current, operating_pf = get_motor_metrics(operating_slip)
rotor_speed = Ns * (1 - operating_slip)

# --- PLOTTING ---
s_plot = np.linspace(0.0001, 1.0, 500)
T_plot, I_plot, _ = get_motor_metrics(s_plot)

fig, ax1 = plt.subplots(figsize=(10, 4.5))
ax2 = ax1.twinx()

ax1.plot(s_plot, T_plot, 'r-', lw=2, label="Motor Torque")
ax2.plot(s_plot, I_plot, 'b--', lw=1.5, label="Stator Current")
ax1.axhline(load_torque, color='green', ls=':', label="Applied Load")

# Marker for result
ax1.scatter(operating_slip, operating_torque, color='black', s=80, zorder=5)
label_text = "STALL (Locked Rotor)" if is_stalled else f"Op. Point\ns={operating_slip:.4f}"
ax1.annotate(label_text, (operating_slip, operating_torque), 
             xytext=(operating_slip+0.1, operating_torque+20), 
             arrowprops=dict(arrowstyle='->', color='black'))

ax1.set_xlim(1.0, 0) # Textbook view: Start at s=1 (left) to s=0 (right)
ax1.set_xlabel("Slip ($s$)", fontsize=11)
ax1.set_ylabel("Torque (Nm)", color='r', fontsize=11)
ax2.set_ylabel("Current (A)", color='b', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)
st.pyplot(fig)

# --- DASHBOARD RESULTS ---
st.subheader("📊 Performance Results")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Sync Speed", f"{Ns:.0f} RPM")
c2.metric("Resulting Slip", f"{operating_slip:.4f}")

if is_stalled:
    c3.metric("Rotor Speed", "0.0 RPM", delta="-100% STALL", delta_color="inverse")
    c4.metric("Current", f"{operating_current:.2f} A", delta="IN-RUSH", delta_color="inverse")
else:
    c3.metric("Rotor Speed", f"{rotor_speed:.1f} RPM")
    c4.metric("Current", f"{operating_current:.2f} A")

# Efficiency and Power calculations
Pin = 3 * V_phase * operating_current * operating_pf
Pout = operating_torque * (omega_s * (1 - operating_slip))
eff = (Pout / Pin) * 100 if not is_stalled and Pin > 0 else 0.0

c5, c6, c7, c8 = st.columns(4)
c5.metric("Input Power", f"{Pin/1000:.2f} kW")
c6.metric("Output Power", f"{Pout/1000:.2f} kW")
c7.metric("Efficiency", f"{eff:.1f} %")
c8.metric("Power Factor", f"{operating_pf:.2f}")

st.divider()
st.info("**Engineering Tip:** The 'Breakdown Torque' is the limit of stability. Once the load exceeds this point, the motor moves from the stable linear region into a stall.")
