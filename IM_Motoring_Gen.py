# 🔥 MUST BE FIRST
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="IM Lab Pro", page_icon="⚡", layout="centered")

# --- SESSION ---
if "page" not in st.session_state:
    st.session_state.page = "Torque"

if "desktop_mode" not in st.session_state:
    st.session_state.desktop_mode = False

layout_width = "1200px" if st.session_state.desktop_mode else "700px"

# --- APP CSS ---
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: #f1f5f9;
}}

.main > div {{
    max-width: {layout_width} !important;
}}

/* HEADER */
.header {{
    font-size: 22px;
    font-weight: bold;
    text-align: center;
    padding: 10px;
    color: #0284c7;
}}

/* CARD */
.card {{
    background: white;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.05);
}}

/* STICKY STATUS BAR */
.status {{
    position: sticky;
    top: 0;
    background: #ffffff;
    padding: 10px;
    border-bottom: 1px solid #e2e8f0;
    z-index: 999;
}}

/* FLOAT BUTTON PANEL */
.floating {{
    position: fixed;
    bottom: 80px;
    right: 20px;
    z-index: 999;
}}

/* BOTTOM NAV */
.bottom-nav {{
    position: fixed;
    bottom: 0;
    width: 100%;
    background: white;
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: space-around;
    padding: 8px 0;
    z-index: 999;
}}

.nav-item {{
    text-align: center;
    font-size: 13px;
}}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if st.button("🖥️ Toggle Desktop View"):
        st.session_state.desktop_mode = not st.session_state.desktop_mode
        st.rerun()

    st.header("⚙️ Parameters")
    V = st.slider("Voltage", 100, 500, 400)
    f = st.slider("Frequency", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)

    st.divider()

    R1 = st.slider("R1", 0.01, 5.0, 0.5)
    X1 = st.slider("X1", 0.1, 5.0, 1.0)
    R2 = st.slider("R2", 0.01, 5.0, 0.8)
    X2 = st.slider("X2", 0.1, 5.0, 1.2)
    Xm = st.slider("Xm", 5.0, 100.0, 30.0)

# --- ENGINE ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
V_th = V_ph * abs((1j * Xm) / (R1 + 1j * (X1 + Xm)))
R_th, X_th = Z_th.real, Z_th.imag

def safe_s(s):
    return np.where(abs(s) < 1e-6, 1e-6, s)

def get_metrics(s):
    s = safe_s(s)
    denom = ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * (R2/s)) / (omega_s * denom)
    Z = (R_th + R2/s) + 1j*(X_th + X2)
    current = V_th / np.abs(Z)
    return torque, current

# --- CONTROL ---
s_oper = st.slider("🎛 Slip Control", -0.5, 1.5, 0.05, step=0.01)

# --- MODE ---
mode = "Motoring"
if s_oper < 0:
    mode = "Generating"
elif s_oper > 1:
    mode = "Braking"

# --- STATUS BAR ---
st.markdown(f"""
<div class="status">
<b>Mode:</b> {mode} | <b>Speed:</b> {Ns*(1-s_oper):.0f} RPM
</div>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header">⚡ Induction Motor Lab Pro</div>', unsafe_allow_html=True)

# --- DATA ---
s_plot = np.linspace(-1, 2, 400)
T_plot, I_plot = get_metrics(s_plot)
N_plot = Ns * (1 - s_plot)

# --- PAGES ---
if st.session_state.page == "Torque":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    d = schemdraw.Drawing()
    d += elm.SourceV().label("V₁")
    d += elm.Resistor().label("R₁")
    d += elm.Inductor().label("X₁")
    d += elm.Dot()

    d.push()
    d += elm.Line().up()
    d += elm.Inductor().label("Xm")
    d += elm.Line().down()
    d.pop()

    d += elm.Resistor().label("R₂/s")
    d += elm.Inductor().label("X₂")

    st.pyplot(d.draw())

    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(N_plot, T_plot)

    ax.scatter(Ns*(1-s_oper), get_metrics(s_oper)[0])

    ax.fill_between(N_plot, T_plot, 0, where=(s_plot < 0), alpha=0.1)
    ax.fill_between(N_plot, T_plot, 0, where=(s_plot >= 0)&(s_plot<=1), alpha=0.1)
    ax.fill_between(N_plot, T_plot, 0, where=(s_plot > 1), alpha=0.1)

    ax.set_title("Torque-Speed")
    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Performance":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(s_plot, I_plot)
    ax.set_title("Current vs Slip")
    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Explain":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if s_oper < 0:
        st.success("Generating Mode → Power returned to supply")
    elif s_oper > 1:
        st.error("Braking Mode → Plugging action")
    else:
        st.info("Motoring Mode → Normal operation")

    st.markdown('</div>', unsafe_allow_html=True)

# --- BOTTOM NAV ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚡"):
        st.session_state.page = "Torque"

with col2:
    if st.button("📊"):
        st.session_state.page = "Performance"

with col3:
    if st.button("🎓"):
        st.session_state.page = "Explain"

st.markdown("""
<div class="bottom-nav">
<div class="nav-item">⚡ Torque</div>
<div class="nav-item">📊 Performance</div>
<div class="nav-item">🎓 Explain</div>
</div>
""", unsafe_allow_html=True)
