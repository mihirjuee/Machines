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
st.set_page_config(page_title="Induction Machine Lab Pro", page_icon="⚡", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ Induction Lab Pro")

    st.header("⚙️ Machine Parameters")
    V = st.slider("Voltage (L-L V)", 100, 500, 400)
    f = st.slider("Frequency (Hz)", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)

    st.divider()

    st.header("⚙️ Equivalent Circuit")
    R1 = st.slider("R1 [Ω]", 0.01, 5.0, 0.5)
    X1 = st.slider("X1 [Ω]", 0.1, 5.0, 1.0)
    R2 = st.slider("R2 [Ω]", 0.01, 5.0, 0.8)
    X2 = st.slider("X2 [Ω]", 0.1, 5.0, 1.2)
    Xm = st.slider("Xm [Ω]", 5.0, 100.0, 30.0)

    st.divider()

    mode_select = st.radio("Select Mode View", ["All", "Motoring", "Generating", "Braking"])

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

def get_current(s):
    s = np.where(s == 0, 1e-6, s)
    Z = complex(R1 + R2/s, X1 + X2)
    return V_ph / abs(Z)

def get_efficiency(s):
    s = np.where(s == 0, 1e-6, s)
    return np.maximum(0, (1 - s) * 100)

# --- TITLE ---
st.title("⚡ Induction Machine – Advanced Analysis")

col1, col2 = st.columns([1, 2])

# --- CIRCUIT ---
with col1:
    st.subheader("🔌 Equivalent Circuit")

    d = schemdraw.Drawing()
    d += elm.SourceV().label("V")
    d += elm.Line().right()
    d += elm.Resistor().label("R1")
    d += elm.Inductor().label("X1")
    d += elm.Dot()

    d.push()
    d += elm.Line().up()
    d += elm.Inductor().label("Xm")
    d += elm.Line().down()
    d.pop()

    d += elm.Line().right()
    d += elm.Resistor().label("R2/s")
    d += elm.Inductor().label("X2")

    d += elm.Line().down()
    d += elm.Line().left(6)
    d += elm.Line().up()

    d.draw()
    st.pyplot(plt.gcf())
    plt.clf()

# --- PLOTS ---
with col2:
    s = np.linspace(-1, 2, 600)
    T = get_torque(s)
    N = Ns * (1 - s)

    # Mode filtering
    if mode_select == "Motoring":
        mask = (s >= 0) & (s <= 1)
    elif mode_select == "Generating":
        mask = (s < 0)
    elif mode_select == "Braking":
        mask = (s > 1)
    else:
        mask = np.ones_like(s, dtype=bool)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(N[mask], T[mask], lw=2)

    # --- Tmax (Breakdown Torque) ---
    Tmax = np.max(T)
    idx = np.argmax(T)
    ax.scatter(N[idx], Tmax)
    ax.text(N[idx], Tmax, "  Tmax", fontsize=9)

    # --- Stable / Unstable ---
    ax.axvline(Ns, linestyle=':', label="Ns")

    # Stable: negative slope
    stable = np.gradient(T) < 0
    ax.fill_between(N, T, 0, where=stable, alpha=0.1, label="Stable")
    ax.fill_between(N, T, 0, where=~stable, alpha=0.05, label="Unstable")

    # --- Regions ---
    ax.fill_between(N, T, 0, where=(s < 0), alpha=0.2, label="Generating")
    ax.fill_between(N, T, 0, where=(s >= 0) & (s <= 1), alpha=0.2, label="Motoring")
    ax.fill_between(N, T, 0, where=(s > 1), alpha=0.2, label="Braking")

    # --- Power Flow Arrows ---
    ax.annotate("Power → Rotor", xy=(0.5*Ns, Tmax/2), xytext=(0.3*Ns, Tmax/1.5),
                arrowprops=dict(arrowstyle="->"))
    ax.annotate("Power → Supply", xy=(1.2*Ns, Tmax/2), xytext=(1.4*Ns, Tmax/1.5),
                arrowprops=dict(arrowstyle="->"))

    ax.axhline(0)
    ax.axvline(0, linestyle='--')

    ax.set_xlabel("Speed (RPM)")
    ax.set_ylabel("Torque (Nm)")
    ax.set_title("Torque–Speed Characteristics")
    ax.legend(fontsize=8)
    ax.grid(True)

    st.pyplot(fig)

# --- EXTRA PLOTS ---
st.subheader("📉 Performance Curves")

colA, colB = st.columns(2)

with colA:
    fig1, ax1 = plt.subplots()
    ax1.plot(N, get_current(s))
    ax1.set_title("Current vs Speed")
    ax1.set_xlabel("Speed")
    ax1.set_ylabel("Current")
    ax1.grid(True)
    st.pyplot(fig1)

with colB:
    fig2, ax2 = plt.subplots()
    ax2.plot(N, get_efficiency(s))
    ax2.set_title("Efficiency vs Speed")
    ax2.set_xlabel("Speed")
    ax2.set_ylabel("Efficiency (%)")
    ax2.grid(True)
    st.pyplot(fig2)

# --- OPERATING POINT ---
st.subheader("🔍 Operating Point")

load_t = st.slider("Load Torque", -100.0, 200.0, 50.0)

def obj(s):
    return abs(get_torque(s) - load_t)

op_slip = fminbound(obj, -0.5, 1.5)
speed = Ns * (1 - op_slip)

colX, colY, colZ = st.columns(3)

colX.metric("Slip", f"{op_slip:.4f}")
colY.metric("Speed (RPM)", f"{speed:.0f}")
mode = "Generating" if op_slip < 0 else ("Braking" if op_slip > 1 else "Motoring")
colZ.metric("Mode", mode)
