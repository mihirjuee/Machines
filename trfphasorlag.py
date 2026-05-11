import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Transformer Phasor Lab", layout="wide")

st.title("⚡ Transformer Phasor Lab: Step-by-Step")
st.markdown("""
This simulation builds the transformer phasor diagram vector-by-vector. 
In this view, **Primary vectors are shown on the left** and **Secondary vectors on the right** for maximum clarity.
""")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Playback Controls
    if "step_index" not in st.session_state:
        st.session_state.step_index = 1
        
    play_clicked = st.button("▶️ Play Simulation")
    if st.button("Reset"):
        st.session_state.step_index = 1

    st.divider()
    
    # Electrical Parameters
    a = st.slider("Turns Ratio (a)", 0.5, 3.0, 2.0)
    pf_angle = st.slider("Secondary PF Angle (°)", -60, 60, 30)
    i2_mag = st.slider("Load Current (I₂)", 0.2, 1.2, 0.8)
    
    with st.expander("Internal Impedances"):
        r1, x1 = 0.1, 0.25
        r2, x2 = 0.06, 0.12
        ic, im = 0.05, 0.18

# ================= CALCULATIONS =================
theta2 = np.radians(pf_angle)
origin = 0 + 0j

# Secondary Side
V2 = 1.0 + 0j
I2 = i2_mag * (np.cos(theta2) - 1j * np.sin(theta2))
V2_drop_r = I2 * r2
V2_drop_x = I2 * 1j * x2
E2 = V2 + V2_drop_r + V2_drop_x

# Primary Side (180 degree shift)
E1_val = a * E2
minus_E1 = -E1_val 

# Currents
minus_I2_prime = -(I2 / a)
# Excitation aligned with -E1
E1_unit = minus_E1 / np.abs(minus_E1)
Ic_vec = ic * E1_unit
Im_vec = im * (E1_unit * -1j)
Iphi = Ic_vec + Im_vec
I1 = minus_I2_prime + Iphi

# Primary Voltage
V1_drop_r = I1 * r1
V1_drop_x = I1 * 1j * x1
minus_V1 = minus_E1 + V1_drop_r + V1_drop_x

# ================= STEP DEFINITIONS =================
steps = [
    {"label": "1. Reference Voltage", "desc": "Start with Secondary Terminal Voltage $V_2$ at 0°."},
    {"label": "2. Load Current", "desc": "Draw $I_2$ lagging $V_2$ by the Power Factor angle $\\theta_2$."},
    {"label": "3. Secondary Resistance", "desc": "Add the resistive drop $I_2R_2$ in phase with $I_2$."},
    {"label": "4. Secondary Reactance", "desc": "Add the inductive drop $jI_2X_2$ perpendicular to $I_2$."},
    {"label": "5. Secondary EMF", "desc": "The resultant is $E_2$, the voltage induced in the secondary winding."},
    {"label": "6. Primary Induced EMF", "desc": "Reflect $E_2$ to the primary as $-E_1$ (mirrored and scaled by $a$)."},
    {"label": "7. Referred Current", "desc": "Draw $I_2'$ (primary current needed to balance the load MMF)."},
    {"label": "8. No-Load Current", "desc": "Add $I_0$ (Excitation current) to account for core losses and magnetization."},
    {"label": "9. Total Primary Current", "desc": "Vector sum: $I_1 = I_2' + I_0$."},
    {"label": "10. Primary Source", "desc": "Add primary drops to find the total source voltage $V_1$."}
]

# Playback Logic
if play_clicked:
    for i in range(st.session_state.step_index, 11):
        st.session_state.step_index = i
        time.sleep(0.8)
        st.rerun()

# Step Slider
curr_step = st.select_slider("Current Step", options=range(1, 11), value=st.session_state.step_index)
st.session_state.step_index = curr_step

# ================= DRAWING =================
def draw(fig, start, end, label, color, width=3, dash=None):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real], y=[start.imag, end.imag],
        mode="lines", line=dict(color=color, width=width, dash=dash),
        name=label, hoverinfo='skip'
    ))
    fig.add_annotation(
        x=end.real, y=end.imag, ax=start.real, ay=start.imag,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=width, arrowcolor=color
    )

fig = go.Figure()

# Plot based on current step
if curr_step >= 1: draw(fig, origin, V2, "V₂", "green", 5)
if curr_step >= 2: draw(fig, origin, I2, "I₂", "orange", 2)
if curr_step >= 3: draw(fig, V2, V2 + V2_drop_r, "I₂R₂", "#4ade80")
if curr_step >= 4: draw(fig, V2 + V2_drop_r, E2, "jI₂X₂", "#22c55e")
if curr_step >= 5: draw(fig, origin, E2, "E₂", "#15803d", 4)
if curr_step >= 6: draw(fig, origin, minus_E1, "-E₁", "blue", 4)
if curr_step >= 7: draw(fig, origin, minus_I2_prime, "I₂'", "orange", 2, "dash")
if curr_step >= 8: draw(fig, origin, Iphi, "I₀", "gray")
if curr_step >= 9: draw(fig, origin, I1, "I₁", "purple", 4)
if curr_step >= 10:
    draw(fig, minus_E1, minus_E1 + V1_drop_r, "I₁R₁", "#f87171")
    draw(fig, minus_E1 + V1_drop_r, minus_V1, "jI₁X₁", "#dc2626")
    draw(fig, origin, minus_V1, "V₁", "darkblue", 5)

# Axis Styling
limit = max(a + 0.5, 2.5)
fig.update_layout(
    height=750, margin=dict(t=0, b=0),
    xaxis=dict(range=[-limit, limit], zeroline=True, zerolinecolor="black", gridcolor="#eee"),
    yaxis=dict(range=[-limit/1.5, limit/1.5], scaleanchor="x", scaleratio=1, zeroline=True, zerolinecolor="black", gridcolor="#eee"),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)
st.success(f"**{steps[curr_step-1]['label']}**: {steps[curr_step-1]['desc']}")

# ================= THEORY NOTES =================
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔍 Key Insight: Phase Opposition")
    st.write("""
    By Lenz's Law, the primary induced voltage opposes the change in flux. In our diagram, 
    $-E_1$ is drawn $180^\circ$ away from $E_2$ to represent this phase opposition. 
    This creates the 'left-hand' side of the diagram, visually separating the input 
    source from the output load.
    """)

with col2:
    st.markdown("### 📈 Efficiency Info")
    v1_mag = np.abs(minus_V1)
    v2_referred = v1_mag / a
    reg = ((v2_referred - 1.0) / 1.0) * 100
    st.metric("Voltage Regulation", f"{reg:.2f}%")
