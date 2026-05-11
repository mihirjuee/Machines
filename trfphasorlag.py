import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Transformer Phasor Lab", page_icon="logo.png", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.main {
    background-color: #f8fbff;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("⚡ Transformer Phasor Lab")
st.markdown("""
This simulator constructs the **complete transformer phasor diagram** step-by-step exactly.  
""")


# ================= SESSION =================
if "step_index" not in st.session_state:
    st.session_state.step_index = 1

# ================= STEP CONTROLS =================
st.subheader("📍 Step-by-Step Construction Control")

col1, col2, col3 = st.columns([1, 2, 1])

# ---- PREVIOUS BUTTON ----
with col1:
    if st.button("➖ Previous", use_container_width=True):
        if st.session_state.step_index > 1:
            st.session_state.step_index -= 1

# ---- CURRENT STEP DISPLAY ----
with col2:
    st.markdown(
        f"""
        <div style='text-align:center;
                    padding:12px;
                    background-color:#e0f2fe;
                    border-radius:12px;
                    font-size:24px;
                    font-weight:bold;
                    color:#0f172a;'>
            Step {st.session_state.step_index} / 11
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- NEXT BUTTON ----
with col3:
    if st.button("➕ Next", use_container_width=True):
        if st.session_state.step_index < 11:
            st.session_state.step_index += 1

# ================= CURRENT STEP =================
curr_step = st.session_state.step_index

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚙️ Configuration")



    st.divider()

    a = st.slider("Turns Ratio (a = N₁/N₂)", 0.5, 3.0, 2.0)
    pf_angle = st.slider("Secondary PF Angle θ₂ (°)", -60, 60, 30)
    i2_mag = st.slider("Load Current I₂", 0.2, 1.2, 0.8)

    st.subheader("Internal Parameters")

    r1 = st.slider("R₁", 0.0, 0.3, 0.10)
    x1 = st.slider("X₁", 0.0, 0.5, 0.25)

    r2 = st.slider("R₂", 0.0, 0.3, 0.06)
    x2 = st.slider("X₂", 0.0, 0.5, 0.12)

    ic = st.slider("Ic", 0.0, 0.2, 0.05)
    im = st.slider("Im", 0.0, 0.3, 0.18)

# ================= CALCULATIONS =================
theta2 = np.radians(pf_angle)

origin = 0 + 0j

# ---------- SECONDARY SIDE ----------
V2 = 1.0 + 0j
I2 = i2_mag * (np.cos(theta2) - 1j * np.sin(theta2))

I2R2 = I2 * r2
jI2X2 = I2 * 1j * x2

E2 = V2 + I2R2 + jI2X2

# ---------- PRIMARY SIDE ----------
E1 = -a * E2  # Lenz's Law opposition

# ---------- FLUX VECTOR ----------
# EMF leads flux by 90°, so flux lags E1 by 90°
phi_flux = (E1 / np.abs(E1)) * np.exp(-1j * np.pi / 2) * 0.9

# ---------- REFERRED CURRENT ----------
I2_prime = -(I2 / a)

# ---------- EXCITATION CURRENT ----------
E1_unit = E1 / np.abs(E1)

Ic_vec = ic * E1_unit
Im_vec = im * (E1_unit * -1j)

I0 = Ic_vec + Im_vec

# ---------- PRIMARY CURRENT ----------
I1 = I2_prime + I0

# ---------- PRIMARY VOLTAGE ----------
I1R1 = I1 * r1
jI1X1 = I1 * 1j * x1

V1 = E1 + I1R1 + jI1X1

# ================= STEPS =================
steps = [
    "Draw secondary terminal voltage V₂ as reference.",
    "Draw secondary current I₂ at angle θ₂.",
    "Add I₂R₂ in phase with I₂.",
    "Add jI₂X₂ perpendicular to I₂.",
    "Resultant gives secondary induced EMF E₂.",
    "Reflect E₂ to primary as −E₁.",
    "Add magnetic flux vector Φ (lags E₁ by 90°).",
    "Draw referred current I₂′ on primary side.",
    "Add no-load current I₀ = Ic + Im.",
    "Vector sum gives primary current I₁.",
    "Add I₁R₁ and jI₁X₁ to obtain source voltage V₁."
]



# ================= DRAW FUNCTION =================
def draw_vector(fig, start, end, label, color, width=4, dash=None, shiftx=0, shifty=0):
    fig.add_trace(go.Scatter(
        x=[start.real, end.real],
        y=[start.imag, end.imag],
        mode="lines",
        line=dict(color=color, width=width, dash=dash),
        hoverinfo="skip"
    ))

    fig.add_annotation(
        x=end.real,
        y=end.imag,
        ax=start.real,
        ay=start.imag,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.3,
        arrowwidth=2.2,
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

# ---------- SECONDARY SIDE ----------
if curr_step >= 1:
    draw_vector(fig, origin, V2, "V₂", "blue", width=5, shifty=-0.12)

if curr_step >= 2:
    draw_vector(fig, origin, I2, "I₂", "green", width=3)

if curr_step >= 3:
    draw_vector(fig, V2, V2 + I2R2, "I₂R₂", "#84cc16", width=3)

if curr_step >= 4:
    draw_vector(fig, V2 + I2R2, E2, "jI₂X₂", "#16a34a", width=3)

if curr_step >= 5:
    draw_vector(fig, origin, E2, "E₂", "#22c55e", width=5, shifty=0.15)

# ---------- PRIMARY SIDE ----------
if curr_step >= 6:
    draw_vector(fig, origin, E1, "−E₁", "purple", width=5, shifty=0.15)

# ---------- FLUX ----------
if curr_step >= 7:
    draw_vector(
        fig,
        origin,
        phi_flux,
        "Φ",
        "#06b6d4",
        width=4,
        dash="dot",
        shifty=0.15
    )

# ---------- REFERRED CURRENT ----------
if curr_step >= 8:
    draw_vector(fig, origin, I2_prime, "I₂′", "orange", width=3, dash="dash")

# ---------- NO LOAD CURRENT ----------
if curr_step >= 9:
    draw_vector(fig, origin, Ic_vec, "Ic", "#f59e0b", width=3)
    draw_vector(fig, origin, Im_vec, "Im", "#eab308", width=3)
    draw_vector(fig, origin, I0, "I₀", "gray", width=4)

# ---------- PRIMARY CURRENT ----------
if curr_step >= 10:
    draw_vector(fig, origin, I1, "I₁", "red", width=4)

# ---------- PRIMARY VOLTAGE ----------
if curr_step >= 11:
    draw_vector(fig, E1, E1 + I1R1, "I₁R₁", "#f97316", width=3)
    draw_vector(fig, E1 + I1R1, V1, "jI₁X₁", "#dc2626", width=3)
    draw_vector(fig, origin, V1, "V₁", "darkblue", width=5, shifty=0.15)

# ================= ANGLE ARC =================
theta_arc = np.linspace(-theta2, 0, 40)

fig.add_trace(go.Scatter(
    x=0.5 * np.cos(theta_arc),
    y=0.5 * np.sin(theta_arc),
    mode="lines",
    line=dict(color="gray", dash="dot")
))

fig.add_annotation(
    x=0.4,
    y=-0.12,
    text="θ₂",
    showarrow=False
)

# ================= SIDE LABELS =================
fig.add_annotation(
    x=-2.4,
    y=1.9,
    text="<b>PRIMARY SIDE</b>",
    showarrow=False,
    font=dict(size=18)
)

fig.add_annotation(
    x=2.4,
    y=1.9,
    text="<b>SECONDARY SIDE</b>",
    showarrow=False,
    font=dict(size=18)
)

# ================= STYLE =================
limit = max(
    abs(V1.real),
    abs(E1.real),
    abs(E2.real),
    2.5
) + 1.4

fig.update_layout(
    height=820,
    xaxis=dict(
        range=[-limit, limit],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        showgrid=True,
        gridcolor="#e5e7eb"
    ),
    yaxis=dict(
        range=[-limit / 1.7, limit / 1.7],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        showgrid=True,
        gridcolor="#e5e7eb",
        scaleanchor="x"
    ),
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# ================= DISPLAY =================
st.plotly_chart(fig, use_container_width=True)

# ================= STEP INFO =================
st.success(f"### Step {curr_step}: {steps[curr_step - 1]}")

# ================= THEORY =================
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📘 Key Equations")
    st.latex(r"E_2 = V_2 + I_2R_2 + jI_2X_2")
    st.latex(r"E_1 = -aE_2")
    st.latex(r"E \propto \frac{d\Phi}{dt}")
    st.latex(r"I_1 = I_2' + I_0")
    st.latex(r"V_1 = -E_1 + I_1R_1 + jI_1X_1")

with col2:
    st.markdown("### 📊 Performance")
    regulation = ((np.abs(V1) / a - np.abs(V2)) / np.abs(V2)) * 100

    st.metric("Voltage Regulation", f"{regulation:.2f}%")
    st.metric("Primary PF Angle θ₁", f"{np.degrees(np.angle(V1-I1)):.2f}°")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🎓 Transformer Phasor Lab")
st.markdown("Flux • EMF • Current • Voltage • Textbook Construction ⚡")
