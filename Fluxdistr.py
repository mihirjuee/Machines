# ============================================================
# RESULTANT AIR-GAP FLUX DENSITY DISTRIBUTION (SIGNED B)
# 3-PHASE INDUCTION MOTOR
# Shows:
# ✅ Positive + Negative flux density
# ✅ Full 360° sinusoidal air-gap distribution
# ✅ North/South polarity clearly visible
# ✅ Continuous rotating field
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Signed Air-Gap Flux Density", layout="wide")

st.title("⚡ Resultant Flux Density Distribution in the Entire Air-Gap")
st.markdown("### Showing positive and negative flux density (North & South poles)")

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

# Signed resultant flux density
# Positive = North polarity
# Negative = South polarity
B_resultant = 1.5 * Bm * np.cos(theta - wt)

Ns = 120 * f / pole

# ============================================================
# METRICS
# ============================================================
col1, col2, col3 = st.columns(3)

col1.metric("Synchronous Speed", f"{Ns:.1f} RPM")
col2.metric("Electrical Angle", f"{wt_deg}°")
col3.metric("Peak Flux Density", f"±{np.max(np.abs(B_resultant)):.2f} pu")

# ============================================================
# PLOT 1: FULL AIR-GAP CROSS SECTION
# ============================================================
st.subheader("🌀 Signed Flux Density Across Full Air-Gap")

fig1, ax1 = plt.subplots(figsize=(10,10))

# Air-gap radial region
r = np.linspace(0.75, 1.0, 100)
Theta, R = np.meshgrid(theta, r)

# Signed flux map
B_map = 1.5 * Bm * np.cos(Theta - wt)

# Polar → Cartesian
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Signed contour map
# Positive and negative regions visible
contour = ax1.contourf(X, Y, B_map, levels=200, cmap="seismic")

# Rotor + stator
rotor = Circle((0, 0), 0.75, fill=False, linewidth=3)
stator = Circle((0, 0), 1.0, fill=False, linewidth=3)

ax1.add_patch(rotor)
ax1.add_patch(stator)

# Flux axis (North)
x_n = 0.68 * np.cos(wt)
y_n = 0.68 * np.sin(wt)

# Flux axis (South)
x_s = -0.68 * np.cos(wt)
y_s = -0.68 * np.sin(wt)

# North vector
ax1.arrow(
    0, 0, x_n, y_n,
    head_width=0.05,
    head_length=0.08,
    linewidth=4
)

# South vector
ax1.arrow(
    0, 0, x_s, y_s,
    head_width=0.05,
    head_length=0.08,
    linewidth=4
)

# Labels
ax1.text(x_n*1.15, y_n*1.15, "N", fontsize=16, fontweight="bold")
ax1.text(x_s*1.15, y_s*1.15, "S", fontsize=16, fontweight="bold")

ax1.text(0, 0, "ROTOR", ha='center', va='center',
         fontsize=14, fontweight='bold')

ax1.text(0, 1.22, "STATOR", ha='center',
         fontsize=15, fontweight='bold')

ax1.set_aspect('equal')
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.axis('off')

cbar = plt.colorbar(contour)
cbar.set_label("Flux Density B (pu)\n(+ = North, - = South)")

st.pyplot(fig1)

# ============================================================
# PLOT 2: SIGNED B vs SPACE ANGLE
# ============================================================
st.subheader("📈 Signed Flux Density Around Entire Circumference")

fig2, ax2 = plt.subplots(figsize=(14,6))

ax2.plot(theta_deg, B_resultant, linewidth=4)

# Zero axis
ax2.axhline(0, linestyle='--', linewidth=1)

# North and South axes
ax2.axvline(wt_deg % 360, linestyle='--', linewidth=2, label="North Pole Axis")
ax2.axvline((wt_deg + 180) % 360, linestyle='--', linewidth=2, label="South Pole Axis")

ax2.set_title("Resultant Signed Air-Gap Flux Density")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("Flux Density B (pu)")

ax2.set_xticks([0, 60, 120, 180, 240, 300, 360])

ax2.grid(True)
ax2.legend()

st.pyplot(fig2)

# ============================================================
# PLOT 3: POLAR SIGNED DISTRIBUTION
# ============================================================
st.subheader("🧭 Polar Signed Flux Wave")

fig3 = plt.figure(figsize=(8,8))
ax3 = fig3.add_subplot(111, projection='polar')

ax3.plot(theta, B_resultant, linewidth=3)

ax3.set_title("Positive + Negative Resultant Flux Wave")

st.pyplot(fig3)

# ============================================================
# ROTATION SNAPSHOTS
# ============================================================
st.subheader("⏱ Signed Flux Rotation at Different Instants")

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
### Signed Resultant Flux Density:
**B(θ,t) = 1.5 Bm cos(θ − ωt)**

---

## Interpretation:
### Positive Region:
North pole flux direction

### Negative Region:
South pole flux direction

---

## Key Insight:
- One half-cycle = North pole
- Opposite half-cycle = South pole
- Entire wave rotates
- Magnitude constant
- Polarity changes with space angle

### Synchronous Speed:
**Ns = 120f/P = {Ns:.1f} RPM**
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ The positive and negative halves of the air-gap flux wave represent rotating North and South magnetic poles.")
