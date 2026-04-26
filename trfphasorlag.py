import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")
st.title("⚡ Transformer Phasor Diagram: Full Construction")

# ================= INPUTS =================
with st.sidebar:
    st.header("🔧 Parameters")
    V2 = st.slider("V₂ (pu)", 0.5, 1.5, 1.0)
    I2 = st.slider("I₂ (pu)", 0.2, 1.2, 0.8)
    phi_deg = st.slider("Load PF Angle (deg)", 0, 70, 30)
    a = st.slider("Turns Ratio (N₁/N₂)", 1.0, 3.0, 2.0)
    step = st.slider("Construction Step", 1, 7, 1)

# ================= CALCULATIONS =================
phi = np.radians(phi_deg)
V2_vec = complex(V2, 0)
I2_vec = complex(I2 * np.cos(-phi), I2 * np.sin(-phi))

# Secondary Drops & EMF
E2_vec = V2_vec + I2_vec * (0.1 + 1j * 0.2)
# Primary Side
E1_vec = E2_vec * a
I1_vec = (-I2_vec / a) + 0.1j # Including magnetizing component
V1_vec = -E1_vec + I1_vec * (0.05 + 1j * 0.1)

# ================= PLOTTING ENGINE =================
def draw_arrow(fig, start, end, name, color):
    # Draw vector line
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode='lines', line=dict(color=color, width=4)
    ))
    # Draw arrow head
    fig.add_annotation(
        ax=start.real, ay=start.imag, x=end.real, y=end.imag,
        showarrow=True, arrowhead=2, arrowsize=2.5, arrowwidth=3, arrowcolor=color
    )
    # Label
    fig.add_annotation(
        x=end.real, y=end.imag, text=f"<b>{name}</b>", 
        showarrow=False, font=dict(color=color, size=18),
        yshift=25
    )

fig = go.Figure()
origin = complex(0, 0)

# Step-by-Step Construction
if step >= 1: draw_arrow(fig, origin, V2_vec, "V₂", "black")
if step >= 2: draw_arrow(fig, origin, I2_vec, "I₂", "blue")
if step >= 3: draw_arrow(fig, V2_vec, E2_vec, "Drops", "red")
if step >= 4: draw_arrow(fig, origin, E2_vec, "E₂", "black")
if step >= 5: draw_arrow(fig, origin, -E1_vec, "-E₁", "purple")
if step >= 6: draw_arrow(fig, -E1_vec, V1_vec, "I₁Z₁", "darkred")
if step >= 7: draw_arrow(fig, origin, V1_vec, "V₁", "black")

# Textbook Layout Styling
fig.update_layout(
    template="plotly_white",
    xaxis=dict(range=[-2.5, 2.5], zeroline=True, zerolinecolor='black', showgrid=True),
    yaxis=dict(range=[-2, 2.5], zeroline=True, zerolinecolor='black', showgrid=True, scaleanchor="x"),
    margin=dict(l=50, r=50, t=50, b=50),
    height=650, showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ================= PEDAGOGICAL NOTE =================
st.info(f"**Current Step: {step}** — Observe how the phasor relationships shift as you adjust the parameters in the sidebar.")
