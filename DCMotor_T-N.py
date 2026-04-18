import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="DC Shunt Motor Characteristics", layout="wide")

st.title("⚡ DC Shunt Motor Torque-Speed Characteristics")

# --- SIDEBAR INPUTS ---
st.sidebar.header("🔧 Motor Parameters")
V = st.sidebar.slider("Supply Voltage (V)", 100, 300, 220)
Ra = st.sidebar.slider("Armature Resistance (Ohm)", 0.1, 2.0, 0.5)
k = st.sidebar.slider("Motor Constant (k)", 0.1, 2.0, 0.8)
phi = st.sidebar.slider("Flux (Φ)", 0.5, 1.5, 1.0)

col1, col2 = st.columns([1, 1])

# --- CIRCUIT DIAGRAM ---
with col1:
    st.subheader("🔌 DC Shunt Motor Circuit")
    
    d = schemdraw.Drawing()
    d += elm.SourceV().label(f"{V}V")
    d += elm.Line().right(length=2)
    
    # Field circuit (Shunt)
    d.push()
    d += elm.Line().down(length=2)
    d += elm.Inductor().label("Rf")
    d += elm.Ground()
    d.pop()
    
    # Armature circuit
    d += elm.Line().right()
    d += elm.Line().down(length=2)
    d += elm.Resistor().label("Ra")
    d += elm.Motor().label("M")
    d += elm.Line().down()
    d += elm.Ground()
    
    # FIX: Use .fig attribute to access the Matplotlib figure directly
    st.pyplot(d.draw().fig)

# --- GRAPH ---
with col2:
    st.subheader("📊 Torque vs Speed")
    
    T = np.linspace(0, 50, 100)
    Ia = T / (k * phi)
    N = (V - Ia * Ra) / (k * phi)

    fig, ax = plt.subplots()
    ax.plot(T, N, color='tab:blue', linewidth=2)
    ax.set_xlabel("Torque (Nm)")
    ax.set_ylabel("Speed (RPM)")
    ax.set_title("Speed-Torque Characteristic")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig)

# --- THEORY ---
st.divider()
st.subheader("📘 Governing Equations")
st.latex(r"T = k \phi I_a")
st.latex(r"N = \frac{V - I_a R_a}{k \phi}")
st.info("👉 Note: The speed decreases linearly with torque due to the armature resistance.")
