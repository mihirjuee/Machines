import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fminbound
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Learn EE: Induction Lab", page_icon="⚡", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); }
[data-testid="stSidebar"] { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Learn EE Interactive")
    st.header("⚙️ Machine Parameters")
    V = st.slider("Voltage (L-L V)", 100, 500, 400)
    f = st.slider("Frequency (Hz)", 10, 100, 50)
    P = st.selectbox("Poles", [2, 4, 6, 8], index=1)
    
    st.divider()
    st.header("⚙️ Equivalent Circuit")
    # Independent sliders for each parameter
    R1 = st.slider("Stator R1 [Ω]", 0.01, 5.0, 0.5)
    X1 = st.slider("Stator X1 [Ω]", 0.1, 5.0, 1.0)
    R2 = st.slider("Rotor R2 [Ω]", 0.01, 5.0, 0.8)
    X2 = st.slider("Rotor X2 [Ω]", 0.1, 5.0, 1.2)
    Xm = st.slider("Magnetizing Xm [Ω]", 5.0, 100.0, 30.0)

# --- ENGINE LOGIC ---
V_ph = V / np.sqrt(3)
Ns = 120 * f / P
omega_s = (2 * np.pi * Ns) / 60
Z_th = ((1j * Xm) * (R1 + 1j * X1)) / (R1 + 1j * (X1 + Xm))
V_th = V_ph * abs((1j * Xm) / (R1 + 1j * (X1 + Xm)))
R_th, X_th = Z_th.real, Z_th.imag

def get_metrics(s):
    # Avoid division by zero
    s = np.where(s == 0, 1e-6, s)
    denom = ((R_th + R2/s)**2 + (X_th + X2)**2)
    torque = (3 * V_th**2 * (R2/s)) / (omega_s * denom)
    return torque

# --- MAIN CONTENT ---
st.title("⚡ Induction Machine: Four-Quadrant Analysis")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔌 Equivalent Circuit")
    d = schemdraw.Drawing()
    d.add(elm.SourceV().label("V₁"))
    d.add(elm.Resistor().label("R₁"))
    d.add(elm.Inductor().label("X₁"))
    d.add(elm.Inductor().at((2,1)).label("Xm").down())
    d.add(elm.Resistor().at((4,0)).label("R₂/s").right())
    d.add(elm.Inductor().label("X₂"))
    st.pyplot(d.draw())
    

with col2:
    # Analyze across full slip range (-1 to 2)
    s_plot = np.linspace(-1.0, 2.0, 500)
    T_plot = get_metrics(s_plot)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(s_plot, T_plot, 'r-', lw=2)
    # Fill zones
    ax.fill_between(s_plot, T_plot, 0, where=(s_plot < 0), color='green', alpha=0.2, label="Generating Zone (s < 0)")
    ax.fill_between(s_plot, T_plot, 0, where=(s_plot >= 0) & (s_plot <= 1), color='blue', alpha=0.2, label="Motoring Zone (0 < s < 1)")
    ax.fill_between(s_plot, T_plot, 0, where=(s_plot > 1), color='orange', alpha=0.2, label="Braking Zone (s > 1)")
    
    ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
    ax.set_xlabel("Slip (s)"); ax.set_ylabel("Torque (Nm)"); ax.legend()
    st.pyplot(fig)
    

# --- DYNAMIC ANALYSIS ---
st.subheader("🔍 Interactive Load Analysis")
load_t = st.slider("Apply Load Torque (Nm)", -100.0, 200.0, 50.0)
def obj(s): return abs(get_metrics(s) - load_t)
op_slip = fminbound(obj, -0.5, 1.5)

cols = st.columns(3)
cols[0].metric("Operating Slip", f"{op_slip:.4f}")
cols[1].metric("Rotor Speed", f"{Ns*(1-op_slip):.0f} RPM")
cols[2].metric("Machine Mode", "Generating" if op_slip < 0 else ("Braking" if op_slip > 1 else "Motoring"))
