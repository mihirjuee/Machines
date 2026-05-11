import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Transformer Simulation Lab", layout="wide")

# Initialize Session State for Steps
if "step_index" not in st.session_state:
    st.session_state.step_index = 1

st.title("⚡ Transformer Phasor Lab")
st.markdown("Build the diagram vector-by-vector to understand how internal impedances affect the relationship between $V_1$ and $V_2$.")

# ================= SIDEBAR: PARAMETERS =================
with st.sidebar:
    st.header("🎮 Controls")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Play"):
            play_active = True
        else:
            play_active = False
    with col2:
        if st.button("⏭️ Next"):
            if st.session_state.step_index < 10:
                st.session_state.step_index += 1
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.step_index = 1

    st.divider()
    
    st.header("🏗️ Transformer Design")
    a = st.slider("Turns Ratio (a = N1/N2)", 0.5, 4.0, 2.0)
    
    with st.expander("Secondary Side (Load)", expanded=True):
        i2_mag = st.slider("Load Current (I₂)", 0.1, 1.5, 0.8)
        pf_angle = st.slider("PF Angle (°)", -90, 90, 30)
        r2 = st.slider("Resistance R₂", 0.0, 0.3, 0.05)
        x2 = st.slider("Reactance X₂", 0.0, 0.5, 0.15)

    with st.expander("Primary Side & Core"):
        r1 = st.slider("Resistance R₁", 0.0, 0.3, 0.05)
        x1 = st.slider("Reactance X₁", 0.0, 0.5, 0.15)
        ic = st.slider("Core Loss (Ic)", 0.0, 0.2, 0.04)
        im = st.slider("Magnetizing (Im)", 0.0, 0.4, 0.15)

# ================= CALCULATIONS =================
theta2 = np.radians(pf_angle)
origin = 0 + 0j

# Secondary Vectors
V2 = 1.0 + 0j
I2 = i2_mag * (np.cos(theta2) - 1j * np.sin(theta2))
V2_drop_r = I2 * r2
V2_drop_x = I2 * 1j * x2
E2 = V2 + V2_drop_r + V2_drop_x

# Primary Vectors (Phasor-flipped 180 degrees)
minus_E1 = -(a * E2)
minus_I2_prime = -(I2 / a)

# Core components relative to -E1
if np.abs(minus_E1) > 0:
    E1_unit = minus_E1 / np.abs(minus_E1)
    Ic_vec = ic * E1_unit
    Im_vec = im * (E1_unit * -1j)
else:
    Ic_vec, Im_vec = 0j, 0j

I0 = Ic_vec + Im_vec
I1 = minus_I2_prime + I0

# Primary Terminal Voltage
V1_drop_r = I1 * r1
V1_drop_x = I1 * 1j * x1
minus_V1 = minus_E1 + V1_drop_r + V1_drop_x

# ================= PLAYBACK LOGIC =================
if play_active:
    for i in range(st.session_state.step_index, 11):
        st.session_state.step_index = i
        time.sleep(0.5)
        st.rerun()

curr_step = st.session_state.step_index

# ================= VISUALIZATION =================
def add_vector(fig, start, end, label, color, width=3, dash=None):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode="lines", line=dict(color=color, width=width, dash=dash),
        name=label, hovertext=f"{label}: {np.abs(end-start):.2f}"
    ))
    fig.add_annotation(
        x=end.real, y=end.imag, ax=start.real, ay=start.imag,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=width, arrowcolor=color
    )

fig = go.Figure()

# Logical progression of the Diagram
if curr_step >= 1: add_vector(fig, origin, V2, "V₂", "#10b981", 5)
if curr_step >= 2: add_vector(fig, origin, I2, "I₂", "#f59e0b", 2)
if curr_step >= 3: add_vector(fig, V2, V2 + V2_drop_r, "I₂R₂", "#86efac")
if curr_step >= 4: add_vector(fig, V2 + V2_drop_r, E2, "jI₂X₂", "#22c55e")
if curr_step >= 5: add_vector(fig, origin, E2, "E₂", "#15803d", 4)
if curr_step >= 6: add_vector(fig, origin, minus_E1, "-E₁", "#3b82f6", 4)
if curr_step >= 7: add_vector(fig, origin, minus_I2_prime, "I₂'", "#fbbf24", 2, "dash")
if curr_step >= 8: add_vector(fig, origin, I0, "I₀", "#94a3b8")
if curr_step >= 9: add_vector(fig, origin, I1, "I₁", "#7c3aed", 4)
if curr_step >= 10:
    add_vector(fig, minus_E1, minus_E1 + V1_drop_r, "I₁R₁", "#f87171")
    add_vector(fig, minus_E1 + V1_drop_r, minus_V1, "jI₁X₁", "#dc2626")
    add_vector(fig, origin, minus_V1, "V₁", "#1e3a8a", 5)

# Axis Scaling
limit = max(np.abs(minus_V1), np.abs(V2), a) + 0.5
fig.update_layout(
    height=700,
    xaxis=dict(range=[-limit, limit], zeroline=True, zerolinecolor="black"),
    yaxis=dict(range=[-limit/1.5, limit/1.5], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="black"),
    margin=dict(t=0, b=0), plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# ================= STATUS MESSAGES =================
step_descriptions = [
    "**Step 1:** Establish $V_2$ as our reference on the real axis.",
    "**Step 2:** Plot $I_2$ lagging $V_2$ by the load phase angle.",
    "**Step 3:** Add the secondary resistance drop $I_2R_2$ (parallel to $I_2$).",
    "**Step 4:** Add the secondary reactance drop $jI_2X_2$ (90° ahead of $I_2$).",
    "**Step 5:** Complete the secondary triangle to find the induced EMF $E_2$.",
    "**Step 6:** Reflect the EMF to the primary side as $-E_1$ (Scaled by $a$).",
    "**Step 7:** Draw the referred load current $I_2'$ on the primary side.",
    "**Step 8:** Introduce the no-load excitation current $I_0$ (Magnetizing + Core loss).",
    "**Step 9:** Combine $I_2'$ and $I_0$ to find the total primary current $I_1$.",
    "**Step 10:** Add primary impedance drops to $-E_1$ to find the source voltage $V_1$."
]

st.info(step_descriptions[curr_step-1])

# Progress Bar
st.progress(curr_step / 10)
