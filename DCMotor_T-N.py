import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="DC Shunt Motor Characteristics",page_icon="logo.png", layout="wide")

st.title("⚡ DC Shunt Motor Torque-Speed Characteristics")

st.write("Interactive simulation with circuit diagram.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("🔧 Motor Parameters")

V = st.sidebar.slider("Supply Voltage (V)", 100, 300, 220)
Ra = st.sidebar.slider("Armature Resistance (Ohm)", 0.1, 2.0, 0.5)
k = st.sidebar.slider("Motor Constant (k)", 0.1, 2.0, 0.8)
phi = st.sidebar.slider("Flux (Φ)", 0.5, 1.5, 1.0)

# --- LAYOUT ---
col1, col2 = st.columns([1, 1])

# =========================
# 🔌 CIRCUIT DIAGRAM
# =========================
with col1:
    st.subheader("🔌 DC Shunt Motor Circuit")

    d = schemdraw.Drawing()

    # Supply
    d += elm.SourceV().label(f"{V} V")

    # Top wire
    d += elm.Line().right()

    # Branch down for field winding
    d.push()
    d += elm.Line().down()
    d += elm.Resistor().label("Rsh (Field)")
    d += elm.Line().down()
    d += elm.Ground()
    d.pop()

    # Continue main line
    d += elm.Resistor().label("Ra (Armature)")
    d += elm.Motor().label("DC Motor")

    # Return path
    d += elm.Line().down()
    d += elm.Ground()

    d.draw()          # first draw
st.pyplot(d.fig)  # then pass figure

# =========================
# 📊 GRAPH
# =========================
with col2:
    st.subheader("📊 Torque vs Speed")

    T = np.linspace(0, 50, 100)
    Ia = T / (k * phi)
    N = (V - Ia * Ra) / (k * phi)

    fig, ax = plt.subplots()
    ax.plot(T, N, linewidth=2)
    ax.set_xlabel("Torque (Nm)")
    ax.set_ylabel("Speed")
    ax.set_title("Torque-Speed Characteristic")
    ax.grid()

    st.pyplot(fig)

# =========================
# 📘 THEORY
# =========================
st.subheader("📘 Governing Equations")

st.latex(r"T = k \phi I_a")
st.latex(r"N = \frac{V - I_a R_a}{k \phi}")

st.info("👉 DC Shunt Motor runs at nearly constant speed with varying load.")
