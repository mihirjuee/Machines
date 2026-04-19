# 🔥 MUST BE FIRST
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Induction Motor Lab",
    page_icon="⚡",
    layout="centered"  # ✅ Better for mobile
)

# --- MOBILE CSS ---
st.markdown("""
<style>
/* Reduce padding for mobile */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
}

/* Bigger buttons & sliders */
button, .stSlider {
    font-size: 16px !important;
}

/* Sticky top panel */
.sticky {
    position: sticky;
    top: 0;
    background-color: white;
    padding: 10px;
    z-index: 999;
    border-bottom: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("⚡ Induction Machine Lab (Mobile)")

# --- PARAMETERS (COLLAPSIBLE) ---
with st.expander("⚙️ Machine Parameters", expanded=True):
    V = st.slider("Voltage (L-L)", 100, 500, 400)
    f = st.slider("Frequency", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)

with st.expander("⚙️ Equivalent Circuit"):
    R1 = st.slider("R1", 0.01, 5.0, 0.5)
    X1 = st.slider("X1", 0.1, 5.0, 1.0)
    R2 = st.slider("R2", 0.01, 5.0, 0.8)
    X2 = st.slider("X2", 0.1, 5.0, 1.2)
    Xm = st.slider("Xm", 5.0, 100.0, 30.0)

# --- SLIP CONTROL (IMPORTANT → KEEP VISIBLE) ---
st.markdown("### 🎛 Control")
s_oper = st.slider("Slip", -0.5, 1.5, 0.05, step=0.01)

# --- CALCULATIONS ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

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

# --- STICKY INFO PANEL ---
mode = "Motoring"
if s_oper < 0:
    mode = "Generating"
elif s_oper > 1:
    mode = "Braking"

st.markdown(f"""
<div class="sticky">
<b>Mode:</b> {mode} &nbsp; | &nbsp;
<b>Speed:</b> {Ns*(1-s_oper):.0f} RPM
</div>
""", unsafe_allow_html=True)

# --- TABS FOR CLEAN UI ---
tab1, tab2, tab3 = st.tabs(["📈 Torque", "📊 Performance", "🎓 Explain"])

# --- TAB 1: TORQUE ---
with tab1:
    s = np.linspace(-1, 2, 400)
    T = [get_torque(x) for x in s]
    N = Ns * (1 - s)

    fig, ax = plt.subplots()
    ax.plot(N, T)

    # Operating point
    ax.scatter(Ns*(1-s_oper), get_torque(s_oper))

    ax.axhline(0)
    ax.axvline(Ns, linestyle='--')

    ax.set_xlabel("Speed")
    ax.set_ylabel("Torque")
    ax.set_title("Torque-Speed")

    st.pyplot(fig, use_container_width=True)

# --- TAB 2: PERFORMANCE ---
with tab2:
    s = np.linspace(-1, 2, 300)
    N = Ns * (1 - s)

    fig1, ax1 = plt.subplots()
    ax1.plot(N, [get_current(x) for x in s])
    ax1.set_title("Current")
    st.pyplot(fig1, use_container_width=True)

    fig2, ax2 = plt.subplots()
    ax2.plot(N, [get_pf(x) for x in s])
    ax2.set_title("Power Factor")
    st.pyplot(fig2, use_container_width=True)

# --- TAB 3: STUDENT MODE ---
with tab3:
    st.subheader("🎓 Auto Explanation")

    if s_oper < 0:
        st.success("Generating Mode: Power flows back to supply.")
    elif s_oper > 1:
        st.error("Braking Mode: Strong reverse torque.")
    else:
        st.info("Motoring Mode: Normal operation.")
