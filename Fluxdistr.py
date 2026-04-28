# ============================================================
# RESULTANT AIR-GAP FLUX DENSITY ONLY
# 3-PHASE INDUCTION MOTOR
# Shows:
# ✅ Only resultant rotating magnetic field
# ✅ Full 360° air-gap sinusoidal flux density
# ✅ Polar air-gap map
# ✅ Structural stator-rotor view
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Resultant Air-Gap Flux", layout="wide")

st.title("⚡ Resultant Flux Density in the Entire Air-Gap")
st.markdown("### Three-Phase Induction Motor — Rotating Magnetic Field Only")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density (Bm)", 0.5, 2.0, 1.0)
wt_deg = st.sidebar.slider("Electrical Angle ωt (degrees)", 0, 360, 0)

wt = np.radians(wt_deg)

# ---------------- CALCULATIONS ----------------
theta_deg = np.linspace(0, 360, 1000)
theta = np.radians(theta_deg)

# Resultant rotating flux density
# B_resultant = 1.5 * Bm * cos(theta - wt)
B_resultant = 1.5 * Bm * np.cos(theta - wt)

Ns = 120 * f / pole

# ============================================================
# METRICS
# ============================================================
col1, col2, col3 = st.columns(3)

col1.metric("Synchronous Speed", f"{Ns:.1f} RPM")
col2.metric("Electrical Angle", f"{wt_deg}°")
col3.metric("Peak Resultant Flux", f"{np.max(B_resultant):.2f} pu")

# ============================================================
# PLOT 1: STRUCTURAL AIR-GAP VIEW (ONLY RESULTANT)
# ============================================================
st.subheader("🌀 Resultant Rotating Flux in Full Air-Gap")

fig1, ax1 = plt.subplots(figsize=(9,9))

# Air-gap region
r = np.linspace(0.75, 1.0, 80)
Theta, R = np.meshgrid(theta, r)

# Flux density map repeated radially
B_map = 1.5 * Bm * np.cos(Theta - wt)

# Convert polar to Cartesian
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Contour map
contour = ax1.contourf(X, Y, B_map, levels=100)

# Rotor and stator boundaries
rotor = Circle((0, 0), 0.75, fill=False, linewidth=3)
stator = Circle((0, 0), 1.0, fill=False, linewidth=3)

ax1.add_patch(rotor)
ax1.add_patch(stator)

# Resultant rotating vector
x_res = 0.68 * np.cos(wt)
y_res = 0.68 * np.sin(wt)

ax1.arrow(
    0, 0, x_res, y_res,
    head_width=0.06,
    head_length=0.08,
    linewidth=4
)

# Labels
ax1.text(0, 0, "ROTOR", ha='center', va='center',
         fontsize=14, fontweight='bold')

ax1.text(0, 1.2, "STATOR", ha='center',
         fontsize=15, fontweight='bold')

ax1.text(
    0.9*np.cos(wt),
    0.9*np.sin(wt),
    "Resultant Flux Axis",
    fontsize=12,
    fontweight='bold'
)

ax1.set_aspect('equal')
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.axis('off')

cbar = plt.colorbar(contour)
cbar.set_label("Resultant Flux Density (pu)")

st.pyplot(fig1)

# ============================================================
# PLOT 2: FULL 360° AIR-GAP DISTRIBUTION
# ============================================================
st.subheader("📈 Resultant Flux Density Across Entire Air-Gap")

fig2, ax2 = plt.subplots(figsize=(14,6))

ax2.plot(theta_deg, B_resultant, linewidth=4)

ax2.set_title("Resultant Air-Gap Flux Density Distribution")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("Flux Density (pu)")

ax2.set_xticks([0, 60, 120, 180, 240, 300, 360])

ax2.grid(True)

# Peak axis
ax2.axvline(wt_deg, linestyle='--', linewidth=2,
            label="Flux Axis")

ax2.legend()

st.pyplot(fig2)

# ============================================================
# PLOT 3: POLAR RESULTANT DISTRIBUTION
# ============================================================
st.subheader("🧭 Polar Representation of Resultant Flux")

fig3 = plt.figure(figsize=(8,8))
ax3 = fig3.add_subplot(111, projection='polar')

ax3.plot(theta, B_resultant, linewidth=3)

# Resultant vector
ax3.arrow(
    wt, 0,
    0, 1.5*Bm,
    width=0.02,
    head_width=0.08,
    head_length=0.15
)

ax3.set_title("Rotating Sinusoidal Resultant Flux Wave")

st.pyplot(fig3)

# ============================================================
# SNAPSHOT POSITIONS
# ============================================================
st.subheader("⏱ Rotating Flux at Different Instants")

snapshot_angles = [0, 90, 180, 270]

cols = st.columns(4)

for i, angle_deg in enumerate(snapshot_angles):

    angle = np.radians(angle_deg)

    B_snap = 1.5 * Bm * np.cos(theta - angle)

    fig_snap = plt.figure(figsize=(3,3))
    ax_snap = fig_snap.add_subplot(111, projection='polar')

    ax_snap.plot(theta, B_snap, linewidth=2)
    ax_snap.set_title(f"{angle_deg}°")

    cols[i].pyplot(fig_snap)

# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Mathematical Model")

st.markdown(f"""
### Resultant Air-Gap Flux Density:
**B(θ,t) = 1.5 Bm cos(θ − ωt)**

---

## Key Meaning:
- Only one sinusoidal resultant wave exists in air-gap
- Magnitude = constant
- Shape = sinusoidal
- Rotates continuously
- Speed = synchronous speed

### Synchronous Speed:
**Ns = 120f/P = {Ns:.1f} RPM**

---

## Important:
This rotating field is what cuts rotor conductors and produces induced EMF + torque.
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ The entire 3-phase stator system creates one constant-magnitude rotating flux wave in the air-gap.")
