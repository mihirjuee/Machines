import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")
st.title("⚡ Transformer Phasor Diagram (Textbook Style)")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🔧 Parameters")

    V2 = st.slider("Secondary Voltage V₂ (pu)", 0.5, 1.5, 1.0)
    I2 = st.slider("Secondary Current I₂ (pu)", 0.2, 1.5, 0.8)
    phi_deg = st.slider("Power Factor Angle φ (lagging)", 0, 70, 30)

    R2 = st.slider("Secondary Resistance R₂", 0.0, 0.3, 0.1)
    X2 = st.slider("Secondary Reactance X₂", 0.0, 0.5, 0.2)

    a = st.slider("Turns Ratio a = N₁/N₂", 1.0, 4.0, 2.0)

# ================= CALCULATIONS =================
phi = np.radians(phi_deg)

# Secondary side
V2_vec = complex(V2, 0)
I2_vec = I2 * np.exp(-1j * phi)

IR2 = I2_vec * R2
IX2 = I2_vec * 1j * X2

E2_vec = V2_vec + IR2 + IX2

# Primary side (different scale)
E1_vec = a * E2_vec
I2_prime = I2_vec / a

# ================= DRAW FUNCTION =================
def draw_vector(fig, start, end, label, color, width=4, label_shift=18):
    # Main line
    fig.add_trace(go.Scatter(
        x=[start.real, end.real],
        y=[start.imag, end.imag],
        mode="lines",
        line=dict(color=color, width=width)
    ))

    # Arrow head
    fig.add_annotation(
        x=end.real,
        y=end.imag,
        ax=start.real,
        ay=start.imag,
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=2.5,
        arrowcolor=color
    )

    # Label
    fig.add_annotation(
        x=end.real,
        y=end.imag,
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=15, color=color),
        bgcolor="white",
        yshift=label_shift
    )

# ================= FIGURE =================
fig = go.Figure()

# ---------------- SECONDARY SIDE (LEFT) ----------------
secondary_origin = complex(-3.5, 0)

draw_vector(fig, secondary_origin, secondary_origin + V2_vec, "V₂", "black")
draw_vector(fig, secondary_origin, secondary_origin + I2_vec, "I₂", "blue")

draw_vector(
    fig,
    secondary_origin + V2_vec,
    secondary_origin + V2_vec + IR2,
    "I₂R₂",
    "green"
)

draw_vector(
    fig,
    secondary_origin + V2_vec + IR2,
    secondary_origin + E2_vec,
    "jI₂X₂",
    "orange"
)

draw_vector(fig, secondary_origin, secondary_origin + E2_vec, "E₂", "purple", width=5)

# ---------------- PRIMARY SIDE (RIGHT) ----------------
primary_origin = complex(3.5, 0)

draw_vector(fig, primary_origin, primary_origin + E1_vec, "E₁", "red", width=5)
draw_vector(fig, primary_origin, primary_origin + I2_prime, "I₂′", "brown")

# ---------------- DIVIDER LINE ----------------
fig.add_shape(
    type="line",
    x0=0,
    y0=-4,
    x1=0,
    y1=4,
    line=dict(color="gray", dash="dash", width=3)
)

# ---------------- LABELS ----------------
fig.add_annotation(
    x=-3.5,
    y=3.8,
    text="<b>SECONDARY SIDE</b>",
    showarrow=False,
    font=dict(size=18, color="black")
)

fig.add_annotation(
    x=3.5,
    y=3.8,
    text="<b>PRIMARY SIDE</b>",
    showarrow=False,
    font=dict(size=18, color="black")
)

# ================= AXES =================
fig.update_layout(
    template="plotly_white",
    xaxis=dict(
        title="Real Axis",
        range=[-8, 8],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title="Imaginary Axis",
        range=[-4, 4],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        showgrid=True,
        gridcolor="lightgray",
        scaleanchor="x"
    ),
    height=750,
    showlegend=False
)

# ================= DISPLAY =================
st.plotly_chart(fig, use_container_width=True)

# ================= THEORY =================
st.subheader("📘 Textbook Construction Steps")
st.markdown("""
**Secondary Side:**  
1. Draw V₂ as reference  
2. Draw I₂ lagging by φ  
3. Add I₂R₂ in phase with I₂  
4. Add jI₂X₂ perpendicular to I₂  
5. Result gives E₂  

**Primary Side:**  
6. E₁ = aE₂ (scaled by turns ratio)  
7. I₂′ = I₂/a  
""")

st.latex(r"E_2 = V_2 + I_2R_2 + jI_2X_2")
st.latex(r"E_1 = aE_2")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🎓 Textbook Style Transformer Phasor Diagram")
st.markdown("Primary and Secondary shown separately for clear conceptual understanding ⚡")
