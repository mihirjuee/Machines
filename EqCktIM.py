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
# 🎨 UI STYLE
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(120deg, #1f4037, #2c7744);
    color: white;
}
section[data-testid="stSidebar"] {
    background: #1c1c1c;
}
h1, h2, h3 {
    color: #00ffcc;
}
.stMetric {
    background-color: rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏷️ TITLE
# =========================
st.title("⚡ Induction Motor Equivalent Circuit Lab")
st.subheader("With Core Loss Branch (Rc)")

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("⚙️ Motor Parameters")

V_line = st.sidebar.slider("Line Voltage (V)", 200, 500, 400)
f = st.sidebar.slider("Frequency (Hz)", 40, 60, 50)

R1 = st.sidebar.slider("Stator Resistance R1 (Ω)", 0.1, 5.0, 0.5)
X1 = st.sidebar.slider("Stator Reactance X1 (Ω)", 0.1, 5.0, 1.0)

R2 = st.sidebar.slider("Rotor Resistance R2 (Ω)", 0.1, 5.0, 0.4)
X2 = st.sidebar.slider("Rotor Reactance X2 (Ω)", 0.1, 5.0, 0.8)

Xm = st.sidebar.slider("Magnetizing Reactance Xm (Ω)", 5.0, 100.0, 30.0)
Rc = st.sidebar.slider("Core Loss Resistance Rc (Ω)", 10.0, 500.0, 150.0)

slip = st.sidebar.slider("Slip (s)", 0.01, 1.0, 0.05)

# =========================
# CALCULATIONS
# =========================
V_phase = V_line / np.sqrt(3)

Z1 = complex(R1, X1)
Z2 = complex(R2/slip, X2)

# Core loss + magnetizing branch
Zm = 1 / (1/Rc + 1/complex(0, Xm))

# Parallel combination
Z_parallel = (Z2 * Zm) / (Z2 + Zm)

Z_total = Z1 + Z_parallel

I1 = V_phase / Z_total
pf = np.cos(np.angle(I1))

P_input = 3 * V_phase * abs(I1) * pf

# Core loss
V_airgap = abs(V_phase - I1 * Z1)
P_core = 3 * (V_airgap**2) / Rc

# Air-gap power
P_ag = 3 * (abs(I1)**2) * (R2/slip)

# Mechanical power
P_mech = P_ag * (1 - slip)

# Efficiency
eff = P_mech / P_input

# Torque
Ns = 120 * f / 4
ws = 2 * np.pi * Ns / 60
Torque = P_mech / ws

# =========================
# METRICS
# =========================
st.subheader("📊 Performance Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Input Current", f"{abs(I1):.2f} A")
c2.metric("Power Factor", f"{pf:.2f}")
c3.metric("Efficiency", f"{eff*100:.1f} %")
c4.metric("Torque", f"{Torque:.2f} Nm")

# =========================
# POWER FLOW
# =========================
st.subheader("⚡ Power Flow")

st.info(f"""
Input Power = {P_input:.2f} W  
Core Loss = {P_core:.2f} W  
Air-gap Power = {P_ag:.2f} W  
Mechanical Power = {P_mech:.2f} W  
Rotor Loss = {P_ag - P_mech:.2f} W  
""")

# =========================
# TORQUE-SPEED CURVE
# =========================
st.subheader("📈 Torque-Speed Curve")

s_vals = np.linspace(0.01, 1, 50)
torque_vals = []

for s in s_vals:
    Z2 = complex(R2/s, X2)
    Zm = 1 / (1/Rc + 1/complex(0, Xm))
    Zp = (Z2 * Zm) / (Z2 + Zm)
    Zt = Z1 + Zp
    I = V_phase / Zt
    P_ag = 3 * (abs(I)**2) * (R2/s)
    P_mech = P_ag * (1 - s)
    T = P_mech / ws
    torque_vals.append(T)

speed = (1 - s_vals) * Ns

fig, ax = plt.subplots()
ax.plot(speed, torque_vals)
ax.set_xlabel("Speed (RPM)")
ax.set_ylabel("Torque (Nm)")
ax.set_title("Torque-Speed Characteristic")
ax.grid()

st.pyplot(fig)

# =========================
# CIRCUIT DIAGRAM
# =========================
st.subheader("🔌 Equivalent Circuit with Core Loss")

d = schemdraw.Drawing()

d += elm.SourceV().label("Vph")
d += elm.Resistor().right().label("R1")
d += elm.Inductor().right().label("X1")

d += elm.Dot()
d.push()

# Rc branch
d += elm.Line().down()
d += elm.Resistor().label("Rc")
d += elm.Ground()

d.pop()
d.push()

# Xm branch
d += elm.Line().down()
d += elm.Inductor().label("Xm")
d += elm.Ground()

d.pop()

# Rotor branch
d += elm.Line().right()
d += elm.Resistor().label("R2/s")
d += elm.Inductor().label("X2")
d += elm.Ground()

st.pyplot(d.draw())

# =========================
# THEORY
# =========================
with st.expander("📘 Theory"):
    st.markdown("""
- Rc represents iron/core losses (hysteresis + eddy current)
- Xm represents magnetizing current
- Both are in parallel (no-load branch)

### Updated Model:
Z_m = Rc || jXm

Adding Rc improves:
✔ Efficiency accuracy  
✔ Power flow realism  
✔ No-load current prediction  
""")
