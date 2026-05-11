import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")
st.title("⚡ Transformer Phasor Diagram")
st.markdown("## Primary Power Factor = cos θ₁ (angle between V₁ & I₁)")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🔧 Parameters")

    V1 = st.slider("V₁ (pu)", 0.5, 1.5, 1.0)
    I1 = st.slider("I₁ (pu)", 0.2, 1.5, 0.8)

    theta1_deg = st.slider("Power Factor cos θ₁", 0, 70, 30)

    V2 = st.slider("V₂ (pu)", 0.3, 1.5, 0.6)
    I2 = st.slider("I₂ (pu)", 0.2, 1.5, 0.8)

    r1 = st.slider("R₁ (pu)", 0.0, 0.1, 0.02)
    x1 = st.slider("X₁ (pu)", 0.0, 0.2, 0.08)

    r2 = st.slider("R₂ (pu)", 0.0, 0.1, 0.02)
    x2 = st.slider("X₂ (pu)", 0.0, 0.2, 0.08)

    a = st.slider("Turns Ratio a = N₁/N₂", 1.0, 4.0, 2.0)

# ================= CALCULATIONS =================
theta1 = np.radians(theta1_deg)

# Reference axis
phi_axis = complex(1, 0)

# Primary
I1_vec = I1 * np.exp(1j * theta1)
Ic_vec = 0.45 * np.exp(1j * np.radians(20))

V1_vec = complex(0, V1)  # vertical like textbook
I1r1 = I1_vec * r1
jI1x1 = I1_vec * 1j * x1

V1_prime = complex(0.15, V1 * 0.85)

# Secondary
theta2 = np.radians(35)
I2_vec = I2 * np.exp(1j * (np.pi + theta2))

V2_vec = 0.9 * np.exp(1j * np.radians(240))

I2r2 = I2_vec * r2
jI2x2 = I2_vec * 1j * x2

E_common = complex(0, -1.6)

# ================= DRAW FUNCTION =================
def draw_arrow(fig, start, end, label, color, width=4, shiftx=0, shifty=0):
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
        font=dict(size=16, color=color)
    )

# ================= FIGURE =================
fig = go.Figure()
origin = 0 + 0j

# Ø axis
draw_arrow(fig, origin, complex(3.8, 0), "Ø", "#d97706", width=3)

# Primary side
draw_arrow(fig, origin, V1_vec, "V1", "#f97316", shiftx=-0.25)
draw_arrow(fig, origin, I1_vec, "I1", "#1d4ed8", shiftx=0.15)
draw_arrow(fig, origin, Ic_vec, "Ic", "#ea580c", shiftx=0.12)

draw_arrow(fig, origin, V1_prime, "V1′=E1", "#f97316", shiftx=0.2)
draw_arrow(fig, V1_prime, V1_prime + I1r1, "I1r1", "#84cc16", shiftx=0.15)
draw_arrow(fig, V1_prime + I1r1, V1_prime + I1r1 + jI1x1, "jI1X1", "#16a34a", shiftx=0.15)

# Secondary side
draw_arrow(fig, origin, I2_vec, "I2", "#7e22ce", shiftx=-0.2)
draw_arrow(fig, origin, V2_vec, "V2", "#f97316", shiftx=-0.15)

draw_arrow(fig, V2_vec, V2_vec + I2r2, "I2r2", "#84cc16", shiftx=-0.15)
draw_arrow(fig, V2_vec + I2r2, E_common, "jI2X2", "#16a34a", shiftx=-0.15)

# Common E1,E2
draw_arrow(fig, origin, E_common, "E1,E2", "#f97316", width=4, shiftx=0.25)

# ================= ANGLES =================
theta_arc = np.linspace(np.pi/2 - theta1, np.pi/2, 40)
fig.add_trace(go.Scatter(
    x=0.45 * np.cos(theta_arc),
    y=0.45 * np.sin(theta_arc),
    mode="lines",
    line=dict(color="gray", width=2)
))
fig.add_annotation(x=0.35, y=0.55, text="θ1", showarrow=False, font=dict(size=15))

alpha_arc = np.linspace(0, np.radians(20), 40)
fig.add_trace(go.Scatter(
    x=0.7 * np.cos(alpha_arc),
    y=0.7 * np.sin(alpha_arc),
    mode="lines",
    line=dict(color="gray", width=2)
))
fig.add_annotation(x=0.85, y=0.15, text="α", showarrow=False, font=dict(size=15))

theta2_arc = np.linspace(np.radians(215), np.radians(240), 40)
fig.add_trace(go.Scatter(
    x=0.55 * np.cos(theta2_arc),
    y=0.55 * np.sin(theta2_arc),
    mode="lines",
    line=dict(color="gray", width=2)
))
fig.add_annotation(x=-0.45, y=-0.45, text="θ2", showarrow=False, font=dict(size=15))

# ================= STYLE =================
fig.update_layout(
    template="plotly_white",
    xaxis=dict(
        range=[-2.5, 4.2],
        zeroline=False,
        showgrid=False,
        visible=False
    ),
    yaxis=dict(
        range=[-2.2, 2.4],
        zeroline=False,
        showgrid=False,
        visible=False,
        scaleanchor="x"
    ),
    height=850,
    showlegend=False,
    plot_bgcolor="#f3f4f6",
    paper_bgcolor="#f3f4f6"
)

st.plotly_chart(fig, use_container_width=True)

# ================= INFO =================
st.markdown("### 📘 Legend")
st.markdown("""
- **V₁** = Primary Voltage  
- **I₁** = Primary Current  
- **I₁r₁** = Primary Resistive Drop  
- **jI₁X₁** = Primary Reactive Drop  
- **V₁′ = E₁** = Internal Primary EMF  
- **Ic** = Exciting Current  
- **V₂** = Secondary Voltage  
- **I₂** = Secondary Current  
- **I₂r₂** = Secondary Resistive Drop  
- **jI₂X₂** = Secondary Reactive Drop  
- **E₁ = E₂** = Common Induced EMF  
""")

st.markdown("---")
st.markdown("### θ₁ = angle between V₁ and I₁ (Primary Power Factor Angle)")
st.markdown("### θ₂ = angle between V₂ and I₂")
