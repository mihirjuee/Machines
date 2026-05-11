import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Transformer Simulation", layout="wide")

st.title("⚡ Transformer Phasor Simulation")
st.markdown("Use the **Simulation Step** slider to build the diagram step-by-step.")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🔧 Parameters")
    step = st.slider("Simulation Step", 1, 5, 5, help="1: Secondary, 2: EMFs, 3: Referred Current, 4: Excitation, 5: Primary Total")
    
    a = st.slider("Turns Ratio (a)", 0.5, 3.0, 2.0)
    theta2_deg = st.slider("Secondary PF Angle θ₂ (°)", -60, 70, 30)
    
    st.divider()
    R1, X1 = 0.1, 0.25
    R2, X2 = 0.05, 0.12
    Ic, Im = 0.06, 0.15

# ================= CALCULATIONS =================
theta2 = np.radians(theta2_deg)
origin = 0 + 0j

# 1. Secondary Side
V2 = 1.0 + 0j
I2 = 0.8 * (np.cos(theta2) - 1j * np.sin(theta2))
E2 = V2 + I2 * (R2 + 1j * X2)

# 2. Primary Side (Rotated 180 degrees for clarity)
# We plot -E1 and -V1 so they appear on the left side of the origin
E1_val = a * E2
minus_E1 = -E1_val 

I2_prime = (I2 / a)
# I2_prime is usually drawn in opposition to I2
minus_I2_prime = -I2_prime

# Excitation (aligned with E1)
E1_unit = minus_E1 / np.abs(minus_E1)
Ic_vec = Ic * E1_unit
Im_vec = Im * (E1_unit * -1j)
Iphi = Ic_vec + Im_vec

I1 = minus_I2_prime + Iphi
minus_V1 = minus_E1 + I1 * (R1 + 1j * X1)

# ================= DRAWING UTILITY =================
def add_vector(fig, start, end, label, color, width=3):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode="lines", line=dict(color=color, width=width), name=label
    ))
    fig.add_annotation(
        x=end.real, y=end.imag, ax=start.real, ay=start.imag,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=width, arrowcolor=color
    )

# ================= FIGURE CONSTRUCTION =================
fig = go.Figure()

# STEP 1: Secondary Output
if step >= 1:
    add_vector(fig, origin, V2, "V₂", "green", 4)
    add_vector(fig, origin, I2, "I₂", "orange", 2)
    add_vector(fig, V2, V2 + I2*R2, "I₂R₂", "green")
    add_vector(fig, V2 + I2*R2, E2, "jI₂X₂", "green")

# STEP 2: Induced EMFs
if step >= 2:
    add_vector(fig, origin, E2, "E₂", "#10b981", 3)
    add_vector(fig, origin, minus_E1, "-E₁", "blue", 3)

# STEP 3: Referred Current
if step >= 3:
    add_vector(fig, origin, minus_I2_prime, "I₂'", "#fbbf24")

# STEP 4: Excitation Current
if step >= 4:
    add_vector(fig, origin, Iphi, "I₀", "#94a3b8")
    add_vector(fig, origin, I1, "I₁", "purple", 4)

# STEP 5: Primary Voltage
if step >= 5:
    add_vector(fig, minus_E1, minus_E1 + I1*R1, "I₁R₁", "red")
    add_vector(fig, minus_E1 + I1*R1, minus_V1, "jI₁X₁", "red")
    add_vector(fig, origin, minus_V1, "V₁", "darkblue", 5)

# Style
fig.update_layout(
    height=700, showlegend=False, plot_bgcolor="white",
    xaxis=dict(range=[-max(a,2), 2], zeroline=True, zerolinecolor="black"),
    yaxis=dict(range=[-1.5, 1.5], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="black"),
)

st.plotly_chart(fig, use_container_width=True)

# ================= STEP EXPLANATION =================
steps_text = [
    "**Step 1:** Establish $V_2$ as the reference. Add the secondary impedance drops ($I_2R_2$ and $jI_2X_2$) to find the induced EMF $E_2$.",
    "**Step 2:** Draw the primary EMF $-E_1$ on the opposite side ($180^{\circ}$ shift). Its magnitude is $a \times E_2$.",
    "**Step 3:** Reflect the load current to the primary side as $I_2'$. It acts in opposition to the secondary current to balance MMF.",
    "**Step 4:** Add the no-load current $I_0$ (consisting of magnetizing and core loss components) to $I_2'$ to find the total primary current $I_1$.",
    "**Step 5:** Finally, add the primary internal impedance drops to $-E_1$ to determine the required source voltage $V_1$."
]
st.info(steps_text[step-1])
