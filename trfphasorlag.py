import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")
st.title("⚡ The Phasor Diagram of the Transformer")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🔧 Parameters")

    V2_mag = st.slider("V₂ Magnitude", 0.5, 1.5, 1.0)
    I2_mag = st.slider("I₂ Magnitude", 0.2, 1.5, 0.8)

    theta2_deg = st.slider("Secondary PF Angle θ₂", 0, 70, 30)

    R1 = st.slider("R₁", 0.0, 0.3, 0.1)
    X1 = st.slider("X₁", 0.0, 0.5, 0.2)

    R2 = st.slider("R₂", 0.0, 0.3, 0.1)
    X2 = st.slider("X₂", 0.0, 0.5, 0.2)

    Ic = st.slider("Ic", 0.0, 0.3, 0.08)
    Im = st.slider("Im", 0.0, 0.4, 0.18)

    a = st.slider("Turns Ratio a=N₁/N₂", 1.0, 4.0, 2.0)

# ================= CALCULATIONS =================
theta2 = np.radians(theta2_deg)

origin = 0 + 0j

# Secondary voltage reference
V2 = V2_mag + 0j

# Secondary current lags
I2 = I2_mag * np.exp(-1j * theta2)

# Secondary drops
I2R2 = I2 * R2
jI2X2 = I2 * 1j * X2

# Secondary induced emf
E2 = V2 + I2R2 + jI2X2

# Primary emf
E1 = a * E2

# Referred current
I2_prime = I2 / a

# Exciting current
Ic_vec = Ic + 0j
Im_vec = -1j * Im
Iphi = Ic_vec + Im_vec

# Primary current
I1 = I2_prime + Iphi

# Primary drops
I1R1 = I1 * R1
jI1X1 = I1 * 1j * X1

# Primary voltage
V1 = E1 + I1R1 + jI1X1

# ================= DRAW FUNCTION =================
def draw_arrow(fig, start, end, label, color, width=4, size=16, shiftx=0, shifty=0):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real],
        y=[start.imag, end.imag],
        mode="lines",
        line=dict(color=color, width=width)
    ))

    fig.add_annotation(
        x=end.real,
        y=end.imag,
        ax=start.real,
        ay=start.imag,
        showarrow=True,
        arrowhead=3,
        arrowsize=1.4,
        arrowwidth=2.5,
        arrowcolor=color
    )

    fig.add_annotation(
        x=end.real + shiftx,
        y=end.imag + shifty,
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=size, color=color)
    )

# ================= FIGURE =================
fig = go.Figure()

# -------- CURRENT TRIANGLE (BOTTOM LEFT) --------
draw_arrow(fig, origin, Ic_vec, "Ic", "#f59e0b", shiftx=0.1)
draw_arrow(fig, origin, Im_vec, "Im", "#eab308", shiftx=-0.2)
draw_arrow(fig, origin, Iphi, "Iϕ", "#fbbf24", shiftx=0.1)
draw_arrow(fig, origin, I2, "I₂", "#16a34a", shiftx=0.1)
draw_arrow(fig, origin, I1, "I₁", "#ef4444", shiftx=0.1)
draw_arrow(fig, origin, I2_prime, "Ip", "#15803d", shiftx=0.1)

# -------- SECONDARY PHASOR CONSTRUCTION --------
secondary_origin = complex(0, 0)

draw_arrow(fig, secondary_origin, V2, "V₂", "#2563eb", width=5, shifty=-0.25)

draw_arrow(fig, V2, V2 + I2R2, "I₂R₂", "#65a30d", shiftx=0.1)

draw_arrow(fig, V2 + I2R2, E2, "jI₂X₂", "#16a34a", shiftx=0.1)

draw_arrow(fig, secondary_origin, E2, "E₂", "#4ade80", width=5, shifty=0.2)

# -------- PRIMARY PHASOR CONSTRUCTION --------
draw_arrow(fig, secondary_origin, E1, "E₁", "#1d4ed8", width=5, shifty=0.25)

draw_arrow(fig, E1, E1 + I1R1, "I₁R₁", "#ef4444", shiftx=0.1)

draw_arrow(fig, E1 + I1R1, V1, "jI₁X₁", "#dc2626", shiftx=0.1)

draw_arrow(fig, secondary_origin, V1, "V₁", "#2563eb", width=6, shifty=0.3)

# ================= ANGLES =================
theta_arc = np.linspace(-theta2, 0, 40)
fig.add_trace(go.Scatter(
    x=0.8 * np.cos(theta_arc),
    y=0.8 * np.sin(theta_arc),
    mode="lines",
    line=dict(color="gray", dash="dot")
))
fig.add_annotation(x=0.65, y=-0.2, text="θ₂", showarrow=False)

theta1 = np.angle(I1)
theta1_arc = np.linspace(theta1, 0, 40)
fig.add_trace(go.Scatter(
    x=1.0 * np.cos(theta1_arc),
    y=1.0 * np.sin(theta1_arc),
    mode="lines",
    line=dict(color="gray", dash="dot")
))
fig.add_annotation(x=0.85, y=0.25, text="θ₁", showarrow=False)

# ================= EQUATION BOX =================
st.markdown("### 📘 Key Equations")
st.latex(r"\frac{E_1}{E_2} = \frac{I_2}{I_p} = \frac{N_1}{N_2} = a")
st.latex(r"V_1 = E_1 + I_1(R_1 + jX_1)")
st.latex(r"V_2 = E_2 - I_2(R_2 + jX_2)")

# ================= STYLE =================
fig.update_layout(
    xaxis=dict(
        visible=False,
        range=[-1.5, max(V1.real + 1.5, 6)]
    ),
    yaxis=dict(
        visible=False,
        range=[min(Im_vec.imag - 1.0, -2.5), max(V1.imag + 1.0, 3.5)],
        scaleanchor="x"
    ),
    height=850,
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ================= THEORY =================
st.markdown("### 🧠 Construction Steps")
st.markdown("""
1. Take **V₂** as reference.  
2. Draw **I₂** lagging by θ₂.  
3. Add **I₂R₂** in phase with I₂.  
4. Add **jI₂X₂** perpendicular to I₂.  
5. Obtain **E₂**.  
6. Scale to get **E₁ = aE₂**.  
7. Draw **Ic** and **Im** to form **Iϕ**.  
8. Add **Ip + Iϕ = I₁**.  
9. Add **I₁R₁** and **jI₁X₁** to get **V₁**.  
""")

st.markdown("---")
st.markdown("### 🎓 Complete Textbook-Style Transformer Phasor Diagram")
st.markdown("Voltage • Current • EMF • Drops • Power Factor ⚡")
