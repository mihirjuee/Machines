import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(page_title="IM Equivalent Circuit Lab", page_icon="logo.png", layout="wide")

# =========================
# 🎨 STYLE
# =========================
st.markdown("""
<style>

/* =========================
   🌌 MAIN BACKGROUND
========================= */
.stApp {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c7744);
}

/* =========================
   📄 MAIN TEXT AREA
========================= */
.main {
    color: #ffffff !important;
}

/* Improve readability globally */
.main * {
    color: #ffffff !important;
}

/* =========================
   📊 METRIC CARDS (GLASS EFFECT)
========================= */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.12);
    padding: 18px;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Metric value styling */
div[data-testid="stMetric"] label {
    color: #a8f0e5 !important;
}

/* =========================
   📚 SIDEBAR (LIGHT PANEL)
========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f7f9fb, #e6edf3) !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #1a1a1a !important;
    font-weight: 500;
}

/* =========================
   🧠 HEADINGS
========================= */
h1, h2, h3 {
    color: #00ffd5 !important;
    text-shadow: 0px 0px 10px rgba(0,255,213,0.3);
}

/* =========================
   📈 BUTTONS (if used)
========================= */
.stButton > button {
    background: linear-gradient(90deg, #00c9ff, #92fe9d);
    color: black !important;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("⚡ 3-Phase Induction Motor Performance Evaluation using Equivalent Circuit Parameters")
st.subheader("Torque-Speed Curve with Operating Point")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Motor Parameters(Set realistic value)")

V_line = st.sidebar.slider("Line Voltage (V)", 200, 500, 400)
f = st.sidebar.slider("Frequency (Hz)", 40, 60, 50)

R1 = st.sidebar.slider("R1 (Ω)", 0.1, 10.0, 0.5)
X1 = st.sidebar.slider("X1 (Ω)", 0.1, 10.0, 1.0)

R2 = st.sidebar.slider("R2 (Ω)", 0.1,10.0, 0.4)
X2 = st.sidebar.slider("X2 (Ω)", 0.1, 10.0, 0.8)

Xm = st.sidebar.slider("Xm (Ω)", 5.0, 200.0, 30.0)
Rc = st.sidebar.slider("Rc (Ω)", 10.0, 2000.0, 150.0)

slip = st.sidebar.slider("Operating Slip (s)", 0.01, 1.0, 0.05)
P = st.sidebar.slider("No. of poles (P)", 2, 8, 4, step=2)

# =========================
# CALCULATIONS
# =========================
V_phase = V_line / np.sqrt(3)

Z1 = complex(R1, X1)

Ns = 120 * f / P
ws = 2 * np.pi * Ns / 60

# Magnetizing + core loss branch
Zm = 1 / (1/Rc + 1/complex(0, Xm))

# =========================
# OPERATING POINT CALCULATION
# =========================
Z2_op = complex(R2/slip, X2)
Zp_op = (Z2_op * Zm) / (Z2_op + Zm)
Zt_op = Z1 + Zp_op

I1_op = V_phase / Zt_op   # stator current

# voltage across parallel branch
V_parallel = V_phase - I1_op * Z1

# rotor current (IMPORTANT FIX)
I2_op = V_parallel / Z2_op

# correct air-gap power
P_ag_op = 3 * (abs(I2_op)**2) * (R2/slip)

# torque
T_op = P_ag_op / ws
I_op = V_phase / Zt_op

operating_speed = (1 - slip) * Ns

# =========================
# TORQUE-SPEED CURVE
# =========================
s_vals = np.linspace(1.0, 0.01, 60)
torque_vals = []

for s in s_vals:

    # Rotor branch impedance (depends on slip)
    Z2 = complex(R2/s, X2)

    # Magnetizing branch
    Zm = 1 / (1/Rc + 1/complex(0, Xm))

    # Parallel combination
    Zp = (Z2 * Zm) / (Z2 + Zm)

    # Total impedance
    Zt = Z1 + Zp

    # Stator current
    I1 = V_phase / Zt

    # Voltage across parallel branch
    V_parallel = V_phase - I1 * Z1

    # Rotor current
    I2 = V_parallel / Z2

    # Air-gap power (CORRECT)
    P_ag = 3 * (abs(I2)**2) * (R2/s)

    # Torque
    T = P_ag / ws

    torque_vals.append(T)

# Speed
speed = (1 - s_vals) * Ns

# =========================
# METRICS
# =========================
st.subheader("📊 Performance at Operating Point")

c1, c2, c3 = st.columns(3)

c1.metric("Operating Speed", f"{operating_speed:.1f} RPM")
c2.metric("Operating Torque", f"{T_op:.2f} Nm")
c3.metric("Rotor Current (A)", f"{abs(I_op):.2f}")

# =========================
# POWER FLOW
# =========================
st.subheader("⚡ Power Flow")

P_input = 3 * V_phase * abs(I_op) * np.cos(np.angle(I_op))
P_core = 3 * (abs(V_parallel)**2) / Rc
P_mech = P_ag_op * (1 - slip)

st.info(f"""
Input Power = {P_input:.2f} W  
Core Loss = {P_core:.2f} W  
Air-gap Power = {P_ag_op:.2f} W  
Mechanical Power = {P_mech:.2f} W  
""")

# =========================
# PLOT WITH OPERATING POINT
# =========================
st.subheader("📈 Torque-Speed Characteristic")

fig, ax = plt.subplots()

ax.plot(speed, torque_vals, linewidth=2, label="Torque-Speed Curve")

# 🔴 Operating point
ax.scatter(operating_speed, T_op, color="red", s=120, label="Operating Point")

ax.annotate(
    f"OP\n{operating_speed:.0f} RPM\n{T_op:.1f} Nm",
    (operating_speed, T_op),
    textcoords="offset points",
    xytext=(10,10),
    color="red"
)

# Starting torque
ax.scatter(speed[0], torque_vals[0], color="green", label="Starting Torque")

# Max torque
idx = np.argmax(torque_vals)
ax.scatter(speed[idx], torque_vals[idx], color="orange", label="Max Torque")

if operating_speed < speed[idx]:
    st.error(f"⚠️ Warning: Slip ({slip:.2f}) is beyond breakdown slip")

elif abs(operating_speed - speed[idx]) < 0.05:
    st.warning("⚡ Operating near maximum (breakdown) torque region")

else:
    st.success("✅ Stable operating region")
    
ax.set_xlabel("Speed (RPM)")
ax.set_ylabel("Torque (Nm)")
ax.set_title("Torque-Speed Curve with Operating Point")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# =========================
# CIRCUIT DIAGRAM
# =========================
import io

st.subheader("🔌 Equivalent Circuit")

d = schemdraw.Drawing()

d += elm.SourceV().label("Vph")
d += elm.Resistor().right().label("R1")
d += elm.Inductor().right().label("jX1")

d += elm.Dot()
d.push()

# Rc branch
d += elm.Line().down(0.1)
d += elm.Resistor().label("Rc")

d.pop()
d.push()
# Xm branch
d += elm.Line().right(1.5)
d += elm.Dot()
d += elm.Line().down(0.1)
d += elm.Inductor().label("jXm")

d.pop()

# Rotor branch
d += elm.Line().right()
d += elm.Inductor().label("jX2")
d += elm.Resistor().label("R2/s")
d += elm.Line().down()
d += elm.Line().left(15)
# =========================
# SAFE RENDER (NO STREAMLIT CRASH)
# =========================

buf = io.BytesIO()
d.save(buf)   # save as image in memory
buf.seek(0)

st.image(buf)

# =========================
# THEORY
# =========================
with st.expander("📘 Theory"):
    st.markdown("""
- Torque is proportional to air-gap power  
- Operating point depends on slip  
- Starting torque is finite and non-zero  
- Maximum torque occurs at specific slip  

### Key Equation:
Torque = Air-gap Power / synchronous angular speed  
""")
