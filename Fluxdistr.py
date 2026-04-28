# ============================================================
# RESULTANT AIR-GAP FLUX WAVEFORM WITH POLE EFFECT
# 3-PHASE INDUCTION MOTOR
# Correctly changes spatial flux distribution with pole number
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Pole-Dependent Air-Gap Flux", layout="wide")

st.title("⚡ Resultant Air-Gap Flux Waveform with Pole Variation")
st.markdown("### Flux waveform correctly changes with number of poles")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density (Bm)", 0.5, 2.0, 1.0)
wt_deg = st.sidebar.slider("Electrical Angle ωt (electrical degrees)", 0, 360, 0)

wt = np.radians(wt_deg)

# ---------------- SPACE AXIS ----------------
theta_mech_deg = np.linspace(0, 360, 1440)
theta_mech = np.radians(theta_mech_deg)

# Pole pairs
p = pole // 2

# ============================================================
# IMPORTANT:
# Electrical angle in space = p * mechanical angle
# More poles => more spatial cycles around air-gap
# ============================================================
B = 1.5 * Bm * np.cos(p * theta_mech - wt)

Ns = 120 * f / pole

# ============================================================
# METRICS
# ============================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Supply Frequency", f"{f} Hz")
col2.metric("Number of Poles", f"{pole}")
col3.metric("Pole Pairs", f"{p}")
col4.metric("Synchronous Speed", f"{Ns:.1f} RPM")

# ============================================================
# AIR-GAP STRUCTURAL VIEW
# ============================================================
st.subheader("🌀 Air-Gap Flux Waveform on Mechanical Axis")

fig, ax = plt.subplots(figsize=(10,10))

# Radii
r_rotor = 0.72
r_axis = 0.88
r_stator = 1.02

# Rotor + stator
rotor = Circle((0,0), r_rotor, fill=False, linewidth=3)
stator = Circle((0,0), r_stator, fill=False, linewidth=3)

ax.add_patch(rotor)
ax.add_patch(stator)

# Mechanical axis
axis_circle = Circle((0,0), r_axis, fill=False, linestyle='--', linewidth=1.5)
ax.add_patch(axis_circle)

# Main x-y axes
ax.plot([-r_stator, r_stator], [0,0], linestyle='--', linewidth=1)
ax.plot([0,0], [-r_stator, r_stator], linestyle='--', linewidth=1)

# ============================================================
# FLUX WAVEFORM
# ============================================================
scale = 0.18 / np.max(np.abs(B))

R_wave = r_axis + scale * B

X_wave = R_wave * np.cos(theta_mech)
Y_wave = R_wave * np.sin(theta_mech)

ax.plot(X_wave, Y_wave, linewidth=4)

# ============================================================
# DRAW MULTIPLE POLES
# ============================================================
for k in range(pole):
    pole_angle = wt/p + k * (2*np.pi/pole)

    # Alternate N/S poles
    label = "N" if k % 2 == 0 else "S"

    ax.text(
        1.12*np.cos(pole_angle),
        1.12*np.sin(pole_angle),
        label,
        fontsize=14,
        fontweight='bold',
        ha='center',
        va='center'
    )

# ============================================================
# DEGREE LABELS
# ============================================================
for ang in [0, 90, 180, 270]:
    a = np.radians(ang)
    ax.text(
        1.22*np.cos(a),
        1.22*np.sin(a),
        f"{ang}°",
        fontsize=10,
        fontweight='bold',
        ha='center'
    )

# ============================================================
# LABELS
# ============================================================
ax.text(0, 0, "ROTOR", ha='center', va='center',
        fontsize=14, fontweight='bold')

ax.text(0, 1.28, "STATOR", ha='center',
        fontsize=15, fontweight='bold')

ax.text(0, -1.28,
        f"{pole}-Pole Flux Distribution",
        ha='center', fontsize=12)

# ============================================================
# FORMAT
# ============================================================
ax.set_aspect('equal')
ax.set_xlim(-1.35, 1.35)
ax.set_ylim(-1.35, 1.35)
ax.axis('off')

st.pyplot(fig)

# ============================================================
# LINEAR DISTRIBUTION
# ============================================================
st.subheader("📈 Flux Density vs Mechanical Space Angle")

fig2, ax2 = plt.subplots(figsize=(14,6))

ax2.plot(theta_mech_deg, B, linewidth=4)

ax2.axhline(0, linestyle='--', linewidth=1)

# Pole boundaries
for k in range(pole + 1):
    angle = k * 360 / pole
    ax2.axvline(angle, linestyle=':', linewidth=1)

ax2.set_title(f"{pole}-Pole Resultant Flux Distribution")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("Flux Density B (pu)")

ax2.set_xticks(np.arange(0, 361, 360/pole))

ax2.grid(True)

st.pyplot(fig2)

# ============================================================
# POLAR VIEW
# ============================================================
st.subheader("🧭 Polar Flux Distribution")

fig3 = plt.figure(figsize=(8,8))
ax3 = fig3.add_subplot(111, projection='polar')

ax3.plot(theta_mech, B, linewidth=3)

ax3.set_title(f"{pole}-Pole Rotating Flux Pattern")

st.pyplot(fig3)

# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Pole Effect on Flux Distribution")

st.markdown(f"""
### Correct Pole-Dependent Flux Equation:
**B(θ,t) = 1.5 Bm cos(pθ − ωt)**

Where:

**p = P/2 = {p}**

---

## Key Meaning:
### 2-Pole:
1 spatial cycle over 360°

### 4-Pole:
2 spatial cycles over 360°

### 6-Pole:
3 spatial cycles over 360°

### 8-Pole:
4 spatial cycles over 360°

---

## Important:
Increasing poles increases the number of North-South pole pairs around the stator circumference.

### Synchronous Speed:
**Ns = 120f/P = {Ns:.1f} RPM**
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ More poles create more spatial flux waves around the air-gap, reducing synchronous speed.")
