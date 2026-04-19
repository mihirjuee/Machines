import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #e3f2fd, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="DC Series Motor", layout="wide")
st.title("⚡ DC Series Motor Torque-Speed Characteristics")

col1, col2 = st.columns([1, 1])

# --- SIDEBAR INPUTS ---
st.sidebar.image("logo.png", use_container_width=True)
V = st.sidebar.slider("Supply Voltage (V)", 100, 300, 220)
Ra_Rs = st.sidebar.slider("Total Resistance (Ra + Rs) (Ohm)", 0.1, 5.0, 1.0)
Kt = st.sidebar.slider("Torque Constant (Kt)", 0.1, 1.0, 0.5)
Kb = st.sidebar.slider("Back EMF Constant (Kb)", 0.1, 1.0, 0.5)

# --- CIRCUIT DIAGRAM ---
with col1:
    st.subheader("🔌 DC Series Motor Circuit")
    d = schemdraw.Drawing()
    d += elm.SourceV().label(f"{V}V")
    d += elm.Line().up(length=1)
    d += elm.Line().right(length=2)
    
    # Series combination: Field + Armature
    d += elm.Inductor().label("Rs")
    d += elm.Resistor().label("Ra")
    d += elm.Motor().label("M")
    
    d += elm.Line().down(length=4)
    d += elm.Line().left(length=11)
    
    st.pyplot(d.draw().fig)



#[Image of a basic DC series motor circuit diagram]


# --- GRAPH ---
with col2:
    st.subheader("📊 Torque vs Speed")
    T = np.linspace(5, 50, 100)
    Ia = np.sqrt(T / Kt)
    N = (V - Ia * Ra_Rs) / (Kb * Ia)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(T, N, color='red', linewidth=2)
    ax.set_xlabel("Torque (Nm)")
    ax.set_ylabel("Speed (RPM)")
    ax.set_title("Speed-Torque Characteristic")
    ax.grid(True, linestyle='--')
    st.pyplot(fig)

# --- THEORY ---
st.divider()
st.subheader("📘 Governing Equations")
st.latex(r"T = K_t I_a^2")
st.latex(r"N = \frac{V - I_a(R_a + R_s)}{K_b I_a}")
st.info("⚠️ Safety Note: Series motors exhibit extremely high speeds at light loads. They should always be connected directly to their load.")
