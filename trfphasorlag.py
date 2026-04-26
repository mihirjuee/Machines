import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")
st.title("⚡ Transformer Phasor Diagram (Full - Corrected)")

# ================= INPUTS =================
with st.sidebar:
    st.header("🔧 Parameters")

    V2 = st.slider("V₂ (pu)", 0.5, 1.5, 1.0)
    I2 = st.slider("I₂ (pu)", 0.2, 1.2, 0.8)
    phi_deg = st.slider("Power Factor Angle (lagging)", 0, 70, 30)

    R2 = st.slider("R₂", 0.0, 0.3, 0.1)
    X2 = st.slider("X₂", 0.0, 0.5, 0.2)

    a = st.slider("Turns Ratio (N₁/N₂)", 1.0, 3.0, 2.0)

    Ic = st.slider("Core Loss Current Ic", 0.0, 0.2, 0.05)
    Im = st.slider("Magnetizing Current Im", 0.0, 0.3, 0.15)

    step = st.slider("Construction Step", 1, 10, 1)

# ================= CALCULATIONS =================
phi = np.radians(phi_deg)

# Secondary
V2_vec = complex(V2, 0)
I2_vec = I2 * np.exp(-1j * phi)

# Voltage drops
IR2 = I2_vec * R2
IX2 = I2_vec * 1j * X2

E2_vec = V2_vec + IR2 + IX2

# Refer to primary
E1_vec = a * E2_vec
I2_prime = I2_vec / a

# No-load current
I0_vec = complex(Ic, -Im)  # Ic in phase, Im lagging

# Primary current
I1_vec = I2_prime + I0_vec

# Primary voltage (approx)
V1_vec = E1_vec

# ================= DRAW FUNCTION =================
def draw_arrow(fig, start, end, name, color):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real],
        y=[start.imag, end.imag],
        mode='lines',
        line=dict(color=color, width=4)
    ))

    fig.add_annotation(
        ax=start.real, ay=start.imag,
        x=end.real, y=end.imag,
        showarrow=True,
        arrowhead=3,
        arrowwidth=2.5,
        arrowcolor=color
    )

    fig.add_annotation(
        x=end.real, y=end.imag,
        text=f"<b>{name}</b>",
        showarrow=False,
        font=dict(color=color, size=16),
        yshift=20
    )

# ================= PLOT =================
fig = go.Figure()
origin = 0 + 0j

# ---- SECONDARY ----
if step >= 1: draw_arrow(fig, origin, V2_vec, "V₂", "black")
if step >= 2: draw_arrow(fig, origin, I2_vec, "I₂", "blue")
if step >= 3: draw_arrow(fig, V2_vec, V2_vec + IR2, "I₂R₂", "green")
if step >= 4: draw_arrow(fig, V2_vec + IR2, E2_vec, "jI₂X₂", "orange")
if step >= 5: draw_arrow(fig, origin, E2_vec, "E₂", "black")

# ---- PRIMARY ----
if step >= 6: draw_arrow(fig, origin, E1_vec, "E₁", "purple")
if step >= 7: draw_arrow(fig, origin, I2_prime, "I₂'", "red")
if step >= 8: draw_arrow(fig, origin, I0_vec, "I₀", "brown")
if step >= 9: draw_arrow(fig, origin, I1_vec, "I₁", "darkblue")
if step >= 10: draw_arrow(fig, origin, V1_vec, "V₁ ≈ E₁", "black")

# ================= STYLE =================
fig.update_layout(
    template="plotly_white",
    xaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor='black'),
    yaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor='black', scaleanchor="x"),
    height=650,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ================= STEP EXPLANATION =================
st.subheader("🧠 Step Explanation")

steps = {
    1: "Draw V₂ as reference.",
    2: "Draw I₂ lagging V₂ by φ.",
    3: "Add I₂R₂ (in phase with I₂).",
    4: "Add jI₂X₂ (90° leading I₂).",
    5: "Resultant gives E₂.",
    6: "Refer to primary → E₁ = aE₂.",
    7: "Refer current → I₂'.",
    8: "Add no-load current I₀ (Ic + jIm).",
    9: "Sum → I₁ = I₂' + I₀.",
    10:"Primary voltage V₁ ≈ E₁."
}

st.info(steps[step])
