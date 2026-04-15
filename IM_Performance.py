import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Induction Motor Performance", layout="wide")

st.title("⚡ Induction Motor Performance Analysis")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Motor Parameters")

V = st.sidebar.slider("Supply Voltage (V)", 100, 500, 400)
f = st.sidebar.slider("Frequency (Hz)", 10, 100, 50)
P = st.sidebar.selectbox("Poles", [2, 4, 6, 8], index=1)

R1 = st.sidebar.slider("Stator Resistance R1 (Ω)", 0.1, 5.0, 0.5)
X1 = st.sidebar.slider("Stator Reactance X1 (Ω)", 0.1, 5.0, 1.0)

R2 = st.sidebar.slider("Rotor Resistance R2 (Ω)", 0.1, 5.0, 0.8)
X2 = st.sidebar.slider("Rotor Reactance X2 (Ω)", 0.1, 5.0, 1.2)

Xm = st.sidebar.slider("Magnetizing Reactance Xm (Ω)", 5.0, 100.0, 30.0)

slip = st.sidebar.slider("Slip (s)", 0.001, 1.0, 0.05)

# --- CALCULATIONS ---

# Synchronous speed
Ns = 120 * f / P

# Rotor speed
Nr = Ns * (1 - slip)

# Equivalent circuit calculations
Z1 = R1 + 1j * X1
Z2 = (R2 / slip) + 1j * X2
Zm = 1j * Xm

# Parallel branch
Zp = (Zm * Z2) / (Zm + Z2)

# Total impedance
Z_total = Z1 + Zp

# Current
I1 = V / Z_total

# Power factor
pf = np.cos(np.angle(I1))

# Input power
Pin = np.sqrt(3) * V * abs(I1) * pf

# Air-gap power
Pag = 3 * (abs(I1)**2) * (R2 / slip)

# Mechanical power
Pm = Pag * (1 - slip)

# Output power (approx)
Pout = Pm

# Torque
omega_s = 2 * np.pi * Ns / 60
T = Pag / omega_s

# Efficiency
eff = (Pout / Pin) * 100

# --- TORQUE-SLIP CURVE ---
s = np.linspace(0.001, 1, 400)
T_curve = (s * V**2 * R2) / (R2**2 + (s * X2)**2)
T_curve = T_curve / max(T_curve)

T_op = (slip * V**2 * R2) / (R2**2 + (slip * X2)**2)
T_op = T_op / max(T_curve)

fig, ax = plt.subplots()
ax.plot(s, T_curve, label="Torque-Slip Curve")
ax.scatter(slip, T_op)
ax.text(slip, T_op, "  Operating Point")

ax.set_xlabel("Slip")
ax.set_ylabel("Torque (pu)")
ax.set_title("Torque-Slip Characteristic")
ax.grid()

st.pyplot(fig)

# --- DASHBOARD ---
st.subheader("📊 Performance Results")

col1, col2, col3 = st.columns(3)

col1.metric("Synchronous Speed", f"{Ns:.1f} RPM")
col2.metric("Rotor Speed", f"{Nr:.1f} RPM")
col3.metric("Slip", f"{slip:.3f}")

col4, col5, col6 = st.columns(3)

col4.metric("Input Power", f"{Pin/1000:.2f} kW")
col5.metric("Output Power", f"{Pout/1000:.2f} kW")
col6.metric("Efficiency", f"{eff:.2f} %")

col7, col8, col9 = st.columns(3)

col7.metric("Torque", f"{T:.2f} Nm")
col8.metric("Power Factor", f"{pf:.2f}")
col9.metric("Stator Current", f"{abs(I1):.2f} A")

# --- THEORY ---
st.divider()
st.info("""
**Understanding Performance:**

- Slip ↑ → Torque ↑ (initially), then decreases  
- Maximum torque occurs when R2 = sX2  
- Efficiency is highest at low slip  
- Rotor copper loss = s × Air-gap power  
""")
