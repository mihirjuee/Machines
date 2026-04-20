import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(page_title="IM Equivalent Circuit Lab", page_icon="⚡", layout="wide")

# =========================
# 🎨 STYLE
# =========================
st.markdown("""
<style>

.main {
    background: linear-gradient(120deg, #1f4037, #2c7744);
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #f7f9fb !important;
}

section[data-testid="stSidebar"] * {
    color: black !important;
    font-weight: 500;
}

.stMetric {
    background-color: rgba(255,255,255,0.12);
    padding: 12px;
    border-radius: 10px;
}

h1, h2, h3 {
    color: #00ffcc;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("⚡ Induction Motor Equivalent Circuit Lab")
st.subheader("Torque-Speed Curve with Operating Point")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Motor Parameters")

V_line = st.sidebar.slider("Line Voltage (V)", 200, 500, 400)
f = st.sidebar.slider("Frequency (Hz)", 40, 60, 50)

R1 = st.sidebar.slider("R1 (Ω)", 0.1, 5.0, 0.5)
X1 = st.sidebar.slider("X1 (Ω)", 0.1, 5.0, 1.0)

R2 = st.sidebar.slider("R2 (Ω)", 0.1, 5.0, 0.4)
X2 = st.sidebar.slider("X2 (Ω)", 0.1, 5.0, 0.8)

Xm = st.sidebar.slider("Xm (Ω)", 5.0, 100.0, 30.0)
Rc = st.sidebar.slider("Rc (Ω)", 10.0, 500.0, 150.0)

slip = st.sidebar.slider("Operating Slip (s)", 0.01, 1.0, 0.05)


# =========================
# CALCULATIONS
# =========================
V_phase = V_line / np.sqrt(3)

Z1 = complex(R1, X1)

Ns = 120 * f / 4
ws = 2 * np.pi * Ns / 60

# Magnetizing + core loss branch
Zm = 1 / (1/Rc + 1/complex(0, Xm))

# =========================
# OPERATING POINT CALCULATION
# =========================
Z2_op = complex(R2/slip, X2)
Zp_op = (Z2_op * Zm) / (Z2_op + Zm)
Zt_op = Z1 + Zp_op

I_op = V_phase / Zt_op
P_ag_op = 3 * (abs(I_op)**2) * (R2/slip)
T_op = P_ag_op / ws

operating_speed = (1 - slip) * Ns

# =========================
# TORQUE-SPEED CURVE
# =========================
s_vals = np.linspace(1.0, 0.01, 60)
torque_vals = []

for s in s_vals:

    Z2 = complex(R2/s, X2)
    Zm = 1 / (1/Rc + 1/complex(0, Xm))
    Zp = (Z2 * Zm) / (Z2 + Zm)
    Zt = Z1 + Zp

    I = V_phase / Zt
    P_ag = 3 * (abs(I)**2) * (R2/s)

    T = P_ag / ws   # ✅ correct torque

    torque_vals.append(T)

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
P_core = 3 * (abs(V_phase)**2) / Rc
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
d += elm.Inductor().right().label("X1")

d += elm.Dot()
d.push()

# Rc branch
d += elm.Line().down(0.1)
d += elm.Resistor().label("Rc")

d.pop()
d.push()
# Xm branch
d += elm.Line().right()
d += elm.Dot()
d += elm.Line().down(0.1)
d += elm.Inductor().label("Xm")

d.pop()

# Rotor branch
d += elm.Line().right()
d += elm.Inductor().label("X2")
d += elm.Resistor().label("R2/s")
d += elm.Line().down()
d += elm.Line().left(10)
d += elm.Line().up()
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
