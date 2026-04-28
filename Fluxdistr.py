# ============================================================
# 3-PHASE INDUCTION MOTOR AIR-GAP RESULTANT FLUX DISTRIBUTION
# WITH STRUCTURAL DIAGRAM
# Streamlit App
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="3-Phase Air-Gap Flux Distribution", layout="wide")

st.title("⚡ 3-Phase Induction Motor Resultant Flux Distribution")
st.markdown("### Air-gap flux waves + rotating magnetic field + motor structural diagram")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density (pu)", 0.5, 2.0, 1.0)
wt_deg = st.sidebar.slider("Electrical Angle ωt (degrees)", 0, 360, 0)

# ---------------- CALCULATIONS ----------------
wt = np.radians(wt_deg)

theta_deg = np.linspace(0, 360, 1000)
theta = np.radians(theta_deg)

# Space flux waves
phi_R = Bm * np.cos(theta - wt)
phi_Y = Bm * np.cos(theta - wt + 2*np.pi/3)
phi_B = Bm * np.cos(theta - wt - 2*np.pi/3)

phi_resultant = phi_R + phi_Y + phi_B

Ns = 120 * f / pole

# ============================================================
# METRICS
# ============================================================
col1, col2, col3 = st.columns(3)

col1.metric("Synchronous Speed", f"{Ns:.1f} RPM")
col2.metric("Electrical Angle", f"{wt_deg}°")
col3.metric("Resultant Flux Peak", f"{np.max(phi_resultant):.2f} pu")

# ============================================================
# STRUCTURAL DIAGRAM
# ============================================================
st.subheader("🛠 Structural Diagram of 3-Phase Induction Motor")

fig0, ax0 = plt.subplots(figsize=(8,8))

# Stator outer circle
stator_outer = Circle((0, 0), 1.0, fill=False, linewidth=4)
# Stator inner circle
stator_inner = Circle((0, 0), 0.75, fill=False, linewidth=3)

# Rotor
rotor = Circle((0, 0), 0.45, fill=False, linewidth=4)

ax0.add_patch(stator_outer)
ax0.add_patch(stator_inner)
ax0.add_patch(rotor)

# Phase winding positions
phase_angles_deg = [90, 210, 330]
phase_labels = ["R", "Y", "B"]

for angle_deg, label in zip(phase_angles_deg, phase_labels):
    angle = np.radians(angle_deg)
    
    # Coil position
    x1, y1 = 0.75*np.cos(angle), 0.75*np.sin(angle)
    x2, y2 = 1.0*np.cos(angle), 1.0*np.sin(angle)
    
    ax0.plot([x1, x2], [y1, y2], linewidth=6)
    
    # Label
    xt, yt = 1.15*np.cos(angle), 1.15*np.sin(angle)
    ax0.text(xt, yt, f"Phase {label}", fontsize=14, fontweight='bold', ha='center')

# Resultant rotating field vector
x_res = 0.7 * np.cos(wt)
y_res = 0.7 * np.sin(wt)

ax0.arrow(
    0, 0, x_res, y_res,
    head_width=0.06,
    head_length=0.08,
    linewidth=4
)

# Rotation arrow
circle_theta = np.linspace(0, 2*np.pi, 200)
ax0.plot(0.6*np.cos(circle_theta), 0.6*np.sin(circle_theta), linestyle='--')

ax0.text(0, 0, "ROTOR", ha='center', va='center', fontsize=14, fontweight='bold')
ax0.text(0, 1.25, "STATOR", ha='center', fontsize=16, fontweight='bold')

ax0.set_xlim(-1.4, 1.4)
ax0.set_ylim(-1.4, 1.4)
ax0.set_aspect('equal')
ax0.axis('off')

st.pyplot(fig0)

# ============================================================
# AIR-GAP FLUX DISTRIBUTION
# ============================================================
st.subheader("🌊 Air-Gap Flux Distribution")

fig1, ax1 = plt.subplots(figsize=(12,6))

ax1.plot(theta_deg, phi_R, label="Phase R Flux (ΦR)", linewidth=2)
ax1.plot(theta_deg, phi_Y, label="Phase Y Flux (ΦY)", linewidth=2)
ax1.plot(theta_deg, phi_B, label="Phase B Flux (ΦB)", linewidth=2)
ax1.plot(theta_deg, phi_resultant, label="Resultant Flux (Φres)", linewidth=4)

ax1.set_title("Flux Distribution in Air Gap")
ax1.set_xlabel("Space Angle (degrees)")
ax1.set_ylabel("Flux Density (pu)")
ax1.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax1.grid(True)
ax1.legend()

st.pyplot(fig1)

# ============================================================
# POLAR ROTATION
# ============================================================
st.subheader("🧭 Resultant Rotating Magnetic Field")

fig2 = plt.figure(figsize=(8,8))
ax2 = fig2.add_subplot(111, projection='polar')

ax2.arrow(
    wt, 0,
    0, 1.5*Bm,
    width=0.02,
    head_width=0.1,
    head_length=0.15
)

angles = np.linspace(0, 2*np.pi, 360)
ax2.plot(angles, np.ones_like(angles)*Bm, linestyle='--')

ax2.set_title("Rotating Flux Vector")
st.pyplot(fig2)

# ============================================================
# TIME WAVEFORMS
# ============================================================
st.subheader("📈 Three-Phase Time Waveforms")

t_deg = np.linspace(0, 360, 1000)
t = np.radians(t_deg)

FR = Bm * np.sin(t)
FY = Bm * np.sin(t - 2*np.pi/3)
FB = Bm * np.sin(t - 4*np.pi/3)

fig3, ax3 = plt.subplots(figsize=(12,5))

ax3.plot(t_deg, FR, label="Phase R")
ax3.plot(t_deg, FY, label="Phase Y")
ax3.plot(t_deg, FB, label="Phase B")

ax3.axvline(wt_deg, linestyle='--', linewidth=2, label="Current ωt")

ax3.set_title("3-Phase Fluxes in Time")
ax3.set_xlabel("Electrical Angle (degrees)")
ax3.set_ylabel("Flux")
ax3.grid(True)
ax3.legend()

st.pyplot(fig3)

# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Theory")

st.markdown(f"""
### Rotating Magnetic Field Principle:
Balanced 3-phase currents produce 3 sinusoidal fluxes displaced by 120° in space and time.

### Equations:
ΦR = Φm cos(θ − ωt)  
ΦY = Φm cos(θ − ωt + 120°)  
ΦB = Φm cos(θ − ωt − 120°)

### Result:
### Constant magnitude rotating flux:
Φres = 1.5 Φm

### Synchronous Speed:
Ns = 120f/P = {Ns:.1f} RPM
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ This rotating air-gap flux is what produces torque in a three-phase induction motor.")
