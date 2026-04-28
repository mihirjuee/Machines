# ============================================================
# 3-PHASE INDUCTION MOTOR COMPLETE AIR-GAP FLUX DENSITY MAP
# Shows:
# ✅ Full 360° air-gap flux density distribution
# ✅ Spatial flux density around entire air-gap
# ✅ Flux contour map
# ✅ Instantaneous rotating field
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Complete Air-Gap Flux Density", layout="wide")

st.title("⚡ Complete Air-Gap Flux Density Distribution in 3-Phase Induction Motor")
st.markdown("### Visualizing flux density across the entire 360° air-gap")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density", 0.5, 2.0, 1.0)
wt_deg = st.sidebar.slider("Electrical Angle ωt (degrees)", 0, 360, 0)

wt = np.radians(wt_deg)

# ---------------- AIR-GAP GRID ----------------
# Spatial angle around full circumference
theta_deg = np.linspace(0, 360, 720)
theta = np.radians(theta_deg)

# Radial air-gap thickness
r = np.linspace(0.75, 1.0, 80)

Theta, R = np.meshgrid(theta, r)

# ---------------- FLUX DENSITY EQUATIONS ----------------
# 3-phase spatial fluxes
B_R = Bm * np.cos(Theta - wt)
B_Y = Bm * np.cos(Theta - wt + 2*np.pi/3)
B_B = Bm * np.cos(Theta - wt - 2*np.pi/3)

# Resultant flux density
B_total = B_R + B_Y + B_B

# =======================
# METRICS
# =======================
Ns = 120 * f / pole

col1, col2, col3 = st.columns(3)

col1.metric("Synchronous Speed", f"{Ns:.1f} RPM")
col2.metric("Electrical Angle", f"{wt_deg}°")
col3.metric("Peak Flux Density", f"{np.max(B_total):.2f} pu")

# ============================================================
# PLOT 1: COMPLETE AIR-GAP CROSS SECTION
# ============================================================
st.subheader("🌀 Complete Air-Gap Flux Density (Entire Circumference)")

fig1, ax1 = plt.subplots(figsize=(10,10))

# Convert polar to cartesian
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

contour = ax1.contourf(X, Y, B_total, levels=100)

# Rotor and stator boundaries
rotor = Circle((0,0), 0.75, fill=False, linewidth=3)
stator = Circle((0,0), 1.0, fill=False, linewidth=3)

ax1.add_patch(rotor)
ax1.add_patch(stator)

# Resultant field vector
x_res = 0.65 * np.cos(wt)
y_res = 0.65 * np.sin(wt)

ax1.arrow(
    0, 0, x_res, y_res,
    head_width=0.05,
    head_length=0.08,
    linewidth=4
)

# Phase labels
phase_angles = [90, 210, 330]
phase_names = ["R", "Y", "B"]

for ang, name in zip(phase_angles, phase_names):
    a = np.radians(ang)
    ax1.text(1.15*np.cos(a), 1.15*np.sin(a), f"Phase {name}",
             ha='center', fontsize=12, fontweight='bold')

ax1.text(0, 0, "ROTOR", ha='center', va='center', fontsize=14, fontweight='bold')
ax1.text(0, 1.25, "STATOR", ha='center', fontsize=14, fontweight='bold')

ax1.set_aspect('equal')
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.axis('off')

cbar = plt.colorbar(contour)
cbar.set_label("Flux Density (pu)")

st.pyplot(fig1)

# ============================================================
# PLOT 2: AIR-GAP FLUX DENSITY vs SPACE ANGLE
# ============================================================
st.subheader("📈 Flux Density Around Full Air-Gap Circumference")

fig2, ax2 = plt.subplots(figsize=(14,6))

ax2.plot(theta_deg, B_R[0], label="Phase R Flux Density", linewidth=2)
ax2.plot(theta_deg, B_Y[0], label="Phase Y Flux Density", linewidth=2)
ax2.plot(theta_deg, B_B[0], label="Phase B Flux Density", linewidth=2)
ax2.plot(theta_deg, B_total[0], label="Resultant Flux Density", linewidth=4)

ax2.set_title("Flux Density Distribution Across Entire Air Gap")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("Flux Density (pu)")
ax2.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax2.grid(True)
ax2.legend()

st.pyplot(fig2)

# ============================================================
# PLOT 3: POLAR FLUX DENSITY
# ============================================================
st.subheader("🧭 Polar Representation of Flux Density")

fig3 = plt.figure(figsize=(8,8))
ax3 = fig3.add_subplot(111, projection='polar')

# Shift negative values outward for visibility
flux_positive = B_total[0]

ax3.plot(theta, flux_positive, linewidth=3)
ax3.set_title("360° Air-Gap Flux Density Pattern")

st.pyplot(fig3)

# ============================================================
# TIME EVOLUTION ANIMATION-LIKE SNAPSHOTS
# ============================================================
st.subheader("⏱ Flux Rotation Principle")

snapshot_angles = [0, 90, 180, 270]

cols = st.columns(4)

for idx, angle_deg in enumerate(snapshot_angles):
    angle = np.radians(angle_deg)
    B_snap = (
        Bm*np.cos(theta-angle)
        + Bm*np.cos(theta-angle+2*np.pi/3)
        + Bm*np.cos(theta-angle-2*np.pi/3)
    )

    fig_snap = plt.figure(figsize=(3,3))
    ax_snap = fig_snap.add_subplot(111, projection='polar')
    ax_snap.plot(theta, B_snap, linewidth=2)
    ax_snap.set_title(f"{angle_deg}°")

    cols[idx].pyplot(fig_snap)

# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Key Concept")

st.markdown(f"""
### Air-Gap Flux Density Equation:
**B(θ,t) = BR + BY + BB**

Where:

**BR = Bm cos(θ − ωt)**  
**BY = Bm cos(θ − ωt + 120°)**  
**BB = Bm cos(θ − ωt − 120°)**  

### Result:
### Btotal = 1.5 Bm cos(θ − ωt)

---

## Meaning:
- Flux exists across the full 360° air-gap
- Magnitude remains constant
- Pattern rotates at synchronous speed
- Creates electromagnetic torque

### Synchronous Speed:
**Ns = 120f/P = {Ns:.1f} RPM**
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ The entire air-gap flux wave rotates as a constant-amplitude sinusoidal field — this is the heart of induction motor operation.")
