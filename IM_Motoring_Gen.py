# 🔥 MUST BE FIRST
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="IM Lab Pro",
    page_icon="⚡",
    layout="centered"
)

# --- APP STYLE CSS ---
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: #0f172a;
    color: white;
}

/* Card style */
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

/* Header */
.header {
    font-size: 22px;
    font-weight: bold;
    padding: 10px;
}

/* Sticky bottom nav */
.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #020617;
    display: flex;
    justify-content: space-around;
    padding: 10px 0;
    border-top: 1px solid #334155;
    z-index: 999;
}

/* Nav buttons */
.nav-btn {
    color: white;
    font-size: 14px;
    text-align: center;
}

/* Slider spacing */
.stSlider {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header">⚡ Induction Motor Lab</div>', unsafe_allow_html=True)

# --- SESSION STATE FOR NAV ---
if "page" not in st.session_state:
    st.session_state.page = "Torque"

# --- NAVIGATION HANDLER ---
def set_page(p):
    st.session_state.page = p

# --- PARAMETERS (CARD) ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎛 Controls")
    V = st.slider("Voltage", 100, 500, 400)
    f = st.slider("Frequency", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)

    s_oper = st.slider("Slip", -0.5, 1.5, 0.05)

    st.markdown('</div>', unsafe_allow_html=True)

# --- CALCULATIONS ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

R1, X1, R2, X2, Xm = 0.5, 1.0, 0.8, 1.2, 30

Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
V_th = V_ph * abs((1j * Xm) / (R1 + 1j * (X1 + Xm)))
R_th, X_th = Z_th.real, Z_th.imag

def safe_s(s):
    return 1e-6 if abs(s) < 1e-6 else s

def get_torque(s):
    s = safe_s(s)
    denom = ((R_th + R2/s)**2 + (X_th + X2)**2)
    return (3 * V_th**2 * (R2/s)) / (omega_s * denom)

def get_current(s):
    s = safe_s(s)
    Z = (R_th + R2/s) + 1j*(X_th + X2)
    return V_th / abs(Z)

def get_pf(s):
    s = safe_s(s)
    Z = (R_th + R2/s) + 1j*(X_th + X2)
    return np.cos(np.angle(Z))

# --- MODE DISPLAY (CARD) ---
mode = "Motoring"
if s_oper < 0:
    mode = "Generating"
elif s_oper > 1:
    mode = "Braking"

st.markdown(f"""
<div class="card">
<b>Mode:</b> {mode} <br>
<b>Speed:</b> {Ns*(1-s_oper):.0f} RPM
</div>
""", unsafe_allow_html=True)

# --- PAGE CONTENT ---
if st.session_state.page == "Torque":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    s = np.linspace(-1, 2, 400)
    T = [get_torque(x) for x in s]
    N = Ns * (1 - s)

    fig, ax = plt.subplots()
    ax.plot(N, T)
    ax.scatter(Ns*(1-s_oper), get_torque(s_oper))

    ax.set_title("Torque-Speed")
    st.pyplot(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Performance":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    s = np.linspace(-1, 2, 300)
    N = Ns * (1 - s)

    fig, ax = plt.subplots()
    ax.plot(N, [get_current(x) for x in s])
    ax.set_title("Current")
    st.pyplot(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "Explain":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎓 Explanation")

    if s_oper < 0:
        st.success("Generating: Power returned to supply.")
    elif s_oper > 1:
        st.error("Braking: High reverse torque.")
    else:
        st.info("Motoring: Normal operation.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- BOTTOM NAVIGATION ---
st.markdown(f"""
<div class="bottom-nav">
    <div class="nav-btn">⚡ Torque</div>
    <div class="nav-btn">📊 Performance</div>
    <div class="nav-btn">🎓 Explain</div>
</div>
""", unsafe_allow_html=True)

# --- CLICK HANDLING ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚡"):
        set_page("Torque")

with col2:
    if st.button("📊"):
        set_page("Performance")

with col3:
    if st.button("🎓"):
        set_page("Explain")
