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
    st.sidebar.subheader("⚡ Armature Reaction")
demag_factor = st.sidebar.slider("Demagnetization Factor", 0.0, 0.02, 0.005)

# --- MAIN SECTION ---
st.subheader("📊 Torque vs Speed (Realistic)")

# Torque range
T = np.linspace(0, 50, 100)

# --- Iterative solution for Ia and phi_eff ---
Ia = T / (k * phi)  # initial guess

for _ in range(5):  # iterative refinement
    phi_eff = np.maximum(phi - demag_factor * Ia, 0.1)
    Ia = T / (k * phi_eff)

# Final speed calculation
N = (V - Ia * Ra) / (k * phi_eff)
N = np.maximum(N, 0)

# --- Ideal case (no armature reaction) ---
Ia_ideal = T / (k * phi)
N_ideal = (V - Ia_ideal * Ra) / (k * phi)

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(T, N, linewidth=2.5, label='Actual (With Armature Reaction)')
ax.plot(T, N_ideal, linestyle='--', label='Ideal (No Armature Reaction)')

ax.set_xlabel("Torque (Nm)")
ax.set_ylabel("Speed (RPM)")
ax.set_title("DC Shunt Motor: Torque vs Speed Characteristics")

ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

st.pyplot(fig)

# --- THEORY ---
st.divider()
st.subheader("📘 Governing Equations")
st.latex(r"T = k \phi I_a")
st.latex(r"N = \frac{V - I_a R_a}{k \phi}")
st.info("👉 Note: The speed decreases linearly with torque due to the armature resistance.")
