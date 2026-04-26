import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Textbook Transformer Phasor", layout="wide")
st.title("⚡ Transformer Phasor Diagram (Lagging Load)")
st.markdown("A step-by-step interactive textbook guide.")

# ================= INPUTS =================
with st.sidebar:
    st.header("🔧 Transformer Parameters")
    V2 = st.slider("V₂ (pu)", 0.5, 1.5, 1.0)
    I2 = st.slider("I₂ (pu)", 0.1, 1.5, 0.8)
    phi_deg = st.slider("Load Power Factor Angle (deg)", 0, 80, 30)
    
    R = st.slider("Secondary Resistance (R₂)", 0.0, 0.3, 0.1)
    X = st.slider("Secondary Reactance (X₂)", 0.0, 0.3, 0.2)
    a = st.slider("Turns Ratio (a = N₁/N₂)", 1.0, 3.0, 2.0)
    
    step = st.slider("Construction Step", 1, 5, 1)

# ================= CALCULATIONS =================
phi = np.radians(phi_deg)
V2_vec = complex(V2, 0)
I2_vec = complex(I2 * np.cos(-phi), I2 * np.sin(-phi))

# Voltage Drops
IR2_vec = I2_vec * R
IX2_vec = I2_vec * 1j * X
E2_vec = V2_vec + IR2_vec + IX2_vec

# Primary (Referenced)
E1_vec = E2_vec * a

# ================= PLOTTING ENGINE =================
def add_vector(fig, start, end, name, color, dash="solid"):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode='lines+markers',
        line=dict(color=color, width=3, dash=dash),
        name=name
    ))
    # Add arrow annotation
    fig.add_annotation(
        x=end.real, y=end.imag, text=name,
        showarrow=True, arrowhead=2, ax=10, ay=-10, font=dict(size=12)
    )

fig = go.Figure()

# Logic for step-by-step textbook construction
origin = complex(0, 0)
if step >= 1: add_vector(fig, origin, V2_vec, "V₂", "black")
if step >= 2: add_vector(fig, origin, I2_vec, "I₂", "blue")
if step >= 3: add_vector(fig, V2_vec, V2_vec + IR2_vec, "I₂R₂", "red")
if step >= 4: add_vector(fig, V2_vec + IR2_vec, E2_vec, "I₂X₂", "green")
if step >= 5: add_vector(fig, origin, E2_vec, "E₂", "black")

# Textbook Layout
fig.update_layout(
    template="plotly_white",
    xaxis=dict(range=[-0.5, 2.5], zeroline=True, zerolinecolor='black'),
    yaxis=dict(range=[-1, 1.5], zeroline=True, zerolinecolor='black', scaleanchor="x", scaleratio=1),
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ================= EDUCATIONAL GUIDE =================
st.info(f"**Step {step}:** " + {
    1: "Draw the terminal voltage V₂ on the real axis as the reference.",
    2: "Draw the load current I₂ lagging V₂ by the power factor angle φ.",
    3: "Add the resistive voltage drop I₂R₂ in phase with the current I₂.",
    4: "Add the inductive drop I₂X₂ at a 90° leading angle to I₂.",
    5: "The resultant vector from the origin to the tip of I₂X₂ is the induced EMF E₂."
}[step])

st.markdown("---")
st.latex(r"E_2 = V_2 + I_2(R_2 + jX_2)")
