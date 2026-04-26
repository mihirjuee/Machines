import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Transformer Phasor Diagram (Full)", layout="wide")
st.title("⚡ Transformer Phasor Diagram (Lagging Load - Full)")

# ================= INPUT =================
st.sidebar.header("🔧 Inputs")

V2 = st.sidebar.slider("V₂ (pu)", 0.5, 1.5, 1.0)
I2 = st.sidebar.slider("I₂ (pu)", 0.1, 1.5, 1.0)
phi_deg = st.sidebar.slider("Power Factor Angle (lagging)", 0, 80, 30)

R = st.sidebar.slider("Secondary Resistance R₂", 0.0, 0.5, 0.1)
X = st.sidebar.slider("Secondary Reactance X₂", 0.0, 0.5, 0.2)

a = st.sidebar.slider("Turns Ratio (N₁/N₂)", 1.0, 5.0, 2.0)

I0 = st.sidebar.slider("No-load current I₀ (pu)", 0.0, 0.5, 0.1)
theta0_deg = st.sidebar.slider("I₀ angle (lagging)", 60, 90, 75)

step = st.sidebar.slider("Step", 1, 10, 1)

# ================= CALC =================
phi = np.radians(phi_deg)
theta0 = np.radians(theta0_deg)

V2_vec = V2 * np.exp(1j * 0)
I2_vec = I2 * np.exp(-1j * phi)

# Secondary drops
IR2 = I2_vec * R
IX2 = I2_vec * 1j * X

E2 = V2_vec + IR2 + IX2

# Refer to primary
E1 = a * E2
I2_prime = I2_vec / a

# No-load current
I0_vec = I0 * np.exp(-1j * theta0)

# Primary current
I1 = I2_prime + I0_vec

# Assume small primary drop → V1 ≈ E1
V1 = E1

# ================= PLOT =================
fig = go.Figure()

def draw(vec, name):
    fig.add_trace(go.Scatter(
        x=[0, vec.real],
        y=[0, vec.imag],
        mode='lines+markers+text',
        text=[None, name],
        textposition="top center",
        line=dict(width=3),
        name=name
    ))

# ---- SECONDARY ----
if step >= 1: draw(V2_vec, "V₂")
if step >= 2: draw(I2_vec, "I₂")
if step >= 3: draw(IR2, "I₂R₂")
if step >= 4: draw(IX2, "I₂X₂")
if step >= 5: draw(E2, "E₂")

# ---- PRIMARY ----
if step >= 6: draw(E1, "E₁")
if step >= 7: draw(I2_prime, "I₂'")
if step >= 8: draw(I0_vec, "I₀")
if step >= 9: draw(I1, "I₁")
if step >= 10: draw(V1, "V₁")

fig.update_layout(
    title="Complete Transformer Phasor Diagram",
    xaxis_title="Real",
    yaxis_title="Imag",
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# ================= STEP GUIDE =================
st.subheader("🧠 Step Explanation")

steps_text = {
1: "Draw V₂ as reference.",
2: "Draw I₂ lagging V₂ by φ.",
3: "Add I₂R₂ in phase with I₂.",
4: "Add I₂X₂ (90° ahead of I₂).",
5: "Result → E₂.",
6: "Refer to primary → E₁ = aE₂.",
7: "Refer current → I₂'.",
8: "Add no-load current I₀.",
9: "Sum → I₁ = I₂' + I₀.",
10:"Approx V₁ ≈ E₁ (neglect drop)."
}

st.info(steps_text[step])

# ================= FORMULAS =================
st.markdown("### 📐 Key Relations")
st.latex(r"E_1 = a E_2")
st.latex(r"I_1 = I_2' + I_0")
