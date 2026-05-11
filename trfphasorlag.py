import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Transformer Phasor Diagram", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stSlider {
        padding-top: 10px;
    }
    </style>
    """, unsafe_content_with_dropdown=True)

st.title("⚡ Interactive Transformer Phasor Diagram")
st.markdown("""
This application visualizes the phasor relationships in a non-ideal transformer. 
Adjust the parameters in the sidebar to see how load, power factor, and internal impedances affect the voltage and current vectors.
""")

# ================= SIDEBAR PARAMETERS =================
with st.sidebar:
    st.header("🔧 Transformer Parameters")
    
    with st.expander("Secondary Load", expanded=True):
        V2_mag = st.slider("V₂ Magnitude (p.u.)", 0.5, 1.5, 1.0, 0.05)
        I2_mag = st.slider("I₂ Magnitude (p.u.)", 0.1, 1.5, 0.8, 0.05)
        theta2_deg = st.slider("Secondary PF Angle θ₂ (°)", -60, 70, 30, 5)
        st.caption("Positive = Lagging (Inductive), Negative = Leading (Capacitive)")

    with st.expander("Impedances & Ratio"):
        a = st.slider("Turns Ratio (a = N₁/N₂)", 0.5, 5.0, 2.0, 0.1)
        R1 = st.slider("Primary Resistance R₁", 0.0, 0.2, 0.05)
        X1 = st.slider("Primary Reactance X₁", 0.0, 0.4, 0.15)
        R2 = st.slider("Secondary Resistance R₂", 0.0, 0.2, 0.05)
        X2 = st.slider("Secondary Reactance X₂", 0.0, 0.4, 0.15)

    with st.expander("Core (No-Load) Components"):
        Ic = st.slider("Core Loss Current Ic", 0.0, 0.2, 0.05)
        Im = st.slider("Magnetizing Current Im", 0.0, 0.3, 0.12)

# ================= CALCULATIONS =================
theta2 = np.radians(theta2_deg)
origin = 0 + 0j

# 1. Secondary side (V2 is the reference at 0 degrees)
V2 = V2_mag + 0j
# I2 lags V2 by theta2
I2 = I2_mag * (np.cos(theta2) - 1j * np.sin(theta2))

# 2. Secondary induced EMF (E2)
# E2 = V2 + I2*Z2
Z2 = R2 + 1j * X2
E2 = V2 + I2 * Z2

# 3. Primary induced EMF (E1)
E1 = a * E2

# 4. Excitation current (Iphi)
# In textbooks, Ic is in phase with E1, Im lags E1 by 90 degrees
if np.abs(E1) > 0:
    E1_unit = E1 / np.abs(E1)
    Ic_vec = Ic * E1_unit
    Im_vec = Im * (E1_unit * -1j)
else:
    Ic_vec = 0j
    Im_vec = 0j
Iphi = Ic_vec + Im_vec

# 5. Primary total current (I1)
I2_prime = I2 / a  # Referred secondary current
I1 = I2_prime + Iphi

# 6. Primary terminal voltage (V1)
Z1 = R1 + 1j * X1
V1 = E1 + I1 * Z1

# ================= DRAWING UTILITY =================
def draw_phasor(fig, start, end, label, color, width=3, is_dashed=False):
    line_style = dict(color=color, width=width)
    if is_dashed:
        line_style['dash'] = 'dash'
        
    fig.add_trace(go.Scatter(
        x=[start.real, end.real],
        y=[start.imag, end.imag],
        mode="lines",
        line=line_style,
        hoverinfo='text',
        text=f"{label}: {np.abs(end-start):.2f} ∠{np.degrees(np.angle(end-start)):.1f}°",
        name=label
    ))

    # Arrow head logic
    fig.add_annotation(
        x=end.real, y=end.imag,
        ax=start.real, ay=start.imag,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=width, arrowcolor=color
    )
    
    # Label offset
    angle = np.angle(end - start)
    dist = 0.1
    fig.add_annotation(
        x=end.real + dist * np.cos(angle),
        y=end.imag + dist * np.sin(angle),
        text=label, showarrow=False, font=dict(color=color, size=14)
    )

# ================= VISUALIZATION =================
fig = go.Figure()

# Primary Side Phasors
draw_phasor(fig, origin, V1, "V₁", "#1e40af", width=5)
draw_phasor(fig, origin, E1, "E₁", "#3b82f6")
draw_phasor(fig, E1, E1 + I1*R1, "I₁R₁", "#ef4444", width=2)
draw_phasor(fig, E1 + I1*R1, V1, "jI₁X₁", "#b91c1c", width=2)

# Secondary Side Phasors
draw_phasor(fig, origin, V2, "V₂", "#065f46", width=5)
draw_phasor(fig, origin, E2, "E₂", "#10b981")
draw_phasor(fig, V2, V2 + I2*R2, "I₂R₂", "#84cc16", width=2)
draw_phasor(fig, V2 + I2*R2, E2, "jI₂X₂", "#4d7c0f", width=2)

# Current Phasors
draw_phasor(fig, origin, I1, "I₁", "#7c3aed")
draw_phasor(fig, origin, I2, "I₂", "#f59e0b")
draw_phasor(fig, origin, I2_prime, "I₂'", "#fbbf24", is_dashed=True)
draw_phasor(fig, origin, Iphi, "I₀", "#94a3b8")

# Layout Adjustments
limit = max(np.abs(V1), np.abs(E1), np.abs(V2)) + 0.5
fig.update_layout(
    height=800,
    showlegend=True,
    plot_bgcolor="white",
    xaxis=dict(range=[-limit/2, limit], zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#eee'),
    yaxis=dict(range=[-limit, limit], zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#eee', scaleanchor="x", scaleratio=1),
    margin=dict(l=20, r=20, t=20, b=20)
)

# Display Plot
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Numerical Values")
    st.metric("V₁ (Primary)", f"{np.abs(V1):.3f} ∠{np.degrees(np.angle(V1)):.1f}°")
    st.metric("V₂ (Secondary)", f"{np.abs(V2):.3f} ∠0°")
    st.metric("I₁ (Primary)", f"{np.abs(I1):.3f} ∠{np.degrees(np.angle(I1)):.1f}°")
    st.metric("I₂ (Secondary)", f"{np.abs(I2):.3f} ∠{theta2_deg:.1f}°")
    
    eff_v_reg = ((np.abs(V1)/a - np.abs(V2)) / np.abs(V2)) * 100
    st.metric("Voltage Regulation", f"{eff_v_reg:.2f}%")

# ================= THEORY SECTION =================
st.divider()
st.header("📖 Transformer Theory & Equations")

t1, t2 = st.columns(2)

with t1:
    st.markdown("### Governing Equations")
    st.latex(r"V_1 = E_1 + I_1(R_1 + jX_1)")
    st.latex(r"E_2 = V_2 + I_2(R_2 + jX_2)")
    st.latex(r"E_1 = a \cdot E_2")
    st.latex(r"I_1 = \frac{I_2}{a} + I_0")
    st.latex(r"I_0 = I_c + I_m")

with t2:
    st.markdown("### Key Observations")
    st.info("""
    - **Lagging Load:** As $\\theta_2$ increases (inductive), $V_2$ drops significantly below the referred $V_1$.
    - **Leading Load:** Notice how $V_2$ can actually become higher than $V_1/a$ at certain capacitive angles (Ferranti-like effect).
    - **No-Load Current:** $I_0$ is small but essential for maintaining the flux ($\Phi$) and covering core losses.
    """)

st.markdown("---")
st.caption("Developed for Electrical Engineering Education | Built with Streamlit & Plotly")
