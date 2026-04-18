import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')  # जरूरी for Streamlit Cloud
import matplotlib.pyplot as plt
from scipy.optimize import fminbound
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Induction Motor Analysis", 
    page_icon="⚡", 
    layout="wide"
)

# --- HEADER ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=100)
    except:
        st.header("⚡")

with col_title:
    st.title("Induction Motor Performance: Load-Driven Analysis")

st.divider()

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

# --- CALCULATIONS ---
V_phase = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

# Thevenin
V_th = V_phase * (Xm / np.sqrt(R1**2 + (X1 + Xm)**2))
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
R_th, X_th = Z_th.real, Z_th.imag

def get_motor_metrics(s):
    s_safe = np.clip(s, 0.0001, 1.0)

    denom = omega_s * ((R_th + R2/s_safe)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * R2 / s_safe) / denom

    Zr = (R2/s_safe) + 1j*X2
    Zp = (1j*Xm * Zr) / (1j*Xm + Zr)
    Z_total = R1 + 1j*X1 + Zp

    I1 = V_phase / abs(Z_total)
    pf = np.cos(np.angle(Z_total))

    return torque, I1, pf

# --- TORQUE RANGE ---
s_range_calc = np.linspace(0.0001, 1.0, 500)
T_range_calc, _, _ = get_motor_metrics(s_range_calc)

max_torque_possible = float(np.max(T_range_calc))
s_at_max_t = s_range_calc[np.argmax(T_range_calc)]

# --- LOAD ---
st.sidebar.divider()
st.sidebar.header("⚖️ Applied Load")

load_torque = st.sidebar.slider(
    "Applied Load Torque (Nm)", 
    0.0, round(max_torque_possible * 1.1, 1), 50.0
)

# --- OPERATING POINT ---
if load_torque > max_torque_possible:
    st.error("🚨 MOTOR STALL: Load exceeds breakdown torque")
    operating_slip = 1.0
    is_stalled = True
else:
    def objective(s_try):
        t, _, _ = get_motor_metrics(s_try)
        return abs(t - load_torque)

    operating_slip = fminbound(objective, 0.0001, s_at_max_t)
    is_stalled = False

operating_torque, operating_current, operating_pf = get_motor_metrics(operating_slip)
rotor_speed = Ns * (1 - operating_slip)

# =============================
# 🔌 LAYOUT (CIRCUIT + GRAPH)
# =============================
col1, col2 = st.columns([1, 2])

# --- CIRCUIT DIAGRAM ---
with col1:
    st.subheader("🔌 Per-Phase Equivalent Circuit")

    d = schemdraw.Drawing()

    d += elm.SourceV().label("V₁")

    d += elm.Resistor().label("R₁")
    d += elm.Inductor().label("X₁")

    # Parallel branch
    d.push()

    # Magnetizing
    d += elm.Line().down()
    d += elm.Inductor().label("Xm")
    d += elm.Line().down()
    d += elm.Ground()
    d.pop()

    # Rotor
    d += elm.Resistor().label("R₂/s")
    d += elm.Inductor().label("X₂")

    d += elm.Line().down()
    d += elm.Ground()

    d.draw()
    st.pyplot(d.fig)

# --- GRAPH ---
with col2:
    s_plot = np.linspace(0.0001, 1.0, 500)
    T_plot, I_plot, _ = get_motor_metrics(s_plot)

    fig, ax1 = plt.subplots(figsize=(10, 4.5))
    ax2 = ax1.twinx()

    ax1.plot(s_plot, T_plot, 'r-', lw=2, label="Torque")
    ax2.plot(s_plot, I_plot, 'b--', lw=1.5, label="Current")

    ax1.axhline(load_torque, color='green', ls=':')

    ax1.scatter(operating_slip, operating_torque, color='black', s=80)

    label = "STALL" if is_stalled else f"s={operating_slip:.4f}"
    ax1.annotate(label, (operating_slip, operating_torque),
                 xytext=(operating_slip+0.1, operating_torque+20),
                 arrowprops=dict(arrowstyle='->'))

    ax1.set_xlim(1.0, 0)
    ax1.set_xlabel("Slip")
    ax1.set_ylabel("Torque (Nm)", color='r')
    ax2.set_ylabel("Current (A)", color='b')
    ax1.grid(True)

    st.pyplot(fig)

# =============================
# 📊 RESULTS
# =============================
st.subheader("📊 Performance Results")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sync Speed", f"{Ns:.0f} RPM")
c2.metric("Slip", f"{operating_slip:.4f}")

if is_stalled:
    c3.metric("Rotor Speed", "0 RPM")
    c4.metric("Current", f"{operating_current:.2f} A")
else:
    c3.metric("Rotor Speed", f"{rotor_speed:.1f} RPM")
    c4.metric("Current", f"{operating_current:.2f} A")

# --- POWER ---
Pin = 3 * V_phase * operating_current * operating_pf
Pout = operating_torque * (omega_s * (1 - operating_slip))
eff = (Pout / Pin) * 100 if not is_stalled and Pin > 0 else 0

c5, c6, c7, c8 = st.columns(4)
c5.metric("Input Power", f"{Pin/1000:.2f} kW")
c6.metric("Output Power", f"{Pout/1000:.2f} kW")
c7.metric("Efficiency", f"{eff:.1f} %")
c8.metric("Power Factor", f"{operating_pf:.2f}")

st.divider()
st.info("💡 Breakdown torque is the stability limit. Beyond this, the motor stalls.")
