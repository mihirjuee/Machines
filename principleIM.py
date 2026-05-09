# three_phase_induction_motor_physical_rotation.py
# Streamlit App: Physical Rotor Rotation in 3-Phase Induction Motor
# Run:
# streamlit run three_phase_induction_motor_physical_rotation.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="3-Phase Induction Motor Rotor Rotation",
    page_icon="⚡",
    layout="wide"
)

# ================= TITLE =================
st.title("⚡ Physical Rotation of Rotor in Three Phase Induction Motor")
st.markdown("### Visualizing Rotating Magnetic Field (Stator) and Rotor Motion")

# ================= SIDEBAR =================
st.sidebar.header("Motor Controls")

frequency = st.sidebar.slider("Supply Frequency (Hz)", 25, 100, 50)
poles = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)
slip = st.sidebar.slider("Slip (%)", 1, 15, 4)

Ns = 120 * frequency / poles
Nr = Ns * (1 - slip / 100)

# Angular velocities
ws = 2 * np.pi * frequency / (poles / 2)     # stator field speed
wr = ws * (1 - slip / 100)                   # rotor speed

# ================= METRICS =================
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Synchronous Speed", f"{Ns:.0f} RPM")

with c2:
    st.metric("Rotor Speed", f"{Nr:.0f} RPM")

with c3:
    st.metric("Slip", f"{slip}%")

# ================= THEORY =================
st.subheader("📘 Principle")
st.markdown("""
The stator produces a rotating magnetic field at synchronous speed.  
The rotor attempts to follow this field but always rotates slightly slower due to slip.

### Key:
- **Blue Arrow:** Stator Rotating Magnetic Field  
- **Red Rotor Bars:** Physical Rotor Rotation  
""")

st.latex(r"N_s = \frac{120f}{P}")
st.latex(r"N_r = N_s(1-s)")

# ================= ANIMATION =================
run = st.checkbox("▶ Run Physical Rotation Animation", value=True)

placeholder = st.empty()

frames = np.linspace(0, 8*np.pi, 180)

# ================= DRAW FUNCTION =================
def create_motor_frame(theta_s, theta_r):
    fig = go.Figure()

    # Stator outer circle
    stator_theta = np.linspace(0, 2*np.pi, 300)
    stator_x = 1.8 * np.cos(stator_theta)
    stator_y = 1.8 * np.sin(stator_theta)

    fig.add_trace(go.Scatter(
        x=stator_x,
        y=stator_y,
        mode='lines',
        name='Stator'
    ))

    # Rotor circle
    rotor_x = 0.9 * np.cos(stator_theta)
    rotor_y = 0.9 * np.sin(stator_theta)

    fig.add_trace(go.Scatter(
        x=rotor_x,
        y=rotor_y,
        mode='lines',
        name='Rotor'
    ))

    # Rotor bars (physical rotation)
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        x1 = 0.2 * np.cos(angle + theta_r)
        y1 = 0.2 * np.sin(angle + theta_r)

        x2 = 0.9 * np.cos(angle + theta_r)
        y2 = 0.9 * np.sin(angle + theta_r)

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode='lines',
            showlegend=False
        ))

    # Shaft
    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode='markers',
        marker=dict(size=12),
        name='Shaft'
    ))

    # Stator RMF Arrow
    rmf_x = 1.5 * np.cos(theta_s)
    rmf_y = 1.5 * np.sin(theta_s)

    fig.add_trace(go.Scatter(
        x=[0, rmf_x],
        y=[0, rmf_y],
        mode='lines+markers',
        name='Rotating Magnetic Field'
    ))

    # Rotor direction arrow
    rotor_arrow_x = 1.1 * np.cos(theta_r)
    rotor_arrow_y = 1.1 * np.sin(theta_r)

    fig.add_trace(go.Scatter(
        x=[0, rotor_arrow_x],
        y=[0, rotor_arrow_y],
        mode='lines+markers',
        name='Rotor Rotation'
    ))

    # Layout
    fig.update_layout(
        title="Physical Rotor Rotation vs Stator RMF",
        xaxis=dict(range=[-2.2, 2.2], zeroline=False, visible=False),
        yaxis=dict(range=[-2.2, 2.2], zeroline=False, visible=False, scaleanchor="x"),
        height=750,
        showlegend=True
    )

    return fig

# ================= RUN ANIMATION =================
if run:
    for t in frames:
        theta_s = ws * t * 0.02
        theta_r = wr * t * 0.02

        fig = create_motor_frame(theta_s, theta_r)
        placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(0.05)

else:
    fig = create_motor_frame(0, 0)
    placeholder.plotly_chart(fig, use_container_width=True)

# ================= EXPLANATION =================
st.subheader("⚙ Observation")
st.markdown("""
### Notice:
- The **stator magnetic field rotates faster**
- The **rotor physically follows**
- Rotor speed is slightly less than RMF due to slip
- This speed difference is essential for torque production

### If Rotor = RMF:
No relative motion → No induced EMF → No torque
""")

# ================= DIRECTION =================
st.subheader("🔁 Direction Control")
st.info("""
Changing any two supply phases reverses direction:

**RYB → Clockwise**  
**RBY → Counterclockwise**
""")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### Advanced Electrical Machine Visualization ⚡")
