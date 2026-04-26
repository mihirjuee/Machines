import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Textbook Transformer Phasor (Primary/Secondary)", layout="wide")
st.title("⚡ Transformer Phasor Diagram (Complete)")

# ================= INPUTS =================
with st.sidebar:
    st.header("🔧 Parameters")
    V2 = st.slider("V₂ (pu)", 0.5, 1.5, 1.0)
    I2 = st.slider("I₂ (pu)", 0.1, 1.5, 0.8)
    phi_deg = st.slider("Load PF Angle (deg)", 0, 80, 30)
    a = st.slider("Turns Ratio (N₁/N₂)", 1.0, 3.0, 2.0)
    R1 = st.slider("Primary Resistance (R₁)", 0.0, 0.2, 0.05)
    X1 = st.slider("Primary Reactance (X₁)", 0.0, 0.2, 0.1)
    step = st.slider("Construction Step", 1, 10, 1)

# ================= CALCULATIONS =================
phi = np.radians(phi_deg)
V2_vec = complex(V2, 0)
I2_vec = V2_vec * np.exp(-1j * phi) / V2 # Scaled current
# Simple secondary drops
E2_vec = V2_vec + I2_vec * (0.1 + 1j * 0.2)
# Primary side
E1_vec = E2_vec * a
I2_prime = -I2_vec / a  # Reflected current
I1_vec = I2_prime + (0.1j) # Adding a small magnetizing component
V1_vec = -E1_vec + I1_vec * (R1 + 1j * X1)

# ================= PLOTTING =================
fig = go.Figure()

def add_vec(fig, start, end, name, color, dash="solid"):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode='lines', line=dict(color=color, width=3, dash=dash),
        name=name
    ))
    fig.add_annotation(x=end.real, y=end.imag, text=name, showarrow=True, arrowhead=2)

origin = complex(0,0)
# Secondary
if step >= 1: add_vec(fig, origin, V2_vec, "V₂", "black")
if step >= 2: add_vec(fig, origin, I2_vec, "I₂", "blue")
if step >= 3: add_vec(fig, V2_vec, E2_vec, "Drops (sec)", "red", "dash")
if step >= 4: add_vec(fig, origin, E2_vec, "E₂", "black")

# Primary
if step >= 5: add_vec(fig, origin, -E1_vec, "-E₁", "grey", "dot")
if step >= 6: add_vec(fig, -E1_vec, -E1_vec + I1_vec*R1, "I₁R₁", "brown")
if step >= 7: add_vec(fig, -E1_vec + I1_vec*R1, V1_vec, "I₁X₁", "green")
if step >= 8: add_vec(fig, origin, V1_vec, "V₁", "black")

fig.update_layout(
    template="plotly_white",
    xaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor='black'),
    yaxis=dict(range=[-2, 3], zeroline=True, zerolinecolor='black', scaleanchor="x"),
    height=600, showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
