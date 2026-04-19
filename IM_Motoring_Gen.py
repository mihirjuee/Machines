import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fminbound

# --- PAGE CONFIG ---
st.set_page_config(page_title="IM Lab Pro", page_icon="⚡", layout="centered")

# --- APP STYLE ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0f172a; color: white; }
.card { background: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); }
.header { font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
if "page" not in st.session_state: st.session_state.page = "Torque"

col1, col2, col3 = st.columns(3)
if col1.button("⚡ Torque"): st.session_state.page = "Torque"
if col2.button("📊 Performance"): st.session_state.page = "Performance"
if col3.button("🎓 Explain"): st.session_state.page = "Explain"

st.markdown('<div class="header">Induction Motor Lab Pro</div>', unsafe_allow_html=True)

# --- PARAMETERS ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    V = st.slider("Voltage", 100, 500, 400)
    f = st.slider("Frequency", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)
    s_oper = st.slider("Operating Slip", -0.5, 1.5, 0.05)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALCULATIONS ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60
R1, X1, R2, X2, Xm = 0.5, 1.0, 0.8, 1.2, 30

def get_metrics(s):
    s = np.where(abs(s) < 1e-6, 1e-6, s)
    Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
    V_th = V_ph * abs((1j * Xm) / (R1 + 1j * (X1 + Xm)))
    R_th, X_th = Z_th.real, Z_th.imag
    denom = ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * (R2/s)) / (omega_s * denom)
    
    Z = (R_th + R2/s) + 1j*(X_th + X2)
    current = V_th / abs(Z)
    pf = np.cos(np.angle(Z))
    return torque, current, pf

# --- RENDER PAGES ---
plt.style.use('dark_background')
s_plot = np.linspace(-1, 2, 400)
T_plot, I_plot, _ = get_metrics(s_plot)
N_plot = Ns * (1 - s_plot)

if st.session_state.page == "Torque":
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(N_plot, T_plot, color='#38bdf8')
    ax.axhline(0, color='white', lw=0.5); ax.axvline(Ns, color='red', ls='--')
    ax.set_title("Torque-Speed Characteristic"); ax.set_xlabel("Speed (RPM)"); ax.set_ylabel("Torque (Nm)")
    st.pyplot(fig)

elif st.session_state.page == "Performance":
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(s_plot, I_plot, color='#fbbf24')
    ax.set_title("Stator Current vs Slip"); ax.set_xlabel("Slip"); ax.set_ylabel("Current (A)")
    st.pyplot(fig)

elif st.session_state.page == "Explain":
    mode = "Generating" if s_oper < 0 else ("Braking" if s_oper > 1 else "Motoring")
    st.markdown(f'<div class="card"><b>Mode:</b> {mode}<br><b>Current:</b> {get_metrics(s_oper)[1]:.2f} A</div>', unsafe_allow_html=True)
    st.write("Understand the modes: Generating (s<0) feeds back, Motoring (0<s<1) operates normally, and Braking (s>1) provides rapid stops.")
