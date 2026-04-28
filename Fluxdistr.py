# ============================================================
# RESULTANT AIR-GAP FLUX DENSITY WITH AXIS + WAVEFORM
# 3-PHASE INDUCTION MOTOR
# Shows:
# ✅ Mechanical space axis around air-gap
# ✅ Flux waveform directly on air-gap axis
# ✅ Positive & negative poles
# ✅ Resultant rotating magnetic field
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Air-Gap Flux Axis & Waveform", layout="wide")

st.title("⚡ Air-Gap Axis with Resultant Flux Waveform")
st.markdown("### Resultant flux density plotted directly on the air-gap axis")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Motor Parameters")

f = st.sidebar.slider("Supply Frequency (Hz)", 1, 100, 50)
pole = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
Bm = st.sidebar.slider("Maximum Flux Density (Bm)", 0.5, 2.0, 1.0)
wt_deg = st.sidebar.slider("Electrical Angle ωt (degrees)", 0, 360, 0)

wt = np.radians(wt_deg)

# ---------------- CALCULATIONS ----------------
theta_deg = np.linspace(0, 360, 720)
theta = np.radians(theta_deg)

# Resultant flux density
B = 1.5 * Bm * np.cos(theta - wt)

Ns = 120 * f / pole

# ============================================================
# METRICS
# ============================================================
col1, col2, col3 = st.columns(3)

col1.metric("Synchronous Speed", f"{Ns:.1f} RPM")
col2.metric("Electrical Angle", f"{wt_deg}°")
col3.metric("Peak Flux Density", f"±{np.max(np.abs(B)):.2f} pu")

# ============================================================
# MAIN AIR-GAP AXIS + FLUX WAVEFORM
# ============================================================
st.subheader("🌀 Flux Waveform Drawn on the Air-Gap Axis")

fig, ax = plt.subplots(figsize=(10,10))

# Base radii
r_rotor = 0.72
r_axis = 0.88
r_stator = 1.02

# Rotor + stator
rotor = Circle((0,0), r_rotor, fill=False, linewidth=3)
stator = Circle((0,0), r_stator, fill=False, linewidth=3)

ax.add_patch(rotor)
ax.add_patch(stator)

# Air-gap axis circle
axis_circle = Circle((0,0), r_axis, fill=False, linestyle='--', linewidth=1.5)
ax.add_patch(axis_circle)

# ============================================================
# DRAW AXES
# ============================================================
# Horizontal axis (0°–180°)
ax.plot([-r_stator, r_stator], [0, 0], linestyle='--', linewidth=1)

# Vertical axis (90°–270°)
ax.plot([0, 0], [-r_stator, r_stator], linestyle='--', linewidth=1)

# Angular labels
for ang in [0, 90, 180, 270]:
    a = np.radians(ang)
    ax.text(
        1.15*np.cos(a),
        1.15*np.sin(a),
        f"{ang}°",
        fontsize=11,
        fontweight='bold',
        ha='center',
        va='center'
    )

# ============================================================
# FLUX WAVEFORM ON AIR-GAP
# Radius modulated by flux density
# Positive outward, negative inward
# ============================================================
scale = 0.18 / np.max(np.abs(B))

R_wave = r_axis + scale * B

X_wave = R_wave * np.cos(theta)
Y_wave = R_wave * np.sin(theta)

ax.plot(X_wave, Y_wave, linewidth=4)

# ============================================================
# RESULTANT AXIS
# ============================================================
# North pole
x_n = r_axis * np.cos(wt)
y_n = r_axis * np.sin(wt)

# South pole
x_s = r_axis * np.cos(wt + np.pi)
y_s = r_axis * np.sin(wt + np.pi)

# Main magnetic axis
ax.plot([x_s, x_n], [y_s, y_n], linestyle='-', linewidth=3)

# Pole labels
ax.text(1.08*np.cos(wt), 1.08*np.sin(wt), "N",
        fontsize=16, fontweight='bold')

ax.text(1.08*np.cos(wt + np.pi), 1.08*np.sin(wt + np.pi), "S",
        fontsize=16, fontweight='bold')

# ============================================================
# ROTATION ARROW
# ============================================================
arrow_angle = wt + np.pi/4
ax.arrow(
    0.55*np.cos(arrow_angle),
    0.55*np.sin(arrow_angle),
    0.001,
    0.001,
    head_width=0.06,
    head_length=0.08,
    linewidth=2
)

# ============================================================
# LABELS
# ============================================================
ax.text(0, 0, "ROTOR", ha='center', va='center',
        fontsize=14, fontweight='bold')

ax.text(0, 1.28, "STATOR", ha='center',
        fontsize=15, fontweight='bold')

ax.text(0, -1.25, "Mechanical Space Axis",
        ha='center', fontsize=12)

# ============================================================
# FORMATTING
# ============================================================
ax.set_aspect('equal')
ax.set_xlim(-1.35, 1.35)
ax.set_ylim(-1.35, 1.35)
ax.axis('off')

st.pyplot(fig)

# ============================================================
# LINEAR WAVEFORM
# ============================================================
st.subheader("📈 Flux Density vs Mechanical Space Angle")

fig2, ax2 = plt.subplots(figsize=(14,6))

ax2.plot(theta_deg, B, linewidth=4)

ax2.axhline(0, linestyle='--', linewidth=1)

# Magnetic axis markers
ax2.axvline(wt_deg % 360, linestyle='--', linewidth=2, label="N-axis")
ax2.axvline((wt_deg + 180) % 360, linestyle='--', linewidth=2, label="S-axis")

ax2.set_title("Resultant Flux Density Along Air-Gap Axis")
ax2.set_xlabel("Mechanical Space Angle (degrees)")
ax2.set_ylabel("Flux Density B (pu)")

ax2.set_xticks([0, 60, 120, 180, 240, 300, 360])

ax2.grid(True)
ax2.legend()

st.pyplot(fig2)

# ============================================================
# THEORY
# ============================================================
st.markdown("---")
st.subheader("📘 Key Concept")

st.markdown(f"""
### Resultant Flux Density:
**B(θ,t) = 1.5 Bm cos(θ − ωt)**

---

## Interpretation:
- Air-gap axis = mechanical position around stator
- Outward waveform = positive flux (North)
- Inward waveform = negative flux (South)
- Wave rotates with synchronous speed

### Synchronous Speed:
**Ns = 120f/P = {Ns:.1f} RPM**

---

## Important:
This visualization shows the actual sinusoidal distribution of magnetic field strength around the complete air-gap.
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.success("⚡ The flux waveform physically exists around the air-gap axis and rotates continuously to produce torque.")
