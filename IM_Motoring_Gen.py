# 🔥 MUST BE FIRST
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fminbound
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Induction Machine Lab", page_icon="⚡", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
}
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ Induction Machine Lab")

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

# --- CALCULATIONS ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60

Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
V_th = V_ph * abs((1j * Xm) / (R1 + 1j * (X1 + Xm)))
R_th, X_th = Z_th.real, Z_th.imag

def get_torque(s):
    s = np.where(s == 0, 1e-6, s)
    denom = ((R_th + R2/s)**2 + (X_th + X2)**2)
    T = (3 * V_th**2 * (R2/s)) / (omega_s * denom)
    return T

# --- TITLE ---
st.title("⚡ Induction Machine: Torque–Speed Characteristics")

col1, col2 = st.columns([1, 2])

# --- EQUIVALENT CIRCUIT ---
with col1:
    st.subheader("🔌 Equivalent Circuit")

    d = schemdraw.Drawing()

    d += elm.SourceV().label("V₁")
    d += elm.Line().right()

    d += elm.Resistor().label("R₁")
    d += elm.Inductor().label("X₁")

    d += elm.Dot()

    # Magnetizing branch
    d.push()
    d += elm.Line().up()
    d += elm.Inductor().label("Xm")
    d += elm.Line().down()
    d.pop()

    # Rotor branch
    d += elm.Line().right()
    d += elm.Resistor().label("R₂/s")
    d += elm.Inductor().label("X₂")

    # Return path
    d += elm.Line().down()
    d += elm.Line().left(6)
    d += elm.Line().up()

    d.draw()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.clf()

# --- TORQUE-SPEED PLOT ---
with col2:
    # Full slip range
    s = np.linspace(-1.0, 2.0, 600)
    T = get_torque(s)

    # Convert to speed
    N = Ns * (1 - s)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(N, T, lw=2)

    # Regions
    ax.fill_between(N, T, 0, where=(s < 0), alpha=0.2, label="Generating (N > Ns)")
    ax.fill_between(N, T, 0, where=(s >= 0) & (s <= 1), alpha=0.2, label="Motoring (0 < N < Ns)")
    ax.fill_between(N, T, 0, where=(s > 1), alpha=0.2, label="Braking (N < 0)")

    # Reference lines
    ax.axhline(0)
    ax.axvline(0, linestyle='--', label="Zero Speed")
    ax.axvline(Ns, linestyle=':', label="Synchronous Speed (Ns)")

    # Labels
    ax.set_xlabel("Speed (RPM)")
    ax.set_ylabel("Torque (Nm)")
    ax.set_title("Torque–Speed Characteristics")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# --- INTERACTIVE ANALYSIS ---
st.subheader("🔍 Interactive Operating Point")

load_t = st.slider("Apply Load Torque (Nm)", -100.0, 200.0, 50.0)

def obj(s):
    return abs(get_torque(s) - load_t)

op_slip = fminbound(obj, -0.5, 1.5)

speed = Ns * (1 - op_slip)

colA, colB, colC = st.columns(3)

colA.metric("Operating Slip", f"{op_slip:.4f}")
colB.metric("Speed (RPM)", f"{speed:.0f}")

mode = "Generating" if op_slip < 0 else ("Braking" if op_slip > 1 else "Motoring")
colC.metric("Mode", mode)
