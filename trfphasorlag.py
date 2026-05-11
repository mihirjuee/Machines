import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")
st.title("⚡ Transformer Phasor Diagram (Clear Vector Construction)")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.main {
    background-color: #eaf6ff;
}
</style>
""", unsafe_allow_html=True)

# ================= INPUTS =================
with st.sidebar:
    st.header("🔧 Parameters")

    V2 = st.slider("V₂ (pu)", 0.5, 1.5, 1.0)
    I2 = st.slider("I₂ (pu)", 0.2, 1.5, 0.8)
    phi_deg = st.slider("Power Factor Angle φ (lagging)", 0, 70, 30)

    R2 = st.slider("R₂", 0.0, 0.3, 0.1)
    X2 = st.slider("X₂", 0.0, 0.5, 0.2)

    a = st.slider("Turns Ratio a = N₁/N₂", 1.0, 3.0, 2.0)

    Ic = st.slider("Ic", 0.0, 0.2, 0.05)
    Im = st.slider("Im", 0.0, 0.3, 0.15)

    step = st.slider("Construction Step", 1, 10, 10)

# ================= CALCULATIONS =================
phi = np.radians(phi_deg)

# Reference vectors
V2_vec = complex(V2, 0)
I2_vec = I2 * np.exp(-1j * phi)

# Voltage drops
IR2 = I2_vec * R2
IX2 = I2_vec * 1j * X2

# Secondary induced emf
E2_vec = V2_vec + IR2 + IX2

# Primary induced emf
E1_vec = a * E2_vec

# Referred current
I2_prime = I2_vec / a

# No-load current
I0_vec = complex(Ic, -Im)

# Primary current
I1_vec = I2_prime + I0_vec

# Approximate primary voltage
V1_vec = E1_vec

# ================= DRAW FUNCTION =================
def draw_arrow(fig, start, end, name, color):
    # Main line
    fig.add_trace(go.Scatter(
        x=[start.real, end.real],
        y=[start.imag, end.imag],
        mode='lines',
        line=dict(color=color, width=5)
    ))

    # Arrowhead
    fig.add_annotation(
        ax=start.real,
        ay=start.imag,
        x=end.real,
        y=end.imag,
        showarrow=True,
        arrowhead=4,
        arrowsize=1.6,
        arrowwidth=3,
        arrowcolor=color
    )

    # Label
    fig.add_annotation(
        x=end.real,
        y=end.imag,
        text=f"<b>{name}</b>",
        showarrow=False,
        font=dict(size=16, color=color),
        bgcolor="white",
        bordercolor=color,
        borderwidth=1,
        yshift=18
    )

# ================= PLOT =================
fig = go.Figure()

origin = 0 + 0j

# -------- SECONDARY SIDE --------
if step >= 1:
    draw_arrow(fig, origin, V2_vec, "V₂", "black")

if step >= 2:
    draw_arrow(fig, origin, I2_vec, "I₂", "blue")

if step >= 3:
    draw_arrow(fig, V2_vec, V2_vec + IR2, "I₂R₂", "green")

if step >= 4:
    draw_arrow(fig, V2_vec + IR2, E2_vec, "jI₂X₂", "orange")

if step >= 5:
    draw_arrow(fig, origin, E2_vec, "E₂", "purple")

# -------- PRIMARY SIDE --------
if step >= 6:
    draw_arrow(fig, origin, E1_vec, "E₁", "red")

if step >= 7:
    draw_arrow(fig, origin, I2_prime, "I₂′", "brown")

if step >= 8:
    draw_arrow(fig, origin, I0_vec, "I₀", "magenta")

if step >= 9:
    draw_arrow(fig, origin, I1_vec, "I₁", "darkblue")

if step >= 10:
    draw_arrow(fig, origin, V1_vec, "V₁", "black")

# Origin
fig.add_trace(go.Scatter(
    x=[0],
    y=[0],
    mode='markers',
    marker=dict(size=10, color='black')
))

# ================= STYLE =================
fig.update_layout(
    template="plotly_white",
    xaxis=dict(
        title="Real Axis",
        range=[-4, 4],
        zeroline=True,
        zerolinewidth=3,
        zerolinecolor='black',
        showgrid=True,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        title="Imaginary Axis",
        range=[-4, 4],
        zeroline=True,
        zerolinewidth=3,
        zerolinecolor='black',
        showgrid=True,
        gridcolor='lightgray',
        scaleanchor="x"
    ),
    height=700,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ================= FORMULAS =================
st.subheader("📘 Key Equations")
st.latex(r"E_2 = V_2 + I_2R_2 + jI_2X_2")
st.latex(r"E_1 = aE_2")
st.latex(r"I_1 = I_2' + I_0")

# ================= STEP EXPLANATION =================
st.subheader("🧠 Step Explanation")

steps = {
    1: "V₂ is taken as the reference phasor.",
    2: "I₂ lags V₂ by power factor angle φ.",
    3: "Voltage drop I₂R₂ is added in phase with I₂.",
    4: "Reactive drop jI₂X₂ is added 90° ahead of I₂.",
    5: "E₂ is obtained by vector sum.",
    6: "E₁ = aE₂ (referred to primary side).",
    7: "I₂′ is secondary current referred to primary.",
    8: "I₀ consists of Ic and Im.",
    9: "I₁ = I₂′ + I₀.",
    10: "V₁ ≈ E₁ for ideal transformer."
}

st.info(steps[step])

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🎓 Designed for Electrical Engineering Visualization")
st.markdown("Understand • Construct • Visualize ⚡")
