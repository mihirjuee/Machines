import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fminbound
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="IM Lab Pro", page_icon="⚡", layout="centered")

# --- LIGHT MODE CSS ---
if "desktop_mode" not in st.session_state: st.session_state.desktop_mode = False
layout_width = "1200px" if st.session_state.desktop_mode else "700px"

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background: #f8fafc; color: #1e293b; }}
.card {{ background: #ffffff; padding: 15px; border-radius: 15px; margin-bottom: 15px; border: 1px solid #e2e8f0; box-shadow: 0px 2px 5px rgba(0,0,0,0.05); }}
.header {{ font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px; color: #0284c7; }}
.main > div {{ max-width: {layout_width} !important; }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: PARAMETERS ---
with st.sidebar:
    if st.button("🖥️ Toggle Desktop View"):
        st.session_state.desktop_mode = not st.session_state.desktop_mode
        st.rerun()
    st.header("⚙️ Machine Parameters")
    V = st.slider("Voltage (L-L V)", 100, 500, 400)
    f = st.slider("Frequency (Hz)", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)
    st.divider()
    st.header("⚙️ Equivalent Circuit")
    R1 = st.slider("Stator R1 [Ω]", 0.01, 5.0, 0.5)
    X1 = st.slider("Stator X1 [Ω]", 0.1, 5.0, 1.0)
    R2 = st.slider("Rotor R2 [Ω]", 0.01, 5.0, 0.8)
    X2 = st.slider("Rotor X2 [Ω]", 0.1, 5.0, 1.2)
    Xm = st.slider("Magnetizing Xm [Ω]", 5.0, 100.0, 30.0)

# --- ENGINE LOGIC ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
V_th = V_ph * abs((1j * Xm) / (R1 + 1j * (X1 + Xm)))
R_th, X_th = Z_th.real, Z_th.imag

def get_metrics(s):
    s = np.where(abs(s) < 1e-6, 1e-6, s)
    denom = ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * (R2/s)) / (omega_s * denom)
    Z = (R_th + R2/s) + 1j*(X_th + X2)
    current = V_th / abs(Z)
    return torque, current

# --- NAVIGATION ---
if "page" not in st.session_state: st.session_state.page = "Torque"
col1, col2, col3 = st.columns(3)
if col1.button("⚡ Torque"): st.session_state.page = "Torque"
if col2.button("📊 Performance"): st.session_state.page = "Performance"
if col3.button("🎓 Explain"): st.session_state.page = "Explain"

st.markdown('<div class="header">Induction Motor Lab Pro</div>', unsafe_allow_html=True)

# --- PAGE CONTENT ---
plt.style.use('default')
s_plot = np.linspace(-1, 2, 400)
T_plot, I_plot = get_metrics(s_plot)
N_plot = Ns * (1 - s_plot)

if st.session_state.page == "Torque":
    st.subheader("🔌 Equivalent Circuit")
    d = schemdraw.Drawing()
    d.add(elm.SourceV().label("V₁")); d.add(elm.Resistor().label("R₁")); d.add(elm.Inductor().label("X₁"))
    d.add(elm.Inductor().at((2,1)).label("Xm").down()); d.add(elm.Resistor().at((4,0)).label("R₂/s").right()); d.add(elm.Inductor().label("X₂"))
    st.pyplot(d.draw())
    
    
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(N_plot, T_plot, color='#0284c7', lw=2)
    ax.fill_between(N_plot, T_plot, 0, where=(s_plot < 0), color='green', alpha=0.1, label="Generating")
    ax.fill_between(N_plot, T_plot, 0, where=(s_plot >= 0) & (s_plot <= 1), color='blue', alpha=0.1, label="Motoring")
    ax.fill_between(N_plot, T_plot, 0, where=(s_plot > 1), color='orange', alpha=0.1, label="Braking")
    ax.set_title("Torque-Speed Characteristic"); ax.set_xlabel("Speed (RPM)"); ax.set_ylabel("Torque (Nm)"); ax.legend()
    st.pyplot(fig)
    

elif st.session_state.page == "Performance":
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(s_plot, I_plot, color='#fbbf24', lw=2)
    ax.set_title("Stator Current vs Slip"); ax.set_xlabel("Slip"); ax.set_ylabel("Current (A)")
    st.pyplot(fig)

elif st.session_state.page == "Explain":
    st.markdown('<div class="card"><b>Modes Explained:</b><br>• <b>Generating (s < 0):</b> Speed > Sync, power back to grid.<br>• <b>Motoring (0 < s < 1):</b> Normal operation.<br>• <b>Braking (s > 1):</b> Rapid deceleration via plugging.</div>', unsafe_allow_html=True)
