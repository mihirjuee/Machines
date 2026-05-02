# ======================================================================
# WHY SINGLE-PHASE INDUCTION MOTOR IS NOT SELF-STARTING
# Streamlit Interactive Visualizer
# Features:
# ✅ Pulsating magnetic field animation
# ✅ Double revolving field theory
# ✅ Forward & backward torque
# ✅ Net torque visualization
# ✅ Push-start mode
# ✅ Capacitor start mode
# ======================================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Single-Phase Motor Self-Starting",
    page_icon="⚡",
    layout="wide"
)

# Background
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Why Single-Phase Induction Motor is NOT Self-Starting")

# ----------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------
st.sidebar.header("🔧 Motor Controls")

Vm = st.sidebar.slider("Supply Voltage Magnitude", 0.5, 1.5, 1.0)
freq = st.sidebar.slider("Supply Frequency (Hz)", 10, 60, 50)
time_angle = st.sidebar.slider("Electrical Angle (°)", 0, 360, 0)

push_start = st.sidebar.toggle("🌀 External Push Start", value=False)
capacitor_mode = st.sidebar.toggle("⚡ Capacitor Start Mode", value=False)

rotor_speed = st.sidebar.slider("Rotor Speed (for push mode)", 0.0, 1.0, 0.2)

# ----------------------------------------------------------------------
# CORE THEORY
# ----------------------------------------------------------------------
theta = np.linspace(0, 2 * np.pi, 400)
wt = np.radians(time_angle)

# Pulsating field
B_main = Vm * np.cos(theta) * np.cos(wt)

# Double revolving field
B_forward = 0.5 * Vm * np.cos(theta - wt)
B_backward = 0.5 * Vm * np.cos(theta + wt)

# ----------------------------------------------------------------------
# TORQUE MODEL
# ----------------------------------------------------------------------
# Simplified educational model
if capacitor_mode:
    T_forward = 1.0
    T_backward = 0.2
elif push_start:
    T_forward = 1.0 - rotor_speed * 0.3
    T_backward = 0.5 * (1 - rotor_speed)
else:
    T_forward = 0.5
    T_backward = 0.5

T_net = T_forward - T_backward

# ----------------------------------------------------------------------
# LAYOUT
# ----------------------------------------------------------------------
col1, col2 = st.columns([1.2, 1])

# ======================================================================
# LEFT: FIELD VISUALIZATION
# ======================================================================
with col1:
    st.subheader("🧲 Magnetic Field Visualization")

    fig, ax = plt.subplots(figsize=(8, 8))

    # Motor boundary
    circle = Circle((0, 0), 1.1, fill=False, linewidth=2)
    ax.add_patch(circle)

    # Pulsating field
    x = np.cos(theta)
    y = B_main
    ax.plot(x, y, label="Pulsating Field")

    # Forward rotating field
    ax.arrow(
        0, 0,
        0.8 * np.cos(wt),
        0.8 * np.sin(wt),
        head_width=0.08,
        length_includes_head=True,
        label="Forward"
    )

    # Backward rotating field
    ax.arrow(
        0, 0,
        0.8 * np.cos(-wt),
        0.8 * np.sin(-wt),
        head_width=0.08,
        length_includes_head=True
    )

    # Capacitor creates phase-shifted auxiliary field
    if capacitor_mode:
        ax.arrow(
            0, 0,
            0.7 * np.cos(wt + np.pi / 2),
            0.7 * np.sin(wt + np.pi / 2),
            head_width=0.08,
            linestyle='--',
            length_includes_head=True
        )

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.set_title("Forward + Backward Fields")
    ax.grid(True)

    st.pyplot(fig)

# ======================================================================
# RIGHT: TORQUE VISUALIZATION
# ======================================================================
with col2:
    st.subheader("📈 Torque Analysis")

    slip = np.linspace(0, 1, 300)

    # Educational torque curves
    Tf_curve = T_forward * slip / (0.2 + slip**2)
    Tb_curve = T_backward * slip / (0.2 + slip**2)
    Tnet_curve = Tf_curve - Tb_curve

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    ax2.plot(slip, Tf_curve, label="Forward Torque")
    ax2.plot(slip, Tb_curve, label="Backward Torque")
    ax2.plot(slip, Tnet_curve, linewidth=3, label="Net Torque")

    ax2.axhline(0, linestyle="--")

    ax2.set_xlabel("Slip")
    ax2.set_ylabel("Torque")
    ax2.set_title("Torque-Slip Characteristics")
    ax2.grid(True)
    ax2.legend()

    st.pyplot(fig2)

# ======================================================================
# STATUS PANEL
# ======================================================================
st.divider()
st.subheader("⚙️ Motor Starting Status")

if capacitor_mode:
    st.success("✅ Capacitor Start creates phase split → Rotating field produced → Motor self-starts")
elif push_start:
    st.success("🌀 External push gives direction → Forward torque dominates → Motor accelerates")
else:
    st.error("❌ At standstill: Forward torque = Backward torque → Net starting torque = 0")

# ======================================================================
# METRICS
# ======================================================================
m1, m2, m3 = st.columns(3)

m1.metric("Forward Torque", f"{T_forward:.2f}")
m2.metric("Backward Torque", f"{T_backward:.2f}")
m3.metric("Net Starting Torque", f"{T_net:.2f}")

# ======================================================================
# THEORY
# ======================================================================
st.divider()
st.subheader("📘 Double Revolving Field Theory")

st.markdown("""
### Single-phase supply creates:
## Pulsating Magnetic Field

This pulsating field can be resolved into:

### Forward Rotating Field
\[
\phi_f = \frac{\phi_m}{2}
\]

### Backward Rotating Field
\[
\phi_b = \frac{\phi_m}{2}
\]

### At Standstill:
\[
T_f = T_b
\]

## Therefore:
### Net Torque = 0

That is why a single-phase induction motor is NOT self-starting.

---
### To Start:
### ✅ Capacitor Start  
### ✅ Split Phase  
### ✅ Shaded Pole  
### ✅ External Push
""")

# ======================================================================
# REAL LIFE
# ======================================================================
with st.expander("💡 Real-Life Example"):
    st.write("""
### Ceiling fan humming but not rotating?
Likely causes:
- Weak capacitor
- Auxiliary winding issue
- Mechanical friction

### Why pushing works:
Push creates initial rotation → Forward slip decreases → Forward torque > Backward torque
""")

# ======================================================================
# FOOTER
# ======================================================================
st.caption("Developed for Electrical Engineering Visualization ⚡")
