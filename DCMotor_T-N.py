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
    d += elm.Line().up(length=2)
    d += elm.SourceV().label(f"{V}V")
    d += elm.Line().right(length=2)
   
    # Field circuit (Shunt)
    d.push()
    d += elm.Line().down(length=1)
    d += elm.Inductor().label("Rf")
    d += elm.Line().down(length=2.1)
    d.pop()
    
    # Armature circuit
    d += elm.Line().right()
    d += elm.Line().down(length=0.1)
    d += elm.Resistor().label("Ra")
    d += elm.Motor().label("M")
    d += elm.Line().left(length=5)
    d += elm.Line().up(length=3)
    # FIX: Use .fig attribute to access the Matplotlib figure directly
    st.pyplot(d.draw().fig)

# --- GRAPH ---
# --- REVISED REALISTIC GRAPH SECTION ---
with col2:
    st.subheader("📊 Torque vs Speed (Realistic)")
    
    T = np.linspace(0, 50, 100)
    Ia = T / (k * phi)
    
    # Introduce a simple model for armature reaction:
    # Flux decreases as current increases
    demag_factor = -0.005 
    phi_eff = np.maximum(phi - (demag_factor * Ia), 0.1)
    
    # Speed is now calculated using the effective (reduced) flux
    N = (V - Ia * Ra) / (k * phi_eff)
    N = np.maximum(N, 0) # Motor doesn't go negative

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(T, N, color='tab:red', linewidth=2.5, label='Actual (Non-linear)')
    
    # Plot the "Ideal" linear version for comparison
    N_ideal = (V - Ia * Ra) / (k * phi)
    ax.plot(T, N_ideal, color='gray', linestyle='--', label='Ideal (Linear)')
    
    ax.set_xlabel("Torque (Nm)")
    ax.set_ylabel("Speed (RPM)")
    ax.set_title("DC Shunt Motor: Ideal vs. Realistic")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    st.pyplot(fig)

# --- THEORY ---
st.divider()
st.subheader("📘 Governing Equations")
st.latex(r"T = k \phi I_a")
st.latex(r"N = \frac{V - I_a R_a}{k \phi}")
st.info("👉 Note: The speed decreases linearly with torque due to the armature resistance.")
